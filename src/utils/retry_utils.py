"""
工具函数：自动重试和健康检查
"""
import time
import logging
from functools import wraps
from typing import Callable, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def retry_on_failure(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    allowed_exceptions: tuple = (Exception,),
    on_retry: Callable = None
):
    """
    自动重试装饰器

    Args:
        max_retries: 最大重试次数
        backoff_factor: 退避因子（指数退避）
        allowed_exceptions: 允许重试的异常类型
        on_retry: 重试时的回调函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    last_exception = e

                    # 最后一次尝试失败，不再重试
                    if attempt == max_retries - 1:
                        logger.error(
                            f"❌ {func.__name__} 失败：{e}（已重试 {max_retries} 次）"
                        )
                        raise

                    # 计算等待时间（指数退避）
                    wait_time = backoff_factor ** attempt

                    logger.warning(
                        f"⚠️  {func.__name__} 失败（第 {attempt + 1}/{max_retries} 次）：{e}"
                        f"，{wait_time:.1f} 秒后重试..."
                    )

                    # 执行重试回调
                    if on_retry:
                        on_retry(attempt, e, wait_time)

                    # 等待后重试
                    time.sleep(wait_time)

            # 如果所有重试都失败
            raise last_exception

        return wrapper
    return decorator


class APIHealthChecker:
    """API 健康检查器"""

    def __init__(self):
        self.api_status = {}
        self.last_check_time = {}

    def check_snovio_health(self, api_key: str) -> bool:
        """
        检查 Snov.io API 健康状态

        Args:
            api_key: Snov.io API 密钥

        Returns:
            True 表示健康，False 表示不健康
        """
        import requests

        if not api_key:
            logger.warning("⚠️  Snov.io API Key 未配置")
            return False

        url = "https://api.snov.io/v1/get-balance"
        headers = {'Authorization': api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                balance = data.get('credits', 0)
                logger.info(f"✅ Snov.io API 正常（余额: {balance} credits）")
                return True
            elif response.status_code == 401:
                logger.error("❌ Snov.io API Key 无效或已过期")
                return False
            elif response.status_code == 429:
                logger.warning("⚠️  Snov.io API 限流")
                return False
            else:
                logger.error(f"❌ Snov.io API 错误: {response.status_code}")
                return False

        except requests.exceptions.Timeout:
            logger.error("❌ Snov.io API 超时")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ Snov.io API 连接失败")
            return False
        except Exception as e:
            logger.error(f"❌ Snov.io API 检查失败: {e}")
            return False

    def check_resend_health(self, api_key: str) -> bool:
        """
        检查 Resend API 健康状态

        Args:
            api_key: Resend API 密钥

        Returns:
            True 表示健康，False 表示不健康
        """
        import requests

        if not api_key:
            logger.warning("⚠️  Resend API Key 未配置")
            return False

        url = "https://api.resend.com/domains"
        headers = {'Authorization': f'Bearer {api_key}'}

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                logger.info("✅ Resend API 正常")
                return True
            elif response.status_code == 401:
                logger.error("❌ Resend API Key 无效或已过期")
                return False
            elif response.status_code == 429:
                logger.warning("⚠️  Resend API 限流")
                return False
            else:
                logger.error(f"❌ Resend API 错误: {response.status_code}")
                return False

        except requests.exceptions.Timeout:
            logger.error("❌ Resend API 超时")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ Resend API 连接失败")
            return False
        except Exception as e:
            logger.error(f"❌ Resend API 检查失败: {e}")
            return False

    def check_all_apis(self, snovio_key: str = None, resend_key: str = None) -> dict:
        """
        检查所有 API 健康状态

        Args:
            snovio_key: Snov.io API 密钥
            resend_key: Resend API 密钥

        Returns:
            包含所有 API 状态的字典
        """
        logger.info("🔍 开始 API 健康检查...")

        results = {
            'timestamp': datetime.now().isoformat(),
            'apis': {}
        }

        # 检查 Snov.io
        if snovio_key:
            results['apis']['snovio'] = {
                'status': 'healthy' if self.check_snovio_health(snovio_key) else 'unhealthy'
            }
        else:
            results['apis']['snovio'] = {
                'status': 'not_configured',
                'message': 'API Key 未配置'
            }

        # 检查 Resend
        if resend_key:
            results['apis']['resend'] = {
                'status': 'healthy' if self.check_resend_health(resend_key) else 'unhealthy'
            }
        else:
            results['apis']['resend'] = {
                'status': 'not_configured',
                'message': 'API Key 未配置'
            }

        # 计算整体健康状态
        all_healthy = all(
            api.get('status') == 'healthy'
            for api in results['apis'].values()
        )
        results['overall_status'] = 'healthy' if all_healthy else 'degraded'

        if all_healthy:
            logger.info("✅ 所有 API 健康检查通过")
        else:
            logger.warning("⚠️  部分或全部 API 健康检查失败")

        return results

    def generate_health_report(self, health_results: dict) -> str:
        """
        生成健康检查报告

        Args:
            health_results: 健康检查结果

        Returns:
            报告文本
        """
        report = f"""
{'='*60}
🏥 API 健康检查报告
{'='*60}

⏰ 检查时间: {health_results['timestamp']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 整体状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

状态: {health_results['overall_status'].upper()}
"""

        if health_results['overall_status'] == 'healthy':
            report += "\n✅ 所有 API 运行正常\n"
        else:
            report += "\n⚠️  部分 API 存在问题，请检查详细信息\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += "🔍 API 详细状态\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        for api_name, api_info in health_results['apis'].items():
            status = api_info['status']
            status_emoji = {
                'healthy': '✅',
                'unhealthy': '❌',
                'not_configured': '⚠️'
            }.get(status, '❓')

            report += f"\n{status_emoji} {api_name.upper()}\n"
            report += f"   状态: {status}\n"

            if 'message' in api_info:
                report += f"   信息: {api_info['message']}\n"

        report += f"\n{'='*60}\n"

        return report


def log_retry_attempt(attempt: int, error: Exception, wait_time: float):
    """
    记录重试尝试

    Args:
        attempt: 当前尝试次数
        error: 错误对象
        wait_time: 等待时间
    """
    logger.warning(f"🔄 重试中...（第 {attempt + 1} 次失败，等待 {wait_time:.1f} 秒）")


# 示例用法
if __name__ == "__main__":
    # 创建健康检查器
    health_checker = APIHealthChecker()

    # 检查所有 API
    results = health_checker.check_all_apis(
        snovio_key=os.getenv('SNOVIO_API_KEY'),
        resend_key=os.getenv('RESEND_API_KEY')
    )

    # 生成报告
    report = health_checker.generate_health_report(results)
    print(report)
