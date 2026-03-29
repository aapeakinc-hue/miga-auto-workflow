#!/usr/bin/env python3
"""
MIGA 数据驱动外贸客户开发系统 - 主脚本
功能：简化系统使用，提供命令行接口
"""
import argparse
from datetime import date, datetime
import sys

def run_init():
    """初始化系统"""
    print("=" * 80)
    print("MIGA 数据驱动外贸客户开发系统 - 系统初始化")
    print("=" * 80)
    print()

    from workflow_orchestrator import WorkflowOrchestrator

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.initialize_system()

    if result["success"]:
        print("\n✅ 系统初始化完成！")
        print("\n已初始化的组件:")
        for component, status in result["components"].items():
            print(f"  {component}: {'✅' if status else '❌'}")

        print("\n下一步:")
        print("  运行每日工作流: python main.py --daily")
        print("  查看帮助: python main.py --help")
    else:
        print(f"\n❌ 系统初始化失败: {result['message']}")
        sys.exit(1)

def run_daily_workflow(work_date=None, market="USA"):
    """运行每日工作流"""
    if work_date is None:
        work_date = date.today()
    else:
        work_date = datetime.strptime(work_date, "%Y-%m-%d").date()

    print("=" * 80)
    print(f"MIGA 每日工作流 - {work_date} - {market}")
    print("=" * 80)
    print()

    from workflow_orchestrator import WorkflowOrchestrator

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_daily_workflow(work_date, market)

    if result["success"]:
        print("\n✅ 每日工作流执行完成！")

        print("\n执行步骤:")
        for step in result["steps"]:
            status_icon = "✅" if step["status"] == "completed" or step["status"] == "success" else "❌"
            print(f"  {status_icon} 步骤{step['step']}: {step['description']}")

        print("\n关键指标:")
        metrics = result.get("daily_report", {}).get("metrics", {})
        print(f"  任务完成率: {metrics.get('completion_rate', 0):.1f}%")
        print(f"  发送邮件: {metrics.get('emails_sent', 0)} 封")
        print(f"  新增客户: {metrics.get('new_customers', 0)} 个")

        print("\n💡 提示: 查看邮箱 info@miga.cc 获取详细报告")
    else:
        print(f"\n❌ 每日工作流执行失败: {result.get('error', '')}")
        sys.exit(1)

def run_weekly_workflow(start_date=None, market="USA"):
    """运行周度工作流"""
    if start_date is None:
        # 计算本周开始日期（周一）
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    from datetime import timedelta

    print("=" * 80)
    print(f"MIGA 周度工作流 - {start_date} 至 {start_date + timedelta(days=6)} - {market}")
    print("=" * 80)
    print()

    from workflow_orchestrator import WorkflowOrchestrator

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_weekly_workflow(start_date, market)

    if result["success"]:
        print("\n✅ 周度工作流执行完成！")

        print("\n本周数据:")
        weekly_metrics = result.get("weekly_report", {}).get("weekly_metrics", {})
        print(f"  总任务数: {weekly_metrics.get('total_tasks', 0)}")
        print(f"  完成任务: {weekly_metrics.get('completed_tasks', 0)}")
        print(f"  发送邮件: {weekly_metrics.get('total_emails_sent', 0)} 封")
        print(f"  新增客户: {weekly_metrics.get('total_new_customers', 0)} 个")

        print("\n💡 提示: 查看邮箱 info@miga.cc 获取详细报告")
    else:
        print(f"\n❌ 周度工作流执行失败: {result.get('error', '')}")
        sys.exit(1)

def run_monthly_workflow(year=None, month=None, market="USA"):
    """运行月度工作流"""
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month

    print("=" * 80)
    print(f"MIGA 月度工作流 - {year}-{month:02d} - {market}")
    print("=" * 80)
    print()

    from workflow_orchestrator import WorkflowOrchestrator

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_monthly_workflow(year, month, market)

    if result["success"]:
        print("\n✅ 月度工作流执行完成！")

        print("\n本月数据:")
        monthly_metrics = result.get("monthly_report", {}).get("monthly_metrics", {})
        print(f"  总任务数: {monthly_metrics.get('total_tasks', 0)}")
        print(f"  完成任务: {monthly_metrics.get('completed_tasks', 0)}")
        print(f"  发送邮件: {monthly_metrics.get('total_emails_sent', 0)} 封")
        print(f"  新增客户: {monthly_metrics.get('total_new_customers', 0)} 个")

        print("\n目标达成情况:")
        goal_achievement = result.get("monthly_report", {}).get("goal_achievement", {})
        for metric, rate in goal_achievement.items():
            print(f"  {metric}: {rate:.1f}%")

        # 检查是否需要调整目标
        adjustment = result.get("adjustment_report", {}).get("adjustment_analysis", {})
        if adjustment.get("adjustment_needed"):
            print(f"\n🔄 目标调整: {adjustment['adjustment_strategy']}")
            print(f"   调整因子: {adjustment['adjustment_factor']:.2f}")
            print(f"   原因: {adjustment['reason']}")

        print("\n💡 提示: 查看邮箱 info@miga.cc 获取详细报告和调整通知")
    else:
        print(f"\n❌ 月度工作流执行失败: {result.get('error', '')}")
        sys.exit(1)

def run_annual_workflow(year=None):
    """运行年度工作流"""
    if year is None:
        year = date.today().year

    print("=" * 80)
    print(f"MIGA 年度工作流 - {year}")
    print("=" * 80)
    print()

    from workflow_orchestrator import WorkflowOrchestrator

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_annual_workflow(year)

    if result["success"]:
        print("\n✅ 年度工作流执行完成！")

        print("\n年度目标达成情况:")
        annual_achievement = result.get("annual_report", {}).get("annual_achievement", {})
        for market, achievement in annual_achievement.items():
            print(f"\n  {market} 市场:")
            for metric, rate in achievement.items():
                if isinstance(rate, (int, float)):
                    print(f"    {metric}: {rate:.1f}%")

        print("\n💡 提示: 查看邮箱 info@miga.cc 获取详细报告")
    else:
        print(f"\n❌ 年度工作流执行失败: {result.get('error', '')}")
        sys.exit(1)

def run_full_workflow():
    """运行完整工作流"""
    print("=" * 80)
    print("MIGA 完整工作流")
    print("=" * 80)
    print()

    from workflow_orchestrator import WorkflowOrchestrator

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_full_workflow()

    if result["success"]:
        print("\n✅ 完整工作流执行完成！")
        print(f"\n执行时间: {result['executed_at']}")

        results = result["results"]

        print("\n各模块执行结果:")
        print(f"  系统初始化: {'✅' if results['init_result']['success'] else '❌'}")
        print(f"  每日工作流: {'✅' if results['daily_result']['success'] else '❌'}")

        if results.get("weekly_result"):
            print(f"  周度工作流: {'✅' if results['weekly_result']['success'] else '❌'}")

        if results.get("monthly_result"):
            print(f"  月度工作流: {'✅' if results['monthly_result']['success'] else '❌'}")

        if results.get("annual_result"):
            print(f"  年度工作流: {'✅' if results['annual_result']['success'] else '❌'}")

        print("\n💡 提示: 查看邮箱 info@miga.cc 获取详细报告")
    else:
        print(f"\n❌ 完整工作流执行失败: {result.get('error', '')}")
        sys.exit(1)

def show_status():
    """显示系统状态"""
    print("=" * 80)
    print("MIGA 系统状态")
    print("=" * 80)
    print()

    import os

    # 检查数据库文件
    databases = [
        ("市场数据", "market_data.db"),
        ("目标数据库", "goals.db"),
        ("每日计划", "daily_planner.db"),
        ("CRM系统", "miga_crm.db")
    ]

    print("📊 数据库状态:")
    all_exist = True
    for name, db_file in databases:
        exists = os.path.exists(db_file)
        print(f"  {name}: {'✅' if exists else '❌'}")
        if not exists:
            all_exist = False

    if not all_exist:
        print("\n⚠️ 部分数据库不存在，请运行系统初始化:")
        print("  python main.py --init")

    print("\n📅 今日任务:")
    from daily_planner import DailyPlanner

    planner = DailyPlanner()
    today = date.today()

    # 检查美国市场
    daily_plan = planner.get_daily_plan(today, "USA")
    if "error" not in daily_plan:
        print(f"  美国市场: {len(daily_plan['tasks'])} 个任务")

    print("\n🎯 当前目标:")
    from goal_setting import GoalSetting

    goal_system = GoalSetting()
    year = today.year
    month = today.month

    annual_goal = goal_system.get_annual_goal(2026, "USA")
    if "error" not in annual_goal:
        print(f"  2026年度目标 (美国市场):")
        print(f"    客户开发: {annual_goal['customer_development_goal']}")
        print(f"    意向客户: {annual_goal['intention_customer_goal']}")
        print(f"    成交客户: {annual_goal['deal_customer_goal']}")
        print(f"    收入目标: ${annual_goal['revenue_goal']:,.0f}")

    print("\n" + "=" * 80)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="MIGA 数据驱动外贸客户开发系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化系统
  python main.py --init

  # 运行每日工作流
  python main.py --daily

  # 运行周度工作流
  python main.py --weekly

  # 运行月度工作流
  python main.py --monthly

  # 运行年度工作流
  python main.py --annual

  # 运行完整工作流
  python main.py --full

  # 查看系统状态
  python main.py --status

  # 指定日期和市场
  python main.py --daily --date 2026-03-22 --market UK
        """
    )

    parser.add_argument("--init", action="store_true", help="初始化系统")
    parser.add_argument("--daily", action="store_true", help="运行每日工作流")
    parser.add_argument("--weekly", action="store_true", help="运行周度工作流")
    parser.add_argument("--monthly", action="store_true", help="运行月度工作流")
    parser.add_argument("--annual", action="store_true", help="运行年度工作流")
    parser.add_argument("--full", action="store_true", help="运行完整工作流")
    parser.add_argument("--status", action="store_true", help="显示系统状态")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--start-date", type=str, help="指定周开始日期 (YYYY-MM-DD)")
    parser.add_argument("--year", type=int, help="指定年份")
    parser.add_argument("--month", type=int, help="指定月份")
    parser.add_argument("--market", type=str, default="USA", help="指定市场 (默认: USA)")

    args = parser.parse_args()

    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # 执行相应的命令
    if args.init:
        run_init()
    elif args.daily:
        run_daily_workflow(args.date, args.market)
    elif args.weekly:
        run_weekly_workflow(args.start_date, args.market)
    elif args.monthly:
        run_monthly_workflow(args.year, args.month, args.market)
    elif args.annual:
        run_annual_workflow(args.year)
    elif args.full:
        run_full_workflow()
    elif args.status:
        show_status()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
