#!/usr/bin/env python3
"""
智能自动化运维系统主入口
整合监控、修复、优化、分析功能
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入运维模块
from src.monitoring.auto_monitor import WorkflowMonitor, AutoFixer, PerformanceTracker
from src.monitoring.ab_testing import ABTestManager
from src.monitoring.knowledge_base import KnowledgeBase

# 配置日志
# 确保日志目录存在
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/ops.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


class IntelligentAutoOps:
    """智能自动化运维系统"""

    def __init__(self, github_token: str = None, repo: str = None):
        """
        初始化运维系统

        Args:
            github_token: GitHub API Token
            repo: 仓库名称 (格式: owner/repo)
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN', '')
        self.repo = repo or os.getenv('GITHUB_REPOSITORY', 'aapeakinc-hue/miga-auto-workflow')

        # 初始化各个模块
        self.monitor = WorkflowMonitor(self.github_token, self.repo)
        self.fixer = AutoFixer()
        self.tracker = PerformanceTracker()
        self.ab_test_manager = ABTestManager()
        self.knowledge_base = KnowledgeBase()

        logger.info("✅ 智能自动化运维系统初始化完成")

    def run_full_monitoring(self) -> dict:
        """
        运行完整的监控流程

        Returns:
            监控结果字典
        """
        logger.info("🔍 开始完整监控流程...")

        result = {
            'timestamp': datetime.now().isoformat(),
            'monitoring': {},
            'auto_fix': {},
            'performance': {},
            'ab_tests': {},
            'knowledge_base': {}
        }

        # 1. 工作流健康监控
        logger.info("📊 监控工作流健康状态...")
        health = self.monitor.check_health()
        result['monitoring']['health'] = health

        if health['status'] == 'critical':
            logger.error(f"⚠️ 工作流健康状态: {health['message']}")

        # 2. 性能分析
        logger.info("📈 分析性能指标...")
        performance_report = self.tracker.generate_optimization_report()
        result['performance']['report'] = performance_report

        # 3. A/B测试分析
        logger.info("🧪 分析 A/B 测试...")
        # 简化版本：只获取活跃测试列表
        active_tests = self.ab_test_manager.tests.get('active_tests', [])
        result['ab_tests']['analysis'] = {
            'active_tests_count': len(active_tests),
            'active_tests': active_tests
        }

        # 4. 知识库更新
        logger.info("📚 更新知识库...")
        # 简化版本：只获取知识库统计
        kb_stats = {
            'total_entries': len(self.knowledge_base.knowledge.get('customers', [])),
            'last_update': datetime.now().isoformat()
        }
        result['knowledge_base']['stats'] = kb_stats

        # 5. 生成运维报告
        logger.info("📋 生成运维报告...")
        report = self.generate_ops_report(result)
        result['report'] = report

        # 6. 保存运维数据
        self.save_ops_data(result)

        logger.info("✅ 监控流程完成")

        return result

    def analyze_failure(self, run_id: str) -> dict:
        """
        分析失败的工作流运行

        Args:
            run_id: GitHub Actions 运行ID

        Returns:
            分析结果
        """
        logger.info(f"🔍 分析失败的运行: {run_id}")

        # 获取失败日志（这里需要 GitHub API）
        # 简化版本：从本地日志文件读取
        failure_log = self.get_failure_log(run_id)

        # 检测问题类型
        issue_type = self.fixer.detect_issue(failure_log)

        # 尝试修复
        fix_result = self.fixer.attempt_fix(failure_log)

        # 记录到知识库
        self.knowledge_base.add_failure_case({
            'run_id': run_id,
            'timestamp': datetime.now().isoformat(),
            'error_type': issue_type,
            'log': failure_log[:1000],  # 只保存前1000字符
            'fix': fix_result
        })

        return {
            'run_id': run_id,
            'issue_type': issue_type,
            'fix_result': fix_result
        }

    def get_failure_log(self, run_id: str) -> str:
        """
        获取失败日志

        Args:
            run_id: 运行ID

        Returns:
            日志内容
        """
        # 简化版本：从本地日志文件读取
        log_file = f"logs/workflow_{run_id}.log"

        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()

        # 如果没有日志文件，返回示例错误
        return "ModuleNotFoundError: No module named 'example_module'"

    def generate_ops_report(self, monitoring_result: dict) -> str:
        """
        生成运维报告

        Args:
            monitoring_result: 监控结果

        Returns:
            报告文本
        """
        health = monitoring_result['monitoring']['health']

        report = f"""
{'='*60}
🤖 智能自动化运维报告
{'='*60}

⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 工作流健康状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

状态: {health['status'].upper()}
消息: {health['message']}

运行统计:
  - 总运行次数: {health['analysis']['total_runs']}
  - 成功次数: {health['analysis']['success_runs']}
  - 失败次数: {health['analysis']['failed_runs']}
  - 成功率: {health['analysis']['success_rate']:.1f}%
  - 连续失败: {health['analysis']['consecutive_failures']} 次

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 性能指标
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{monitoring_result['performance']['report']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 知识库状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

总条目数: {monitoring_result['knowledge_base']['stats'].get('total_entries', 0)}
最新更新: {monitoring_result['knowledge_base']['stats'].get('last_update', '无')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 优化建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # 根据健康状态给出建议
        if health['status'] == 'critical':
            report += """
⚠️ 严重警告:
  - 工作流连续失败，需要立即检查！
  - 建议查看最近的失败日志
  - 考虑暂停自动化运行，修复问题后再启用

"""
        elif health['status'] == 'warning':
            report += """
⚠️ 警告:
  - 成功率低于预期，建议检查配置
  - 查看是否有频繁失败的任务

"""
        else:
            report += """
✅ 系统运行正常:
  - 继续监控性能指标
  - 定期审查和优化关键词策略

"""

        report += f"{'='*60}\n"

        return report

    def save_ops_data(self, monitoring_result: dict):
        """
        保存运维数据

        Args:
            monitoring_result: 监控结果
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存完整的运维数据
        ops_file = f"logs/ops_{timestamp}.json"
        try:
            with open(ops_file, 'w', encoding='utf-8') as f:
                json.dump(monitoring_result, f, ensure_ascii=False, indent=2)
            logger.info(f"✅ 运维数据已保存: {ops_file}")
        except Exception as e:
            logger.error(f"保存运维数据失败: {e}")

        # 保存运维报告
        report_file = f"logs/ops_report_{timestamp}.txt"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(monitoring_result['report'])
            logger.info(f"✅ 运维报告已保存: {report_file}")
        except Exception as e:
            logger.error(f"保存运维报告失败: {e}")

    def auto_optimize(self) -> dict:
        """
        自动优化配置

        Returns:
            优化结果
        """
        logger.info("🚀 开始自动优化...")

        result = {
            'timestamp': datetime.now().isoformat(),
            'optimizations': []
        }

        # 1. 分析关键词性能，推荐最佳关键词
        top_keywords = self.tracker.analyze_keyword_performance(top_n=5)
        if top_keywords:
            best_keyword = top_keywords[0]
            result['optimizations'].append({
                'type': 'keyword_recommendation',
                'value': best_keyword['keyword'],
                'reason': f"回复率最高 ({best_keyword['response_rate']:.1f}%)"
            })
            logger.info(f"✅ 推荐关键词: {best_keyword['keyword']}")

        # 2. A/B测试结果应用（简化版本）
        active_tests = self.ab_test_manager.tests.get('active_tests', [])
        if active_tests:
            result['optimizations'].append({
                'type': 'ab_test_status',
                'active_tests': len(active_tests),
                'message': f"有 {len(active_tests)} 个活跃的 A/B 测试"
            })
            logger.info(f"✅ A/B测试状态: {len(active_tests)} 个活跃测试")

        logger.info("✅ 自动优化完成")

        return result


def main():
    """主函数"""
    logger.info("🚀 启动智能自动化运维系统")

    # 创建日志目录
    os.makedirs('logs', exist_ok=True)

    # 获取 GitHub Token
    github_token = os.getenv('GITHUB_TOKEN', '')
    if not github_token:
        logger.warning("⚠️  GITHUB_TOKEN 未设置，部分功能可能受限")

    # 初始化运维系统
    ops = IntelligentAutoOps(github_token)

    # 运行完整监控
    try:
        result = ops.run_full_monitoring()

        # 打印报告
        print("\n" + result['report'])

        # 尝试自动优化
        optimization = ops.auto_optimize()
        logger.info(f"✅ 自动优化结果: {len(optimization['optimizations'])} 项优化")

        # 保存结果
        ops.save_ops_data(result)

        logger.info("✅ 智能自动化运维完成")
        return 0

    except Exception as e:
        logger.error(f"❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
