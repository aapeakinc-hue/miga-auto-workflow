"""
外贸客户开发自动化工作流 - 真实 API 版本
基于 LangGraph 工作流，调用真实的 LLM 和 Web Search API
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入工作流
from graphs.graph import main_graph
from graphs.state import GraphInput

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_sent_emails():
    """加载已发送记录"""
    sent_file = "logs/sent_emails.json"
    try:
        if os.path.exists(sent_file):
            with open(sent_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"加载发送记录失败: {e}")
        return []


def save_sent_emails(sent_emails):
    """保存发送记录"""
    sent_file = "logs/sent_emails.json"
    try:
        os.makedirs("logs", exist_ok=True)
        with open(sent_file, 'w', encoding='utf-8') as f:
            json.dump(sent_emails, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存发送记录失败: {e}")


def generate_report(result: Dict[str, Any]):
    """生成执行报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 外贸客户开发工作流报告（真实 API 版本）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 执行时间: {timestamp}

📋 工作流结果:
"""

    if "send_results" in result:
        send_results = result["send_results"]
        total = send_results.get("total", 0)
        success = send_results.get("success", 0)
        failed = send_results.get("failed", 0)

        report += f"""
  - 总邮件数: {total}
  - 成功: {success}
  - 失败: {failed}
"""

        if "details" in send_results and send_results["details"]:
            report += "\n📧 发送详情:\n"
            for detail in send_results["details"]:
                status_icon = "✅" if detail.get("status") == "success" else "❌"
                report += f"  {status_icon} {detail.get('to_email', 'N/A')} - {detail.get('to_company', 'N/A')}\n"

    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 说明:
  - 使用真实的 LLM API 生成邮件内容
  - 使用真实的 Web Search API 搜索客户
  - 使用真实的 Resend API 发送邮件

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    logger.info(report)

    # 保存报告到文件
    try:
        os.makedirs("logs", exist_ok=True)
        report_file = f"logs/workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"报告已保存: {report_file}")
    except Exception as e:
        logger.error(f"保存报告失败: {e}")


def run_auto_workflow(target_keywords: str = None, website_url: str = None):
    """
    运行自动化工作流（使用真实 API）

    Args:
        target_keywords: 目标客户关键词
        website_url: 产品网站 URL
    """
    logger.info("🚀 外贸客户开发自动化工作流启动（真实 API 版本）")
    logger.info("=" * 60)

    # 默认参数
    if not target_keywords:
        target_keywords = "美国水晶工艺品批发商"
    if not website_url:
        website_url = "https://www.miga.cc"

    logger.info(f"🔍 目标关键词: {target_keywords}")
    logger.info(f"🌐 产品网站: {website_url}")

    # 构建输入
    workflow_input = GraphInput(
        target_keywords=target_keywords,
        website_url=website_url
    )

    try:
        # 运行工作流
        logger.info("\n🔄 开始执行工作流...")
        result = main_graph.invoke(workflow_input)

        # 生成报告
        generate_report(result)

        # 检查结果
        if "send_results" in result:
            send_results = result["send_results"]
            total = send_results.get("total", 0)
            success = send_results.get("success", 0)

            logger.info("\n" + "=" * 60)
            logger.info(f"✅ 工作流执行完成 - 成功发送: {success}/{total}")
            logger.info("=" * 60)

            return {
                "success": True,
                "result": result
            }
        else:
            logger.warning("⚠️  工作流执行完成，但没有邮件发送结果")
            return {
                "success": False,
                "result": result,
                "message": "没有邮件发送结果"
            }

    except Exception as e:
        logger.error(f"❌ 工作流执行失败: {e}")
        import traceback
        traceback.print_exc()

        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="外贸客户开发自动化工作流（真实 API 版本）")
    parser.add_argument(
        "--keywords",
        type=str,
        default="美国水晶工艺品批发商",
        help="目标客户关键词"
    )
    parser.add_argument(
        "--website",
        type=str,
        default="https://www.miga.cc",
        help="产品网站 URL"
    )

    args = parser.parse_args()

    # 运行工作流
    result = run_auto_workflow(
        target_keywords=args.keywords,
        website_url=args.website
    )

    # 返回状态码
    if result.get("success"):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
