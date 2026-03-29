#!/usr/bin/env python3
"""
目标调整系统
功能：基于达成度进行不间断的目标调整
"""
import json
from typing import Dict, List
from datetime import datetime, date
import sqlite3

class GoalAdjuster:
    """目标调整器"""

    def __init__(self, goals_db: str = "goals.db",
                 daily_planner_db: str = "daily_planner.db"):
        self.goals_db = goals_db
        self.daily_planner_db = daily_planner_db

    def analyze_performance(self, year: int, month: int, market: str) -> Dict:
        """分析绩效"""
        from goal_setting import GoalSetting
        from report_generator import ReportGenerator

        goal_system = GoalSetting(self.goals_db)
        report_generator = ReportGenerator(self.daily_planner_db, self.goals_db)

        # 获取月度目标
        monthly_goal = goal_system.get_monthly_goal(year, month, market)

        if "error" in monthly_goal:
            return {"error": "Monthly goal not found"}

        # 生成月度报告
        try:
            monthly_report = report_generator.generate_monthly_report(year, month, market)
        except:
            # 如果没有足够的数据，返回简化版本
            monthly_report = {"error": "Insufficient data for report generation"}

        # 计算绩效指标
        performance = {
            "year": year,
            "month": month,
            "market": market,
            "monthly_goal": monthly_goal,
            "monthly_report": monthly_report
        }

        return performance

    def calculate_adjustment_factor(self, performance: Dict) -> Dict:
        """计算调整因子"""
        monthly_report = performance.get("monthly_report", {})

        if "error" in monthly_report:
            return {
                "adjustment_needed": False,
                "reason": "Insufficient data for adjustment"
            }

        goal_achievement = monthly_report.get("goal_achievement", {})

        # 计算平均达成率
        rates = [r for r in goal_achievement.values() if isinstance(r, (int, float))]
        avg_achievement = sum(rates) / len(rates) if rates else 0

        # 确定调整策略
        if avg_achievement > 120:
            adjustment_strategy = "increase"
            adjustment_factor = 1.15
            reason = f"平均达成率{avg_achievement:.1f}%，超额完成，建议提高15%"
        elif avg_achievement > 100:
            adjustment_strategy = "maintain"
            adjustment_factor = 1.0
            reason = f"平均达成率{avg_achievement:.1f}%，刚好完成，建议保持目标"
        elif avg_achievement > 80:
            adjustment_strategy = "maintain"
            adjustment_factor = 1.0
            reason = f"平均达成率{avg_achievement:.1f}%，基本达成，建议保持目标"
        elif avg_achievement > 60:
            adjustment_strategy = "decrease"
            adjustment_factor = 0.90
            reason = f"平均达成率{avg_achievement:.1f}%，部分未达标，建议降低10%"
        else:
            adjustment_strategy = "decrease"
            adjustment_factor = 0.80
            reason = f"平均达成率{avg_achievement:.1f}%，严重未达标，建议降低20%"

        return {
            "adjustment_needed": adjustment_strategy != "maintain",
            "adjustment_strategy": adjustment_strategy,
            "adjustment_factor": adjustment_factor,
            "avg_achievement": avg_achievement,
            "reason": reason
        }

    def adjust_next_month_goals(self, year: int, month: int, market: str) -> Dict:
        """调整下月目标"""
        from goal_setting import GoalSetting

        # 分析当前月度绩效
        performance = self.analyze_performance(year, month, market)

        if "error" in performance:
            return performance

        # 计算调整因子
        adjustment = self.calculate_adjustment_factor(performance)

        if not adjustment["adjustment_needed"]:
            return {
                "message": "No adjustment needed",
                "reason": adjustment["reason"]
            }

        # 获取当前月度目标
        goal_system = GoalSetting(self.goals_db)
        current_monthly_goal = goal_system.get_monthly_goal(year, month, market)

        if "error" in current_monthly_goal:
            return {"error": "Current monthly goal not found"}

        # 计算下月日期
        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1

        # 获取下月当前目标（如果存在）
        next_monthly_goal = goal_system.get_monthly_goal(next_year, next_month, market)

        if "error" in next_monthly_goal:
            # 如果下月目标不存在，使用当前目标作为基准
            base_goals = current_monthly_goal
        else:
            base_goals = next_monthly_goal

        # 应用调整因子
        adjustment_factor = adjustment["adjustment_factor"]
        adjusted_goals = {
            "customer_development_goal": int(
                base_goals["customer_development_goal"] * adjustment_factor
            ),
            "intention_customer_goal": int(
                base_goals["intention_customer_goal"] * adjustment_factor
            ),
            "deal_customer_goal": int(
                base_goals["deal_customer_goal"] * adjustment_factor
            ),
            "revenue_goal": base_goals["revenue_goal"] * adjustment_factor
        }

        # 更新下月目标
        goal_system.set_monthly_goal(
            year=next_year,
            month=next_month,
            market=market,
            customer_development_goal=adjusted_goals["customer_development_goal"],
            intention_customer_goal=adjusted_goals["intention_customer_goal"],
            deal_customer_goal=adjusted_goals["deal_customer_goal"],
            revenue_goal=adjusted_goals["revenue_goal"]
        )

        return {
            "adjustment_applied": True,
            "adjustment_factor": adjustment_factor,
            "adjustment_strategy": adjustment["adjustment_strategy"],
            "original_goals": base_goals,
            "adjusted_goals": adjusted_goals,
            "reason": adjustment["reason"]
        }

    def adjust_quarterly_goals(self, year: int, quarter: int, market: str) -> Dict:
        """调整季度目标"""
        # 季度包含的月份
        quarter_months = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12]
        }

        months = quarter_months.get(quarter, [])

        if not months:
            return {"error": "Invalid quarter"}

        # 分析季度内各月份的绩效
        quarterly_performance = []

        for month in months:
            performance = self.analyze_performance(year, month, market)
            quarterly_performance.append(performance)

        # 计算季度平均达成率
        all_rates = []
        for perf in quarterly_performance:
            if "error" not in perf.get("monthly_report", {}):
                goal_achievement = perf["monthly_report"].get("goal_achievement", {})
                rates = [r for r in goal_achievement.values() if isinstance(r, (int, float))]
                all_rates.extend(rates)

        if not all_rates:
            return {"error": "Insufficient data for quarterly adjustment"}

        avg_quarterly_achievement = sum(all_rates) / len(all_rates)

        # 确定调整策略
        if avg_quarterly_achievement > 115:
            adjustment_factor = 1.20
            adjustment_strategy = "increase"
            reason = f"季度平均达成率{avg_quarterly_achievement:.1f}%，超额完成，建议提高20%"
        elif avg_quarterly_achievement > 100:
            adjustment_factor = 1.10
            adjustment_strategy = "increase"
            reason = f"季度平均达成率{avg_quarterly_achievement:.1f}%，刚好完成，建议提高10%"
        elif avg_quarterly_achievement > 85:
            adjustment_factor = 1.0
            adjustment_strategy = "maintain"
            reason = f"季度平均达成率{avg_quarterly_achievement:.1f}%，基本达成，建议保持目标"
        elif avg_quarterly_achievement > 70:
            adjustment_factor = 0.90
            adjustment_strategy = "decrease"
            reason = f"季度平均达成率{avg_quarterly_achievement:.1f}%，部分未达标，建议降低10%"
        else:
            adjustment_factor = 0.80
            adjustment_strategy = "decrease"
            reason = f"季度平均达成率{avg_quarterly_achievement:.1f}%，严重未达标，建议降低20%"

        # 调整下一季度的目标
        next_quarter = quarter + 1 if quarter < 4 else 1
        next_quarter_year = year + 1 if quarter == 4 else year

        next_quarter_months = quarter_months.get(next_quarter, [])

        # 调整下一季度各个月份的目标
        adjusted_goals = {}

        for month in next_quarter_months:
            adjustment_result = self.adjust_next_month_goals(
                year if next_quarter_year == year else next_quarter_year - 1,
                month,
                market
            )

            if "adjustment_applied" in adjustment_result:
                adjusted_goals[month] = adjustment_result["adjusted_goals"]

        return {
            "quarterly_achievement": avg_quarterly_achievement,
            "adjustment_factor": adjustment_factor,
            "adjustment_strategy": adjustment_strategy,
            "reason": reason,
            "adjusted_goals": adjusted_goals
        }

    def generate_adjustment_report(self, year: int, month: int, market: str) -> Dict:
        """生成调整报告"""
        from goal_setting import GoalSetting

        # 分析绩效
        performance = self.analyze_performance(year, month, market)

        if "error" in performance:
            return performance

        # 计算调整因子
        adjustment = self.calculate_adjustment_factor(performance)

        # 生成详细报告
        report = {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "year": year,
            "month": month,
            "market": market,
            "performance_analysis": performance,
            "adjustment_analysis": adjustment,
            "recommendations": self._generate_adjustment_recommendations(performance, adjustment)
        }

        return report

    def _generate_adjustment_recommendations(self, performance: Dict,
                                           adjustment: Dict) -> List[str]:
        """生成调整建议"""
        recommendations = []

        monthly_report = performance.get("monthly_report", {})

        if "error" not in monthly_report:
            goal_achievement = monthly_report.get("goal_achievement", {})

            # 针对各个指标的建议
            for metric, rate in goal_achievement.items():
                if isinstance(rate, (int, float)):
                    if rate < 60:
                        recommendations.append(
                            f"🔴 {metric} 严重未达标（{rate:.1f}%），需要立即分析原因并改进策略"
                        )
                    elif rate < 80:
                        recommendations.append(
                            f"🟡 {metric} 未达标（{rate:.1f}%），需要优化执行流程"
                        )
                    elif rate > 120:
                        recommendations.append(
                            f"🟢 {metric} 超额完成（{rate:.1f}%），可以挑战更高目标"
                        )

        # 基于调整策略的建议
        if adjustment.get("adjustment_strategy") == "increase":
            recommendations.append(
                "💡 建议提高目标，团队表现出色，可以挑战更高目标"
            )
        elif adjustment.get("adjustment_strategy") == "decrease":
            recommendations.append(
                "💡 建议降低目标，确保目标的可达成性，同时分析未达标原因"
            )
        else:
            recommendations.append(
                "💡 建议保持当前目标，团队表现稳定，继续执行即可"
            )

        return recommendations

    def save_adjustment_record(self, adjustment_report: Dict) -> int:
        """保存调整记录"""
        conn = sqlite3.connect(self.goals_db)
        cursor = conn.cursor()

        # 创建调整记录表（如果不存在）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adjustment_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date TEXT NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                market TEXT NOT NULL,
                performance_data TEXT,
                adjustment_data TEXT,
                recommendations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 插入调整记录
        cursor.execute("""
            INSERT INTO adjustment_records
            (report_date, year, month, market, performance_data,
             adjustment_data, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            adjustment_report["report_date"],
            adjustment_report["year"],
            adjustment_report["month"],
            adjustment_report["market"],
            json.dumps(adjustment_report["performance_analysis"], ensure_ascii=False),
            json.dumps(adjustment_report["adjustment_analysis"], ensure_ascii=False),
            json.dumps(adjustation_report["recommendations"], ensure_ascii=False)
        ))

        record_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return record_id

if __name__ == "__main__":
    # 测试目标调整
    from datetime import date

    adjuster = GoalAdjuster()

    # 分析2026年3月美国市场的绩效
    year = 2026
    month = 3
    market = "USA"

    print("=" * 80)
    print("目标调整分析")
    print("=" * 80)

    # 生成调整报告
    adjustment_report = adjuster.generate_adjustment_report(year, month, market)

    print(f"\n📊 绩效分析:")
    print(f"  年份: {adjustment_report['year']}")
    print(f"  月份: {adjustment_report['month']}")
    print(f"  市场: {adjustment_report['market']}")

    if "error" not in adjustment_report.get("adjustment_analysis", {}):
        adjustment = adjustment_report["adjustment_analysis"]
        print(f"\n🔄 调整分析:")
        print(f"  是否需要调整: {'是' if adjustment['adjustment_needed'] else '否'}")
        print(f"  调整策略: {adjustment['adjustment_strategy']}")
        print(f"  调整因子: {adjustment['adjustment_factor']:.2f}")
        print(f"  平均达成率: {adjustment['avg_achievement']:.1f}%")
        print(f"  原因: {adjustment['reason']}")

    print(f"\n💡 建议:")
    for rec in adjustment_report.get("recommendations", []):
        print(f"  {rec}")

    # 保存调整记录
    record_id = adjuster.save_adjustment_record(adjustment_report)
    print(f"\n✅ 调整记录已保存，ID: {record_id}")

    print("\n" + "=" * 80)
