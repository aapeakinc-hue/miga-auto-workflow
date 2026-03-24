"""
自动化运维监控系统
监控工作流运行状态，自动检测和报告问题
"""
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowMonitor:
    """工作流监控器"""

    def __init__(self, github_token: str, repo: str):
        self.github_token = github_token
        self.repo = repo
        self.github_api = "https://api.github.com"

    def get_workflow_runs(self, workflow_file: str = "auto-workflow.yml") -> List[Dict]:
        """获取工作流运行记录"""
        url = f"{self.github_api}/repos/{self.repo}/actions/workflows/{workflow_file}/runs"
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('workflow_runs', [])
            else:
                logger.error(f"获取工作流记录失败: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"请求失败: {e}")
            return []

    def analyze_runs(self, runs: List[Dict]) -> Dict[str, Any]:
        """分析工作流运行情况"""
        if not runs:
            return {}

        total_runs = len(runs)
        success_runs = sum(1 for run in runs if run['conclusion'] == 'success')
        failed_runs = sum(1 for run in runs if run['conclusion'] == 'failure')

        success_rate = (success_runs / total_runs * 100) if total_runs > 0 else 0

        # 获取最近的失败记录
        recent_failures = [
            run for run in runs
            if run['conclusion'] == 'failure'
        ][:5]

        # 检查是否有连续失败
        consecutive_failures = 0
        for run in runs:
            if run['conclusion'] == 'failure':
                consecutive_failures += 1
            else:
                break

        return {
            'total_runs': total_runs,
            'success_runs': success_runs,
            'failed_runs': failed_runs,
            'success_rate': success_rate,
            'recent_failures': recent_failures,
            'consecutive_failures': consecutive_failures
        }

    def check_health(self) -> Dict[str, Any]:
        """检查工作流健康状态"""
        runs = self.get_workflow_runs()
        analysis = self.analyze_runs(runs)

        # 健康状态判断
        if analysis['consecutive_failures'] >= 3:
            health_status = 'critical'
            alert_message = f"⚠️ 严重：连续 {analysis['consecutive_failures']} 次失败！"
        elif analysis['success_rate'] < 50:
            health_status = 'warning'
            alert_message = f"⚠️ 警告：成功率只有 {analysis['success_rate']:.1f}%"
        else:
            health_status = 'healthy'
            alert_message = "✅ 工作流运行正常"

        return {
            'status': health_status,
            'message': alert_message,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }

    def send_alert(self, alert_data: Dict[str, Any]):
        """发送告警通知（可以集成到邮件、Slack等）"""
        logger.warning(f"⚠️ 告警: {alert_data['message']}")
        logger.warning(f"分析数据: {alert_data['analysis']}")

        # 这里可以添加邮件、Slack等通知方式
        # 例如：send_email("admin@miga.cc", alert_data['message'])


class AutoFixer:
    """自动修复器"""

    def __init__(self):
        self.fix_strategies = {
            'ModuleNotFoundError': self.fix_missing_module,
            'KeyError': self.fix_missing_secret,
            'ConnectionError': self.fix_network_issue,
            'TimeoutError': self.fix_timeout
        }

    def detect_issue(self, error_log: str) -> str:
        """检测错误类型"""
        for error_type in self.fix_strategies.keys():
            if error_type in error_log:
                return error_type
        return 'unknown'

    def fix_missing_module(self, error_log: str) -> Dict[str, Any]:
        """修复缺失模块"""
        # 提取模块名
        import re
        match = re.search(r"No module named '([^']+)'", error_log)
        if match:
            module_name = match.group(1)
            return {
                'issue': 'missing_module',
                'module': module_name,
                'fix': f"pip install {module_name}",
                'auto_fixable': True
            }
        return {'auto_fixable': False}

    def fix_missing_secret(self, error_log: str) -> Dict[str, Any]:
        """修复缺失密钥"""
        import re
        match = re.search(r"KeyError: '([^']+)'", error_log)
        if match:
            secret_name = match.group(1)
            return {
                'issue': 'missing_secret',
                'secret': secret_name,
                'fix': f"请在 GitHub Secrets 中添加 {secret_name}",
                'auto_fixable': False  # 需要手动配置
            }
        return {'auto_fixable': False}

    def fix_network_issue(self, error_log: str) -> Dict[str, Any]:
        """修复网络问题"""
        return {
            'issue': 'network_error',
            'fix': '检查网络连接或 API 服务状态',
            'auto_fixable': False
        }

    def fix_timeout(self, error_log: str) -> Dict[str, Any]:
        """修复超时问题"""
        return {
            'issue': 'timeout',
            'fix': '增加超时时间或优化代码',
            'auto_fixable': False
        }

    def attempt_fix(self, error_log: str) -> Dict[str, Any]:
        """尝试自动修复"""
        issue_type = self.detect_issue(error_log)
        fix_strategy = self.fix_strategies.get(issue_type)

        if fix_strategy:
            return fix_strategy(error_log)
        else:
            return {
                'issue': 'unknown',
                'fix': '需要手动检查',
                'auto_fixable': False
            }


class PerformanceTracker:
    """性能跟踪器"""

    def __init__(self, metrics_file: str = "logs/metrics.json"):
        self.metrics_file = metrics_file
        self.load_metrics()

    def load_metrics(self):
        """加载指标数据"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    self.metrics = json.load(f)
            else:
                self.metrics = {
                    'daily_stats': [],
                    'keyword_performance': {},
                    'email_template_performance': {},
                    'customer_segments': {}
                }
        except Exception as e:
            logger.error(f"加载指标失败: {e}")
            self.metrics = {}

    def save_metrics(self):
        """保存指标数据"""
        try:
            os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存指标失败: {e}")

    def record_daily_stats(self, date: str, stats: Dict[str, Any]):
        """记录每日统计"""
        self.metrics['daily_stats'].append({
            'date': date,
            **stats
        })
        self.save_metrics()

    def record_keyword_performance(self, keyword: str, performance: Dict[str, Any]):
        """记录关键词性能"""
        if keyword not in self.metrics['keyword_performance']:
            self.metrics['keyword_performance'][keyword] = []
        self.metrics['keyword_performance'][keyword].append({
            'timestamp': datetime.now().isoformat(),
            **performance
        })
        self.save_metrics()

    def analyze_keyword_performance(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """分析关键词性能"""
        keyword_stats = []

        for keyword, performances in self.metrics['keyword_performance'].items():
            if not performances:
                continue

            total_emails = sum(p.get('emails_sent', 0) for p in performances)
            total_responses = sum(p.get('responses', 0) for p in performances)
            response_rate = (total_responses / total_emails * 100) if total_emails > 0 else 0

            keyword_stats.append({
                'keyword': keyword,
                'total_emails': total_emails,
                'total_responses': total_responses,
                'response_rate': response_rate
            })

        # 按回复率排序
        keyword_stats.sort(key=lambda x: x['response_rate'], reverse=True)
        return keyword_stats[:top_n]

    def generate_optimization_report(self) -> str:
        """生成优化报告"""
        top_keywords = self.analyze_keyword_performance()

        report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 自动化运维优化报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔍 关键词性能排名 (Top 10)
"""
        for i, kw in enumerate(top_keywords, 1):
            report += f"""
{i}. {kw['keyword']}
   - 发送邮件: {kw['total_emails']} 封
   - 回复数量: {kw['total_responses']} 个
   - 回复率: {kw['response_rate']:.1f}%
"""

        report += """
💡 优化建议
"""
        if top_keywords:
            best_keyword = top_keywords[0]
            report += f"""
✅ 最佳关键词: {best_keyword['keyword']} (回复率: {best_keyword['response_rate']:.1f}%)
   建议: 优先使用此类关键词

"""
        else:
            report += "暂无足够数据，继续收集..."

        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        return report


if __name__ == "__main__":
    # 测试监控功能
    logger.info("🔍 启动自动化运维监控系统")

    # 这里需要 GitHub Token 才能真正监控
    # github_token = os.getenv('GITHUB_TOKEN', '')
    # monitor = WorkflowMonitor(github_token, 'aapeakinc-hue/miga-auto-workflow')
    # health = monitor.check_health()
    # print(json.dumps(health, indent=2, ensure_ascii=False))

    logger.info("✅ 监控系统已启动")
