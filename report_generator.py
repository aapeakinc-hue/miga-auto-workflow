#!/usr/bin/env python3
"""
报告生成系统
功能：生成日、周、月、年度总结报告
"""
import json
from typing import Dict, List
from datetime import datetime, date, timedelta
import sqlite3

class ReportGenerator:
    """报告生成器"""

    def __init__(self, daily_planner_db: str = "daily_planner.db",
                 goals_db: str = "goals.db",
                 crm_db: str = "miga_crm.db"):
        self.daily_planner_db = daily_planner_db
        self.goals_db = goals_db
        self.crm_db = crm_db

    def generate_daily_report(self, report_date: date, market: str) -> Dict:
        """生成每日报告"""
        from daily_planner import DailyPlanner

        planner = DailyPlanner(self.daily_planner_db)

        # 获取每日总结
        daily_summary = planner.generate_daily_summary(report_date, market)

        # 获取CRM数据
        crm_stats = self._get_crm_stats(report_date, market)

        # 计算当日指标
        metrics = self._calculate_daily_metrics(daily_summary, crm_stats)

        # 生成报告
        report = {
            "report_type": "daily",
            "report_date": report_date.isoformat(),
            "market": market,
            "summary": daily_summary,
            "crm_stats": crm_stats,
            "metrics": metrics,
            "highlights": self._generate_daily_highlights(metrics),
            "issues": self._identify_daily_issues(metrics),
            "action_items": self._generate_daily_action_items(metrics)
        }

        return report

    def generate_weekly_report(self, start_date: date, market: str) -> Dict:
        """生成周度报告"""
        from daily_planner import DailyPlanner

        planner = DailyPlanner(self.daily_planner_db)

        # 获取周内每日数据
        daily_reports = []
        weekdays = [start_date + timedelta(days=i) for i in range(7)]

        for day in weekdays:
            daily_report = self.generate_daily_report(day, market)
            daily_reports.append(daily_report)

        # 汇总周度数据
        weekly_metrics = self._aggregate_weekly_metrics(daily_reports)

        # 获取周度目标达成情况
        weekly_goal_achievement = self._check_weekly_goal_achievement(
            start_date, market, weekly_metrics
        )

        # 生成报告
        report = {
            "report_type": "weekly",
            "week_start": start_date.isoformat(),
            "week_end": (start_date + timedelta(days=6)).isoformat(),
            "market": market,
            "daily_reports": daily_reports,
            "weekly_metrics": weekly_metrics,
            "goal_achievement": weekly_goal_achievement,
            "highlights": self._generate_weekly_highlights(weekly_metrics, daily_reports),
            "issues": self._identify_weekly_issues(weekly_metrics, daily_reports),
            "recommendations": self._generate_weekly_recommendations(
                weekly_metrics, weekly_goal_achievement
            )
        }

        return report

    def generate_monthly_report(self, year: int, month: int, market: str) -> Dict:
        """生成月度报告"""
        from goal_setting import GoalSetting

        # 获取月内每日数据
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        daily_reports = []
        current_date = start_date

        while current_date <= end_date:
            try:
                daily_report = self.generate_daily_report(current_date, market)
                daily_reports.append(daily_report)
            except:
                pass
            current_date += timedelta(days=1)

        # 汇总月度数据
        monthly_metrics = self._aggregate_monthly_metrics(daily_reports)

        # 获取月度目标
        goal_system = GoalSetting(self.goals_db)
        monthly_goal = goal_system.get_monthly_goal(year, month, market)

        # 计算目标达成率
        goal_achievement = self._calculate_monthly_goal_achievement(
            monthly_goal, monthly_metrics
        )

        # 生成报告
        report = {
            "report_type": "monthly",
            "year": year,
            "month": month,
            "market": market,
            "monthly_goal": monthly_goal,
            "monthly_metrics": monthly_metrics,
            "goal_achievement": goal_achievement,
            "trend_analysis": self._analyze_trends(daily_reports),
            "highlights": self._generate_monthly_highlights(monthly_metrics, goal_achievement),
            "issues": self._identify_monthly_issues(monthly_metrics, goal_achievement),
            "recommendations": self._generate_monthly_recommendations(
                monthly_metrics, goal_achievement
            )
        }

        return report

    def generate_annual_report(self, year: int) -> Dict:
        """生成年度报告"""
        from goal_setting import GoalSetting

        markets = ["USA", "UK", "Germany", "UAE", "Japan"]
        goal_system = GoalSetting(self.goals_db)

        # 获取各市场年度目标
        annual_goals = {}
        for market in markets:
            goal = goal_system.get_annual_goal(year, market)
            if "error" not in goal:
                annual_goals[market] = goal

        # 汇总年度数据
        annual_metrics = {}
        for market in markets:
            # 汇总月度数据
            monthly_reports = []
            for month in range(1, 13):
                try:
                    monthly_report = self.generate_monthly_report(year, month, market)
                    monthly_reports.append(monthly_report)
                except:
                    pass

            annual_metrics[market] = self._aggregate_annual_metrics(monthly_reports)

        # 计算年度目标达成率
        annual_achievement = {}
        for market, goal in annual_goals.items():
            metrics = annual_metrics.get(market, {})
            achievement = self._calculate_annual_goal_achievement(goal, metrics)
            annual_achievement[market] = achievement

        # 生成报告
        report = {
            "report_type": "annual",
            "year": year,
            "annual_goals": annual_goals,
            "annual_metrics": annual_metrics,
            "annual_achievement": annual_achievement,
            "market_comparison": self._compare_markets(annual_metrics),
            "highlights": self._generate_annual_highlights(annual_achievement),
            "issues": self._identify_annual_issues(annual_achievement),
            "recommendations": self._generate_annual_recommendations(
                annual_achievement, annual_metrics
            )
        }

        return report

    def _get_crm_stats(self, report_date: date, market: str) -> Dict:
        """获取CRM统计数据"""
        try:
            conn = sqlite3.connect(self.crm_db)
            cursor = conn.cursor()

            # 获取当日新增客户
            cursor.execute("""
                SELECT COUNT(*) FROM customers
                WHERE created_at LIKE ?
            """, (f"{report_date.isoformat()}%",))

            new_customers = cursor.fetchone()[0]

            # 获取当日互动次数
            cursor.execute("""
                SELECT COUNT(*) FROM interactions
                WHERE created_at LIKE ?
            """, (f"{report_date.isoformat()}%",))

            interactions = cursor.fetchone()[0]

            conn.close()

            return {
                "new_customers": new_customers,
                "interactions": interactions
            }
        except:
            return {
                "new_customers": 0,
                "interactions": 0
            }

    def _calculate_daily_metrics(self, summary: Dict, crm_stats: Dict) -> Dict:
        """计算每日指标"""
        metrics = {
            "tasks_total": 0,
            "tasks_completed": 0,
            "completion_rate": 0,
            "emails_sent": 0,
            "new_customers": crm_stats.get("new_customers", 0),
            "interactions": crm_stats.get("interactions", 0)
        }

        if "error" not in summary.get("daily_plan", {}):
            metrics["tasks_total"] = len(summary["daily_plan"]["tasks"])

        if "error" not in summary.get("daily_execution", {}):
            metrics["tasks_completed"] = len(summary["daily_execution"]["tasks_completed"])

        if metrics["tasks_total"] > 0:
            metrics["completion_rate"] = (metrics["tasks_completed"] / metrics["tasks_total"]) * 100

        # 从执行记录中提取邮件发送数
        if "error" not in summary.get("daily_execution", {}):
            execution_metrics = summary["daily_execution"].get("metrics", {})
            metrics["emails_sent"] = execution_metrics.get("emails_sent", 0)

        return metrics

    def _aggregate_weekly_metrics(self, daily_reports: List[Dict]) -> Dict:
        """汇总周度指标"""
        weekly_metrics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "total_emails_sent": 0,
            "total_new_customers": 0,
            "total_interactions": 0,
            "avg_completion_rate": 0,
            "avg_emails_per_day": 0
        }

        valid_days = 0

        for daily_report in daily_reports:
            metrics = daily_report.get("metrics", {})
            weekly_metrics["total_tasks"] += metrics.get("tasks_total", 0)
            weekly_metrics["completed_tasks"] += metrics.get("tasks_completed", 0)
            weekly_metrics["total_emails_sent"] += metrics.get("emails_sent", 0)
            weekly_metrics["total_new_customers"] += metrics.get("new_customers", 0)
            weekly_metrics["total_interactions"] += metrics.get("interactions", 0)

            if metrics.get("tasks_total", 0) > 0:
                weekly_metrics["avg_completion_rate"] += metrics.get("completion_rate", 0)
                valid_days += 1

        if valid_days > 0:
            weekly_metrics["avg_completion_rate"] /= valid_days

        if valid_days > 0:
            weekly_metrics["avg_emails_per_day"] = weekly_metrics["total_emails_sent"] / valid_days

        return weekly_metrics

    def _aggregate_monthly_metrics(self, daily_reports: List[Dict]) -> Dict:
        """汇总月度指标"""
        monthly_metrics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "total_emails_sent": 0,
            "total_new_customers": 0,
            "total_interactions": 0,
            "avg_completion_rate": 0,
            "avg_emails_per_day": 0
        }

        valid_days = 0

        for daily_report in daily_reports:
            metrics = daily_report.get("metrics", {})
            monthly_metrics["total_tasks"] += metrics.get("tasks_total", 0)
            monthly_metrics["completed_tasks"] += metrics.get("tasks_completed", 0)
            monthly_metrics["total_emails_sent"] += metrics.get("emails_sent", 0)
            monthly_metrics["total_new_customers"] += metrics.get("new_customers", 0)
            monthly_metrics["total_interactions"] += metrics.get("interactions", 0)

            if metrics.get("tasks_total", 0) > 0:
                monthly_metrics["avg_completion_rate"] += metrics.get("completion_rate", 0)
                valid_days += 1

        if valid_days > 0:
            monthly_metrics["avg_completion_rate"] /= valid_days
            monthly_metrics["avg_emails_per_day"] = monthly_metrics["total_emails_sent"] / valid_days

        return monthly_metrics

    def _aggregate_annual_metrics(self, monthly_reports: List[Dict]) -> Dict:
        """汇总年度指标"""
        annual_metrics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "total_emails_sent": 0,
            "total_new_customers": 0,
            "total_interactions": 0,
            "avg_completion_rate": 0,
            "avg_emails_per_month": 0
        }

        valid_months = 0

        for monthly_report in monthly_reports:
            metrics = monthly_report.get("monthly_metrics", {})
            annual_metrics["total_tasks"] += metrics.get("total_tasks", 0)
            annual_metrics["completed_tasks"] += metrics.get("completed_tasks", 0)
            annual_metrics["total_emails_sent"] += metrics.get("total_emails_sent", 0)
            annual_metrics["total_new_customers"] += metrics.get("new_customers", 0)
            annual_metrics["total_interactions"] += metrics.get("interactions", 0)

            if metrics.get("total_tasks", 0) > 0:
                annual_metrics["avg_completion_rate"] += metrics.get("avg_completion_rate", 0)
                valid_months += 1

        if valid_months > 0:
            annual_metrics["avg_completion_rate"] /= valid_months
            annual_metrics["avg_emails_per_month"] = annual_metrics["total_emails_sent"] / valid_months

        return annual_metrics

    def _generate_daily_highlights(self, metrics: Dict) -> List[str]:
        """生成每日亮点"""
        highlights = []

        if metrics.get("emails_sent", 0) >= 20:
            highlights.append(f"✓ 今日发送邮件 {metrics['emails_sent']} 封，达到目标")
        if metrics.get("new_customers", 0) >= 5:
            highlights.append(f"✓ 新增客户 {metrics['new_customers']} 个，表现优秀")
        if metrics.get("completion_rate", 0) >= 90:
            highlights.append(f"✓ 任务完成率 {metrics['completion_rate']:.1f}%，效率高")

        return highlights

    def _identify_daily_issues(self, metrics: Dict) -> List[str]:
        """识别每日问题"""
        issues = []

        if metrics.get("emails_sent", 0) < 10:
            issues.append(f"⚠️ 今日仅发送 {metrics['emails_sent']} 封邮件，未达到目标")
        if metrics.get("completion_rate", 0) < 70:
            issues.append(f"⚠️ 任务完成率仅 {metrics['completion_rate']:.1f}%，需要提高效率")

        return issues

    def _generate_daily_action_items(self, metrics: Dict) -> List[str]:
        """生成每日行动项"""
        action_items = []

        if metrics.get("emails_sent", 0) < 20:
            action_items.append("明日计划发送25封邮件以弥补今日不足")
        if metrics.get("completion_rate", 0) < 80:
            action_items.append("优化工作流程，提高任务完成率")

        return action_items

    def _check_weekly_goal_achievement(self, start_date: date, market: str,
                                      weekly_metrics: Dict) -> Dict:
        """检查周度目标达成情况"""
        # 简化处理，假设周度目标是月度目标的1/4
        year = start_date.year
        month = start_date.month

        from goal_setting import GoalSetting
        goal_system = GoalSetting(self.goals_db)

        monthly_goal = goal_system.get_monthly_goal(year, month, market)

        if "error" in monthly_goal:
            return {"error": "Monthly goal not found"}

        # 计算周度目标（简化）
        weekly_goal = {
            "customer_development_goal": monthly_goal["customer_development_goal"] // 4,
            "intention_customer_goal": monthly_goal["intention_customer_goal"] // 4,
            "deal_customer_goal": monthly_goal["deal_customer_goal"] // 4,
            "revenue_goal": monthly_goal["revenue_goal"] // 4
        }

        # 计算达成率
        achievement = {
            "customer_development": (weekly_metrics.get("total_new_customers", 0) /
                                    weekly_goal["customer_development_goal"] * 100)
                                   if weekly_goal["customer_development_goal"] > 0 else 0,
            "emails_sent": (weekly_metrics.get("total_emails_sent", 0) /
                          (weekly_goal["customer_development_goal"] * 4) * 100)
                          if weekly_goal["customer_development_goal"] > 0 else 0
        }

        return {
            "weekly_goal": weekly_goal,
            "achievement": achievement
        }

    def _calculate_monthly_goal_achievement(self, monthly_goal: Dict,
                                           monthly_metrics: Dict) -> Dict:
        """计算月度目标达成率"""
        achievement = {}

        if "error" in monthly_goal:
            return {"error": "Monthly goal not found"}

        # 客户开发目标达成率
        if monthly_goal.get("customer_development_goal", 0) > 0:
            achievement["customer_development"] = (
                monthly_metrics.get("total_new_customers", 0) /
                monthly_goal["customer_development_goal"] * 100
            )

        # 意向客户目标达成率（简化计算）
        if monthly_goal.get("intention_customer_goal", 0) > 0:
            achievement["intention_customer"] = (
                monthly_metrics.get("total_new_customers", 0) *
                0.1 / monthly_goal["intention_customer_goal"] * 100
            )

        # 成交客户目标达成率（简化计算）
        if monthly_goal.get("deal_customer_goal", 0) > 0:
            achievement["deal_customer"] = (
                monthly_metrics.get("total_new_customers", 0) *
                0.02 / monthly_goal["deal_customer_goal"] * 100
            )

        return achievement

    def _calculate_annual_goal_achievement(self, annual_goal: Dict,
                                         annual_metrics: Dict) -> Dict:
        """计算年度目标达成率"""
        achievement = {}

        if "error" in annual_goal:
            return {"error": "Annual goal not found"}

        # 客户开发目标达成率
        if annual_goal.get("customer_development_goal", 0) > 0:
            achievement["customer_development"] = (
                annual_metrics.get("total_new_customers", 0) /
                annual_goal["customer_development_goal"] * 100
            )

        # 意向客户目标达成率
        if annual_goal.get("intention_customer_goal", 0) > 0:
            achievement["intention_customer"] = (
                annual_metrics.get("total_new_customers", 0) *
                0.1 / annual_goal["intention_customer_goal"] * 100
            )

        # 成交客户目标达成率
        if annual_goal.get("deal_customer_goal", 0) > 0:
            achievement["deal_customer"] = (
                annual_metrics.get("total_new_customers", 0) *
                0.02 / annual_goal["deal_customer_goal"] * 100
            )

        return achievement

    def _generate_weekly_highlights(self, weekly_metrics: Dict,
                                   daily_reports: List[Dict]) -> List[str]:
        """生成周度亮点"""
        highlights = []

        if weekly_metrics.get("total_emails_sent", 0) >= 100:
            highlights.append(f"✓ 本周发送邮件 {weekly_metrics['total_emails_sent']} 封，表现优秀")
        if weekly_metrics.get("total_new_customers", 0) >= 20:
            highlights.append(f"✓ 本周新增客户 {weekly_metrics['total_new_customers']} 个")
        if weekly_metrics.get("avg_completion_rate", 0) >= 85:
            highlights.append(f"✓ 平均任务完成率 {weekly_metrics['avg_completion_rate']:.1f}%")

        return highlights

    def _identify_weekly_issues(self, weekly_metrics: Dict,
                               daily_reports: List[Dict]) -> List[str]:
        """识别周度问题"""
        issues = []

        if weekly_metrics.get("total_emails_sent", 0) < 80:
            issues.append(f"⚠️ 本周仅发送 {weekly_metrics['total_emails_sent']} 封邮件，未达标")
        if weekly_metrics.get("avg_completion_rate", 0) < 75:
            issues.append(f"⚠️ 平均完成率 {weekly_metrics['avg_completion_rate']:.1f}%，需改进")

        return issues

    def _generate_weekly_recommendations(self, weekly_metrics: Dict,
                                       weekly_goal_achievement: Dict) -> List[str]:
        """生成周度建议"""
        recommendations = []

        if weekly_metrics.get("avg_completion_rate", 0) < 80:
            recommendations.append("建议优化工作流程，提高任务完成率")
        if weekly_metrics.get("total_emails_sent", 0) < 100:
            recommendations.append("建议增加每日邮件发送量，确保周度目标达成")

        return recommendations

    def _analyze_trends(self, daily_reports: List[Dict]) -> Dict:
        """分析趋势"""
        if len(daily_reports) < 2:
            return {"error": "Insufficient data for trend analysis"}

        # 简化趋势分析
        first_week_emails = sum([d.get("metrics", {}).get("emails_sent", 0)
                               for d in daily_reports[:min(7, len(daily_reports))]])
        last_week_emails = sum([d.get("metrics", {}).get("emails_sent", 0)
                              for d in daily_reports[-min(7, len(daily_reports)):]])

        trend = "stable"
        if last_week_emails > first_week_emails * 1.2:
            trend = "increasing"
        elif last_week_emails < first_week_emails * 0.8:
            trend = "decreasing"

        return {
            "email_trend": trend,
            "first_week_emails": first_week_emails,
            "last_week_emails": last_week_emails
        }

    def _generate_monthly_highlights(self, monthly_metrics: Dict,
                                    goal_achievement: Dict) -> List[str]:
        """生成月度亮点"""
        highlights = []

        if monthly_metrics.get("total_emails_sent", 0) >= 400:
            highlights.append(f"✓ 本月发送邮件 {monthly_metrics['total_emails_sent']} 封")
        if monthly_metrics.get("total_new_customers", 0) >= 80:
            highlights.append(f"✓ 本月新增客户 {monthly_metrics['total_new_customers']} 个")

        return highlights

    def _identify_monthly_issues(self, monthly_metrics: Dict,
                                goal_achievement: Dict) -> List[str]:
        """识别月度问题"""
        issues = []

        for metric, rate in goal_achievement.items():
            if rate < 80:
                issues.append(f"⚠️ {metric} 目标达成率仅 {rate:.1f}%，需要改进")

        return issues

    def _generate_monthly_recommendations(self, monthly_metrics: Dict,
                                        goal_achievement: Dict) -> List[str]:
        """生成月度建议"""
        recommendations = []

        # 基于达成率的建议
        low_achievement = [m for m, r in goal_achievement.items() if r < 80]
        if low_achievement:
            recommendations.append(f"重点关注未达标的指标: {', '.join(low_achievement)}")

        return recommendations

    def _compare_markets(self, annual_metrics: Dict) -> Dict:
        """比较各市场表现"""
        comparison = {}

        for market, metrics in annual_metrics.items():
            comparison[market] = {
                "emails_sent": metrics.get("total_emails_sent", 0),
                "new_customers": metrics.get("total_new_customers", 0),
                "rank": 0  # 简化处理
            }

        return comparison

    def _generate_annual_highlights(self, annual_achievement: Dict) -> List[str]:
        """生成年度亮点"""
        highlights = []

        # 找出表现最好的市场
        best_market = None
        best_rate = 0

        for market, achievement in annual_achievement.items():
            if "customer_development" in achievement:
                if achievement["customer_development"] > best_rate:
                    best_rate = achievement["customer_development"]
                    best_market = market

        if best_market:
            highlights.append(f"✓ {best_market} 市场表现最佳，达成率 {best_rate:.1f}%")

        return highlights

    def _identify_annual_issues(self, annual_achievement: Dict) -> List[str]:
        """识别年度问题"""
        issues = []

        for market, achievement in annual_achievement.items():
            for metric, rate in achievement.items():
                if rate < 50:
                    issues.append(f"⚠️ {market} 市场 {metric} 达成率仅 {rate:.1f}%")

        return issues

    def _generate_annual_recommendations(self, annual_achievement: Dict,
                                        annual_metrics: Dict) -> List[str]:
        """生成年度建议"""
        recommendations = []

        # 找出需要改进的市场
        poor_markets = []
        for market, achievement in annual_achievement.items():
            avg_rate = sum([r for r in achievement.values() if isinstance(r, (int, float))]) / len(achievement)
            if avg_rate < 70:
                poor_markets.append(market)

        if poor_markets:
            recommendations.append(f"重点关注并改进以下市场: {', '.join(poor_markets)}")

        return recommendations

if __name__ == "__main__":
    # 测试报告生成
    from datetime import date

    generator = ReportGenerator()

    # 生成每日报告
    today = date.today()
    daily_report = generator.generate_daily_report(today, "USA")

    print("=" * 80)
    print("每日报告示例")
    print("=" * 80)
    print(f"日期: {daily_report['report_date']}")
    print(f"市场: {daily_report['market']}")
    print(f"\n指标:")
    for key, value in daily_report['metrics'].items():
        print(f"  {key}: {value}")
    print(f"\n亮点:")
    for highlight in daily_report['highlights']:
        print(f"  {highlight}")
    print("\n" + "=" * 80)
