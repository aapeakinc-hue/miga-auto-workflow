#!/usr/bin/env python3
"""
工作流编排器
功能：整合市场研究、目标设定、每日计划、报告生成、邮件发送、目标调整
"""
import json
from typing import Dict, List
from datetime import datetime, date, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/work/logs/bypass/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkflowOrchestrator:
    """工作流编排器"""

    def __init__(self):
        from market_research import MarketResearch
        from goal_setting import GoalSetting
        from daily_planner import DailyPlanner
        from report_generator import ReportGenerator
        from summary_sender import SummarySender
        from goal_adjuster import GoalAdjuster

        self.market_research = MarketResearch()
        self.goal_setting = GoalSetting()
        self.daily_planner = DailyPlanner()
        self.report_generator = ReportGenerator()
        self.summary_sender = SummarySender()
        self.goal_adjuster = GoalAdjuster()

    def initialize_system(self) -> Dict:
        """初始化系统"""
        logger.info("开始初始化MIGA自动化系统...")

        results = {
            "market_research": False,
            "goal_setting": False,
            "daily_planner": False
        }

        try:
            # 初始化市场研究（导入示例数据）
            from market_research import load_sample_market_data
            customs_data, market_size_data = load_sample_market_data()
            self.market_research.import_customs_data(customs_data)
            self.market_research.import_market_size_data(market_size_data)
            results["market_research"] = True
            logger.info("✅ 市场研究系统初始化完成")

            # 初始化目标设定
            from goal_setting import initialize_sample_goals
            initialize_sample_goals()
            results["goal_setting"] = True
            logger.info("✅ 目标设定系统初始化完成")

            # 初始化每日计划（示例数据）
            from daily_planner import generate_sample_daily_plan
            generate_sample_daily_plan()
            results["daily_planner"] = True
            logger.info("✅ 每日计划系统初始化完成")

        except Exception as e:
            logger.error(f"❌ 系统初始化失败: {e}")

        return {
            "success": all(results.values()),
            "components": results,
            "message": "系统初始化完成" if all(results.values()) else "部分组件初始化失败"
        }

    def run_daily_workflow(self, work_date: date = None, market: str = "USA") -> Dict:
        """运行每日工作流"""
        if work_date is None:
            work_date = date.today()

        logger.info(f"开始执行每日工作流 - {work_date} - {market}")

        results = {
            "date": work_date.isoformat(),
            "market": market,
            "steps": []
        }

        try:
            # 步骤1: 生成每日计划（如果不存在）
            logger.info("步骤1: 检查每日计划...")
            daily_plan = self.daily_planner.get_daily_plan(work_date, market)

            if "error" in daily_plan:
                # 创建默认每日计划
                tasks = [
                    {
                        "task_id": 1,
                        "description": "执行客户搜索工作流",
                        "category": "客户开发",
                        "priority": "high",
                        "estimated_time": "2小时",
                        "responsible": "工作流系统"
                    },
                    {
                        "task_id": 2,
                        "description": "发送开发邮件20封",
                        "category": "邮件发送",
                        "priority": "high",
                        "estimated_time": "1小时",
                        "responsible": "工作流系统"
                    },
                    {
                        "task_id": 3,
                        "description": "检查邮箱回复并跟进",
                        "category": "客户跟进",
                        "priority": "high",
                        "estimated_time": "1小时",
                        "responsible": "人工"
                    },
                    {
                        "task_id": 4,
                        "description": "更新CRM系统",
                        "category": "数据管理",
                        "priority": "medium",
                        "estimated_time": "0.5小时",
                        "responsible": "人工"
                    },
                    {
                        "task_id": 5,
                        "description": "分析当日数据并生成报告",
                        "category": "数据分析",
                        "priority": "medium",
                        "estimated_time": "0.5小时",
                        "responsible": "系统"
                    }
                ]

                expected_outcomes = [
                    "成功搜索到20-30个潜在客户",
                    "成功发送20封开发邮件",
                    "收到3-5封客户回复",
                    "CRM系统数据更新完整",
                    "生成每日总结报告"
                ]

                self.daily_planner.create_daily_plan(
                    plan_date=work_date,
                    market=market,
                    tasks=tasks,
                    expected_outcomes=expected_outcomes,
                    priority="high"
                )
                logger.info("✅ 每日计划已创建")
            else:
                logger.info("✅ 每日计划已存在")

            results["steps"].append({"step": 1, "status": "completed", "description": "每日计划检查完成"})

            # 步骤2: 生成每日总结
            logger.info("步骤2: 生成每日总结...")
            daily_report = self.report_generator.generate_daily_report(work_date, market)
            logger.info("✅ 每日总结已生成")
            results["steps"].append({"step": 2, "status": "completed", "description": "每日总结生成完成"})

            # 步骤3: 发送每日总结邮件
            logger.info("步骤3: 发送每日总结邮件...")
            send_result = self.summary_sender.send_daily_summary(daily_report)
            if send_result.get("success"):
                logger.info(f"✅ 每日总结邮件已发送，消息ID: {send_result.get('message_id', '')}")
            else:
                logger.error(f"❌ 每日总结邮件发送失败: {send_result.get('error', '')}")

            results["steps"].append({
                "step": 3,
                "status": "success" if send_result.get("success") else "failed",
                "description": "每日总结邮件发送完成",
                "result": send_result
            })

            # 步骤4: 创建次日计划
            logger.info("步骤4: 创建次日计划...")
            next_day = work_date + timedelta(days=1)

            # 简化处理，复用今日任务
            tomorrow_tasks = tasks if 'tasks' in locals() else [
                {
                    "task_id": 1,
                    "description": "执行客户搜索工作流",
                    "category": "客户开发",
                    "priority": "high",
                    "estimated_time": "2小时",
                    "responsible": "工作流系统"
                }
            ]

            tomorrow_priorities = {
                "high": ["执行客户搜索工作流", "发送开发邮件20封"],
                "medium": ["检查邮箱回复并跟进"]
            }

            tomorrow_outcomes = [
                "成功搜索到20-30个潜在客户",
                "成功发送20封开发邮件",
                "及时跟进所有客户回复"
            ]

            self.daily_planner.create_next_day_plan(
                plan_date=next_day,
                market=market,
                tasks=tomorrow_tasks,
                priorities=tomorrow_priorities,
                expected_outcomes=tomorrow_outcomes
            )
            logger.info("✅ 次日计划已创建")
            results["steps"].append({"step": 4, "status": "completed", "description": "次日计划创建完成"})

            logger.info(f"✅ 每日工作流执行完成 - {work_date}")

            return {
                "success": True,
                "workflow_type": "daily",
                "date": work_date.isoformat(),
                "market": market,
                "steps": results["steps"],
                "daily_report": daily_report
            }

        except Exception as e:
            logger.error(f"❌ 每日工作流执行失败: {e}")
            return {
                "success": False,
                "workflow_type": "daily",
                "date": work_date.isoformat(),
                "market": market,
                "error": str(e)
            }

    def run_weekly_workflow(self, start_date: date = None, market: str = "USA") -> Dict:
        """运行周度工作流"""
        if start_date is None:
            # 计算本周开始日期（假设周一开始）
            today = date.today()
            start_date = today - timedelta(days=today.weekday())

        logger.info(f"开始执行周度工作流 - {start_date} - {market}")

        results = {
            "week_start": start_date.isoformat(),
            "week_end": (start_date + timedelta(days=6)).isoformat(),
            "market": market
        }

        try:
            # 生成周度报告
            logger.info("生成周度报告...")
            weekly_report = self.report_generator.generate_weekly_report(start_date, market)
            logger.info("✅ 周度报告已生成")

            # 发送周度总结邮件
            logger.info("发送周度总结邮件...")
            send_result = self.summary_sender.send_weekly_summary(weekly_report)

            if send_result.get("success"):
                logger.info(f"✅ 周度总结邮件已发送，消息ID: {send_result.get('message_id', '')}")
            else:
                logger.error(f"❌ 周度总结邮件发送失败: {send_result.get('error', '')}")

            logger.info(f"✅ 周度工作流执行完成 - {start_date}")

            return {
                "success": True,
                "workflow_type": "weekly",
                "week_start": start_date.isoformat(),
                "week_end": (start_date + timedelta(days=6)).isoformat(),
                "market": market,
                "weekly_report": weekly_report,
                "send_result": send_result
            }

        except Exception as e:
            logger.error(f"❌ 周度工作流执行失败: {e}")
            return {
                "success": False,
                "workflow_type": "weekly",
                "error": str(e)
            }

    def run_monthly_workflow(self, year: int = None, month: int = None, market: str = "USA") -> Dict:
        """运行月度工作流"""
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month

        logger.info(f"开始执行月度工作流 - {year}-{month:02d} - {market}")

        try:
            # 生成月度报告
            logger.info("生成月度报告...")
            monthly_report = self.report_generator.generate_monthly_report(year, month, market)
            logger.info("✅ 月度报告已生成")

            # 发送月度总结邮件
            logger.info("发送月度总结邮件...")
            send_result = self.summary_sender.send_monthly_summary(monthly_report)

            if send_result.get("success"):
                logger.info(f"✅ 月度总结邮件已发送，消息ID: {send_result.get('message_id', '')}")
            else:
                logger.error(f"❌ 月度总结邮件发送失败: {send_result.get('error', '')}")

            # 进行目标调整分析
            logger.info("进行目标调整分析...")
            adjustment_report = self.goal_adjuster.generate_adjustment_report(year, month, market)
            logger.info("✅ 目标调整分析完成")

            # 保存调整记录
            record_id = self.goal_adjuster.save_adjustment_record(adjustment_report)
            logger.info(f"✅ 调整记录已保存，ID: {record_id}")

            # 如果需要调整，发送调整通知
            if adjustment_report.get("adjustment_analysis", {}).get("adjustment_needed"):
                logger.info("发送目标调整通知...")
                adjustment_result = self.goal_adjuster.adjust_next_month_goals(year, month, market)
                logger.info(f"✅ 下月目标已调整")

                send_adjustment_result = self.summary_sender.send_goal_adjustment_notification(
                    adjustment_report
                )
                logger.info("✅ 目标调整通知已发送")
            else:
                logger.info("目标调整不需要，跳过调整步骤")
                send_adjustment_result = {"skipped": True}

            logger.info(f"✅ 月度工作流执行完成 - {year}-{month:02d}")

            return {
                "success": True,
                "workflow_type": "monthly",
                "year": year,
                "month": month,
                "market": market,
                "monthly_report": monthly_report,
                "adjustment_report": adjustment_report,
                "monthly_send_result": send_result,
                "adjustment_send_result": send_adjustment_result
            }

        except Exception as e:
            logger.error(f"❌ 月度工作流执行失败: {e}")
            return {
                "success": False,
                "workflow_type": "monthly",
                "error": str(e)
            }

    def run_annual_workflow(self, year: int = None) -> Dict:
        """运行年度工作流"""
        if year is None:
            year = date.today().year

        logger.info(f"开始执行年度工作流 - {year}")

        try:
            # 生成年度报告
            logger.info("生成年度报告...")
            annual_report = self.report_generator.generate_annual_report(year)
            logger.info("✅ 年度报告已生成")

            # 发送年度总结邮件
            logger.info("发送年度总结邮件...")
            send_result = self.summary_sender.send_annual_summary(annual_report)

            if send_result.get("success"):
                logger.info(f"✅ 年度总结邮件已发送，消息ID: {send_result.get('message_id', '')}")
            else:
                logger.error(f"❌ 年度总结邮件发送失败: {send_result.get('error', '')}")

            logger.info(f"✅ 年度工作流执行完成 - {year}")

            return {
                "success": True,
                "workflow_type": "annual",
                "year": year,
                "annual_report": annual_report,
                "send_result": send_result
            }

        except Exception as e:
            logger.error(f"❌ 年度工作流执行失败: {e}")
            return {
                "success": False,
                "workflow_type": "annual",
                "error": str(e)
            }

    def run_full_workflow(self) -> Dict:
        """运行完整工作流（初始化 + 每日/周度/月度/年度）"""
        logger.info("开始执行完整工作流...")

        # 初始化系统
        init_result = self.initialize_system()

        if not init_result["success"]:
            logger.error("系统初始化失败，终止工作流")
            return {
                "success": False,
                "error": "系统初始化失败",
                "init_result": init_result
            }

        # 运行每日工作流
        daily_result = self.run_daily_workflow()

        # 根据日期决定是否运行周度/月度/年度工作流
        today = date.today()

        results = {
            "init_result": init_result,
            "daily_result": daily_result,
            "weekly_result": None,
            "monthly_result": None,
            "annual_result": None
        }

        # 如果是周日，运行周度工作流
        if today.weekday() == 6:  # 周日
            logger.info("今天是周日，执行周度工作流")
            week_start = today - timedelta(days=6)
            results["weekly_result"] = self.run_weekly_workflow(week_start)

        # 如果是月末，运行月度工作流
        tomorrow = today + timedelta(days=1)
        if tomorrow.month != today.month:
            logger.info("今天是月末，执行月度工作流")
            results["monthly_result"] = self.run_monthly_workflow(today.year, today.month)

        # 如果是年末，运行年度工作流
        if tomorrow.year != today.year:
            logger.info("今天是年末，执行年度工作流")
            results["annual_result"] = self.run_annual_workflow(today.year)

        logger.info("✅ 完整工作流执行完成")

        return {
            "success": True,
            "executed_at": datetime.now().isoformat(),
            "results": results
        }

if __name__ == "__main__":
    # 测试工作流编排器
    orchestrator = WorkflowOrchestrator()

    print("=" * 80)
    print("MIGA 自动化工作流测试")
    print("=" * 80)

    # 运行完整工作流
    print("\n开始执行完整工作流...")
    result = orchestrator.run_full_workflow()

    if result["success"]:
        print("\n✅ 工作流执行成功！")
        print(f"\n执行时间: {result['executed_at']}")

        results = result["results"]

        print("\n📊 各模块执行结果:")
        print(f"  系统初始化: {'✅' if results['init_result']['success'] else '❌'}")
        print(f"  每日工作流: {'✅' if results['daily_result']['success'] else '❌'}")

        if results.get("weekly_result"):
            print(f"  周度工作流: {'✅' if results['weekly_result']['success'] else '❌'}")

        if results.get("monthly_result"):
            print(f"  月度工作流: {'✅' if results['monthly_result']['success'] else '❌'}")

        if results.get("annual_result"):
            print(f"  年度工作流: {'✅' if results['annual_result']['success'] else '❌'}")
    else:
        print("\n❌ 工作流执行失败！")
        print(f"错误: {result.get('error', '')}")

    print("\n" + "=" * 80)
