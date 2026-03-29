#!/usr/bin/env python3
"""
目标设定系统
功能：基于市场数据设定月度和年度目标
"""
import json
from typing import Dict, List
from datetime import datetime, timedelta
import sqlite3

class GoalSetting:
    """目标设定与管理"""

    def __init__(self, db_path: str = "goals.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化目标数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建年度目标表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS annual_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                market TEXT NOT NULL,
                customer_development_goal INTEGER,
                intention_customer_goal INTEGER,
                deal_customer_goal INTEGER,
                revenue_goal REAL,
                revenue_unit TEXT DEFAULT 'USD',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(year, market)
            )
        """)

        # 创建月度目标表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monthly_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                market TEXT NOT NULL,
                customer_development_goal INTEGER,
                intention_customer_goal INTEGER,
                deal_customer_goal INTEGER,
                revenue_goal REAL,
                revenue_unit TEXT DEFAULT 'USD',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(year, month, market)
            )
        """)

        # 创建目标达成记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goal_achievement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_type TEXT NOT NULL,
                goal_id INTEGER NOT NULL,
                year INTEGER,
                month INTEGER,
                metric_name TEXT NOT NULL,
                target_value REAL,
                actual_value REAL,
                achievement_rate REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def set_annual_goal(self, year: int, market: str,
                       customer_development_goal: int,
                       intention_customer_goal: int,
                       deal_customer_goal: int,
                       revenue_goal: float,
                       revenue_unit: str = "USD") -> int:
        """设定年度目标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO annual_goals
            (year, market, customer_development_goal, intention_customer_goal,
             deal_customer_goal, revenue_goal, revenue_unit, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (year, market, customer_development_goal, intention_customer_goal,
              deal_customer_goal, revenue_goal, revenue_unit, datetime.now()))

        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return goal_id

    def set_monthly_goal(self, year: int, month: int, market: str,
                        customer_development_goal: int,
                        intention_customer_goal: int,
                        deal_customer_goal: int,
                        revenue_goal: float,
                        revenue_unit: str = "USD") -> int:
        """设定月度目标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO monthly_goals
            (year, month, market, customer_development_goal, intention_customer_goal,
             deal_customer_goal, revenue_goal, revenue_unit, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (year, month, market, customer_development_goal, intention_customer_goal,
              deal_customer_goal, revenue_goal, revenue_unit, datetime.now()))

        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return goal_id

    def calculate_monthly_goals_from_annual(self, year: int, market: str,
                                           monthly_weights: List[float] = None) -> Dict:
        """从年度目标分解月度目标"""
        # 获取年度目标
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_development_goal, intention_customer_goal,
                   deal_customer_goal, revenue_goal
            FROM annual_goals
            WHERE year = ? AND market = ?
        """, (year, market))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"error": "Annual goal not found"}

        annual_customer_dev, annual_intention, annual_deal, annual_revenue = result

        # 如果没有提供权重，使用默认权重（考虑季节性）
        if monthly_weights is None:
            # 水晶产品有季节性，Q4（10-12月）是旺季
            monthly_weights = [
                0.08,  # 1月
                0.07,  # 2月
                0.08,  # 3月
                0.08,  # 4月
                0.08,  # 5月
                0.08,  # 6月
                0.08,  # 7月
                0.08,  # 8月
                0.08,  # 9月
                0.10,  # 10月 - 旺季开始
                0.11,  # 11月 - 旺季高峰
                0.09   # 12月 - 旺季延续
            ]

        # 分解月度目标
        monthly_goals = {}
        for month in range(1, 13):
            weight = monthly_weights[month - 1]

            monthly_goals[month] = {
                "year": year,
                "month": month,
                "market": market,
                "customer_development_goal": int(annual_customer_dev * weight),
                "intention_customer_goal": int(annual_intention * weight),
                "deal_customer_goal": int(annual_deal * weight),
                "revenue_goal": annual_revenue * weight,
                "weight": weight,
                "reason": f"月度权重: {weight * 100:.1f}%"
            }

        return {
            "annual_summary": {
                "customer_development_goal": annual_customer_dev,
                "intention_customer_goal": annual_intention,
                "deal_customer_goal": annual_deal,
                "revenue_goal": annual_revenue
            },
            "monthly_breakdown": monthly_goals
        }

    def save_monthly_goals(self, monthly_goals: Dict) -> int:
        """保存月度目标到数据库"""
        saved_count = 0

        for month, goal_data in monthly_goals["monthly_breakdown"].items():
            goal_id = self.set_monthly_goal(
                year=goal_data["year"],
                month=goal_data["month"],
                market=goal_data["market"],
                customer_development_goal=goal_data["customer_development_goal"],
                intention_customer_goal=goal_data["intention_customer_goal"],
                deal_customer_goal=goal_data["deal_customer_goal"],
                revenue_goal=goal_data["revenue_goal"]
            )
            if goal_id > 0:
                saved_count += 1

        return saved_count

    def get_annual_goal(self, year: int, market: str) -> Dict:
        """获取年度目标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_development_goal, intention_customer_goal,
                   deal_customer_goal, revenue_goal, revenue_unit
            FROM annual_goals
            WHERE year = ? AND market = ?
        """, (year, market))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"error": "Annual goal not found"}

        return {
            "year": year,
            "market": market,
            "customer_development_goal": result[0],
            "intention_customer_goal": result[1],
            "deal_customer_goal": result[2],
            "revenue_goal": result[3],
            "revenue_unit": result[4]
        }

    def get_monthly_goal(self, year: int, month: int, market: str) -> Dict:
        """获取月度目标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_development_goal, intention_customer_goal,
                   deal_customer_goal, revenue_goal, revenue_unit
            FROM monthly_goals
            WHERE year = ? AND month = ? AND market = ?
        """, (year, month, market))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"error": "Monthly goal not found"}

        return {
            "year": year,
            "month": month,
            "market": market,
            "customer_development_goal": result[0],
            "intention_customer_goal": result[1],
            "deal_customer_goal": result[2],
            "revenue_goal": result[3],
            "revenue_unit": result[4]
        }

    def generate_goals_based_on_market_data(self, market_report: Dict,
                                           target_market_share: float = 0.05) -> Dict:
        """基于市场数据生成目标"""
        country = market_report["country"]
        market_size = market_report["estimated_market_size"]
        growth_rate = market_report["growth_rate"]
        opportunity_level = market_report["opportunity_level"]

        # 基于市场规模和目标市场份额设定年度收入目标
        annual_revenue_goal = market_size * target_market_share

        # 根据机会等级调整目标
        if opportunity_level == "high":
            target_market_share = 0.08  # 高机会市场，目标8%市场份额
        elif opportunity_level == "medium":
            target_market_share = 0.05  # 中等机会市场，目标5%市场份额
        elif opportunity_level == "low":
            target_market_share = 0.02  # 低机会市场，目标2%市场份额
        else:
            target_market_share = 0.01  # 负增长市场，目标1%市场份额

        annual_revenue_goal = market_size * target_market_share

        # 基于收入目标计算客户目标
        avg_order_value = 2000  # 平均订单价值 $2000
        deal_customer_goal = int(annual_revenue_goal / avg_order_value)

        # 基于转化漏斗计算意向客户目标
        intention_to_deal_rate = 0.20  # 意向客户转化率 20%
        intention_customer_goal = int(deal_customer_goal / intention_to_deal_rate)

        # 基于意向客户率计算潜在客户目标
        intention_rate = 0.10  # 潜在客户意向率 10%
        customer_development_goal = int(intention_customer_goal / intention_rate)

        return {
            "country": country,
            "market_size": market_size,
            "target_market_share": target_market_share,
            "annual_goals": {
                "customer_development_goal": customer_development_goal,
                "intention_customer_goal": intention_customer_goal,
                "deal_customer_goal": deal_customer_goal,
                "revenue_goal": annual_revenue_goal
            },
            "assumptions": {
                "average_order_value": avg_order_value,
                "intention_to_deal_rate": intention_to_deal_rate,
                "intention_rate": intention_rate
            },
            "opportunity_adjustment": {
                "opportunity_level": opportunity_level,
                "growth_rate": growth_rate,
                "adjustment_reason": f"根据{opportunity_level}机会等级和{growth_rate}%增长率调整目标"
            }
        }

    def adjust_goals_based_on_achievement(self, year: int, month: int,
                                          market: str,
                                          actual_data: Dict) -> Dict:
        """基于达成度调整目标"""
        current_monthly_goal = self.get_monthly_goal(year, month, market)

        if "error" in current_monthly_goal:
            return {"error": "Cannot adjust goals: current goal not found"}

        # 计算达成率
        achievements = {}
        adjustments = {}

        for metric in ["customer_development", "intention_customer", "deal_customer"]:
            target = current_monthly_goal[f"{metric}_goal"]
            actual = actual_data.get(metric, 0)

            if target > 0:
                achievement_rate = (actual / target) * 100
                achievements[metric] = {
                    "target": target,
                    "actual": actual,
                    "achievement_rate": round(achievement_rate, 2)
                }

                # 调整下月目标
                if achievement_rate > 120:  # 超额完成20%以上
                    adjustment_factor = 1.15  # 提高15%
                    adjustment_reason = "超额完成，提高目标"
                elif achievement_rate < 80:  # 未完成80%
                    adjustment_factor = 0.85  # 降低15%
                    adjustment_reason = "未达标，降低目标以保持可行性"
                else:
                    adjustment_factor = 1.0  # 保持不变
                    adjustment_reason = "达成率在合理范围内，保持目标"

                adjustments[metric] = {
                    "adjustment_factor": adjustment_factor,
                    "adjustment_reason": adjustment_reason
                }
            else:
                achievements[metric] = {"error": "Target is zero"}
                adjustments[metric] = {"adjustment_factor": 1.0, "adjustment_reason": "无目标"}

        # 收入目标调整
        target_revenue = current_monthly_goal["revenue_goal"]
        actual_revenue = actual_data.get("revenue", 0)

        if target_revenue > 0:
            revenue_achievement_rate = (actual_revenue / target_revenue) * 100
            achievements["revenue"] = {
                "target": target_revenue,
                "actual": actual_revenue,
                "achievement_rate": round(revenue_achievement_rate, 2)
            }

            if revenue_achievement_rate > 120:
                revenue_adjustment_factor = 1.15
                revenue_adjustment_reason = "收入超额完成，提高目标"
            elif revenue_achievement_rate < 80:
                revenue_adjustment_factor = 0.85
                revenue_adjustment_reason = "收入未达标，降低目标"
            else:
                revenue_adjustment_factor = 1.0
                revenue_adjustment_reason = "收入达成率在合理范围内，保持目标"

            adjustments["revenue"] = {
                "adjustment_factor": revenue_adjustment_factor,
                "adjustment_reason": revenue_adjustment_reason
            }

        return {
            "year": year,
            "month": month,
            "market": market,
            "current_goals": current_monthly_goal,
            "actual_data": actual_data,
            "achievements": achievements,
            "adjustments": adjustments,
            "recommendation": self._generate_adjustment_recommendation(achievements)
        }

    def _generate_adjustment_recommendation(self, achievements: Dict) -> str:
        """生成调整建议"""
        avg_achievement = 0
        count = 0

        for metric, data in achievements.items():
            if "achievement_rate" in data:
                avg_achievement += data["achievement_rate"]
                count += 1

        if count == 0:
            return "无法生成建议：缺乏达成率数据"

        avg_achievement = avg_achievement / count

        if avg_achievement > 110:
            return "整体达成率优秀，建议适度提高目标，挑战更高目标"
        elif avg_achievement > 90:
            return "整体达成率良好，建议保持当前目标，稳步推进"
        elif avg_achievement > 70:
            return "整体达成率一般，建议保持或微调目标，重点关注薄弱环节"
        else:
            return "整体达成率较低，建议降低目标，分析原因并改进策略"

def initialize_sample_goals():
    """初始化示例目标"""
    goal = GoalSetting()

    # 2026年美国市场年度目标
    goal.set_annual_goal(
        year=2026,
        market="USA",
        customer_development_goal=500,
        intention_customer_goal=50,
        deal_customer_goal=10,
        revenue_goal=20000
    )

    # 2026年英国市场年度目标
    goal.set_annual_goal(
        year=2026,
        market="UK",
        customer_development_goal=300,
        intention_customer_goal=30,
        deal_customer_goal=6,
        revenue_goal=12000
    )

    # 2026年德国市场年度目标
    goal.set_annual_goal(
        year=2026,
        market="Germany",
        customer_development_goal=250,
        intention_customer_goal=25,
        deal_customer_goal=5,
        revenue_goal=10000
    )

    # 2026年阿联酋市场年度目标
    goal.set_annual_goal(
        year=2026,
        market="UAE",
        customer_development_goal=200,
        intention_customer_goal=20,
        deal_customer_goal=4,
        revenue_goal=8000
    )

    # 2026年日本市场年度目标
    goal.set_annual_goal(
        year=2026,
        market="Japan",
        customer_development_goal=150,
        intention_customer_goal=15,
        deal_customer_goal=3,
        revenue_goal=6000
    )

    # 为美国市场生成月度目标
    monthly_goals = goal.calculate_monthly_goals_from_annual(2026, "USA")
    goal.save_monthly_goals(monthly_goals)

    print("✅ 示例目标初始化完成")
    print("\n年度目标:")
    for market in ["USA", "UK", "Germany", "UAE", "Japan"]:
        annual_goal = goal.get_annual_goal(2026, market)
        if "error" not in annual_goal:
            print(f"\n{market} 2026年度目标:")
            print(f"  客户开发目标: {annual_goal['customer_development_goal']}")
            print(f"  意向客户目标: {annual_goal['intention_customer_goal']}")
            print(f"  成交客户目标: {annual_goal['deal_customer_goal']}")
            print(f"  收入目标: ${annual_goal['revenue_goal']:,.0f}")

if __name__ == "__main__":
    initialize_sample_goals()
