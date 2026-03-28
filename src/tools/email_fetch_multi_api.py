"""
多 API 邮箱抓取工具
支持 Snov.io, Hunter.io, Clearbit 等多个免费 API
自动轮换使用，突破单账户限制
"""
import requests
import logging
from typing import Dict, List, Any, Optional
from email_api_manager import get_email_api_key, mark_api_key_used, email_api_manager

logger = logging.getLogger(__name__)


class MultiAPIMailFetcher:
    """
    多 API 邮箱抓取器

    支持的 API：
    1. Snov.io（免费 50/月）
    2. Hunter.io（免费 25/月）
    3. Clearbit（免费 50/月）
    4. Voila Norbert（免费 50/月）
    """

    def __init__(self):
        self.current_api = None

    def fetch_emails_from_domain(self, domain: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        从域名抓取邮箱

        Args:
            domain: 目标域名
            max_results: 最大结果数

        Returns:
            邮箱列表
        """
        # 尝试使用 Snov.io
        emails = self._fetch_from_snovio(domain, max_results)
        if emails:
            logger.info(f"✅ 从 Snov.io 获取到 {len(emails)} 个邮箱")
            return emails

        # 尝试使用 Hunter.io
        emails = self._fetch_from_hunter(domain, max_results)
        if emails:
            logger.info(f"✅ 从 Hunter.io 获取到 {len(emails)} 个邮箱")
            return emails

        # 尝试使用 Clearbit
        emails = self._fetch_from_clearbit(domain, max_results)
        if emails:
            logger.info(f"✅ 从 Clearbit 获取到 {len(emails)} 个邮箱")
            return emails

        # 所有 API 都失败，返回空列表
        logger.warning(f"⚠️  所有 API 都无法获取 {domain} 的邮箱")
        return []

    def _fetch_from_snovio(self, domain: str, max_results: int) -> List[Dict[str, Any]]:
        """使用 Snov.io API 获取邮箱"""
        api_key = self._get_api_key("snovio")
        if not api_key:
            return []

        try:
            url = "https://api.snov.io/v2/domain-emails-with-info"
            headers = {
                'Authorization': api_key,
                'Content-Type': 'application/json'
            }
            data = {
                'domain': domain,
                'limit': max_results
            }

            response = requests.post(url, json=data, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                emails = result.get('data', {}).get('emails', [])

                # 标记 API 已使用
                self._mark_api_used(api_key)

                # 格式化结果
                return [
                    {
                        'email': email.get('email'),
                        'first_name': email.get('firstName', ''),
                        'last_name': email.get('lastName', ''),
                        'position': email.get('position', ''),
                        'source': 'snovio'
                    }
                    for email in emails[:max_results]
                ]

            elif response.status_code == 429:
                logger.warning(f"Snov.io API 限流: {response.text}")
                return []

            else:
                logger.error(f"Snov.io API 错误: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Snov.io API 调用失败: {e}")
            return []

    def _fetch_from_hunter(self, domain: str, max_results: int) -> List[Dict[str, Any]]:
        """使用 Hunter.io API 获取邮箱"""
        api_key = self._get_api_key("hunter")
        if not api_key:
            return []

        try:
            url = f"https://api.hunter.io/v2/email-finder"
            params = {
                'domain': domain,
                'api_key': api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                result = response.json()
                email_data = result.get('data', {})

                if email_data.get('email'):
                    # 标记 API 已使用
                    self._mark_api_used(api_key)

                    return [{
                        'email': email_data.get('email'),
                        'first_name': email_data.get('first_name', ''),
                        'last_name': email_data.get('last_name', ''),
                        'position': '',
                        'source': 'hunter.io',
                        'confidence': email_data.get('score', 0)
                    }]

            return []

        except Exception as e:
            logger.error(f"Hunter.io API 调用失败: {e}")
            return []

    def _fetch_from_clearbit(self, domain: str, max_results: int) -> List[Dict[str, Any]]:
        """使用 Clearbit API 获取邮箱"""
        api_key = self._get_api_key("clearbit")
        if not api_key:
            return []

        try:
            # Clearbit 使用 Reveal API
            url = f"https://person.clearbit.com/v1/people/domain/{domain}"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                person = response.json()

                if person.get('email'):
                    # 标记 API 已使用
                    self._mark_api_used(api_key)

                    return [{
                        'email': person.get('email'),
                        'first_name': person.get('name', {}).get('givenName', ''),
                        'last_name': person.get('name', {}).get('familyName', ''),
                        'position': person.get('title', ''),
                        'source': 'clearbit'
                    }]

            return []

        except Exception as e:
            logger.error(f"Clearbit API 调用失败: {e}")
            return []

    def _get_api_key(self, api_name: str) -> Optional[str]:
        """获取 API Key"""
        return get_email_api_key()

    def _mark_api_used(self, api_key: str):
        """标记 API 已使用"""
        mark_api_key_used(api_key)


# 全局实例
multi_api_mail_fetcher = MultiAPIMailFetcher()


def fetch_emails_from_domain(domain: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    从域名抓取邮箱（便捷函数）

    Args:
        domain: 目标域名
        max_results: 最大结果数

    Returns:
        邮箱列表
    """
    return multi_api_mail_fetcher.fetch_emails_from_domain(domain, max_results)


if __name__ == "__main__":
    # 测试代码
    from email_api_manager import setup_email_apis

    # 设置 API Keys（测试用）
    setup_email_apis()

    # 测试域名
    test_domain = "miga.cc"

    print(f"\n🔍 测试抓取邮箱: {test_domain}")
    print("=" * 60)

    emails = fetch_emails_from_domain(test_domain, max_results=5)

    if emails:
        print(f"\n✅ 找到 {len(emails)} 个邮箱:")
        for email in emails:
            print(f"  📧 {email['email']}")
            print(f"     姓名: {email.get('first_name', '')} {email.get('last_name', '')}")
            print(f"     职位: {email.get('position', 'N/A')}")
            print(f"     来源: {email['source']}")
            print()
    else:
        print("\n⚠️  未找到邮箱")

    # 打印统计信息
    stats = email_api_manager.get_usage_stats()
    print("\n📊 API 使用统计:")
    for detail in stats['details']:
        print(f"  {detail['name']}: {detail['used']}/{detail['limit']} (剩余: {detail['remaining']})")
