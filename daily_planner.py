#!/usr/bin/env python3
"""
每日计划与总结系统
功能：每日工作计划、执行记录、次日计划
"""
import json
from typing import Dict, List
from datetime import datetime, date, timedelta
import sqlite3

class DailyPlanner:
    """每日计划与总结"""

    def __init__(self, db_path: str = "daily_planner.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化每日计划数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建每日计划表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_date DATE NOT NULL,
                market TEXT NOT NULL,
                tasks TEXT NOT NULL,
                expected_outcomes TEXT,
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(plan_date, market)
            )
        """)

        # 创建每日执行记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_execution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_date DATE NOT NULL,
                market TEXT NOT NULL,
                tasks_completed TEXT NOT NULL,
                tasks_incomplete TEXT,
                metrics TEXT,
                challenges TEXT,
                lessons_learned TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(execution_date, market)
            )
        """)

        # 创建次日计划表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS next_day_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_date DATE NOT NULL,
                market TEXT NOT NULL,
                tasks TEXT NOT NULL,
                priorities TEXT,
                expected_outcomes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(plan_date, market)
            )
        """)

        conn.commit()
        conn.close()

    def create_daily_plan(self, plan_date: date, market: str,
                         tasks: List[Dict],
                         expected_outcomes: List[str] = None,
                         priority: str = "medium") -> int:
        """创建每日计划"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        tasks_json = json.dumps(tasks, ensure_ascii=False)
        outcomes_json = json.dumps(expected_outcomes or [], ensure_ascii=False)

        cursor.execute("""
            INSERT OR REPLACE INTO daily_plans
            (plan_date, market, tasks, expected_outcomes, priority, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (plan_date.isoformat(), market, tasks_json, outcomes_json,
              priority, datetime.now()))

        plan_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return plan_id

    def record_daily_execution(self, execution_date: date, market: str,
                              tasks_completed: List[Dict],
                              tasks_incomplete: List[Dict] = None,
                              metrics: Dict = None,
                              challenges: List[str] = None,
                              lessons_learned: List[str] = None) -> int:
        """记录每日执行情况"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        completed_json = json.dumps(tasks_completed, ensure_ascii=False)
        incomplete_json = json.dumps(tasks_incomplete or [], ensure_ascii=False)
        metrics_json = json.dumps(metrics or {}, ensure_ascii=False)
        challenges_json = json.dumps(challenges or [], ensure_ascii=False)
        lessons_json = json.dumps(lessons_learned or [], ensure_ascii=False)

        cursor.execute("""
            INSERT OR REPLACE INTO daily_execution
            (execution_date, market, tasks_completed, tasks_incomplete,
             metrics, challenges, lessons_learned, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (execution_date.isoformat(), market, completed_json, incomplete_json,
              metrics_json, challenges_json, lessons_json, datetime.now()))

        execution_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return execution_id

    def create_next_day_plan(self, plan_date: date, market: str,
                            tasks: List[Dict],
                            priorities: Dict = None,
                            expected_outcomes: List[str] = None) -> int:
        """创建次日计划"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        tasks_json = json.dumps(tasks, ensure_ascii=False)
        priorities_json = json.dumps(priorities or {}, ensure_ascii=False)
        outcomes_json = json.dumps(expected_outcomes or [], ensure_ascii=False)

        cursor.execute("""
            INSERT OR REPLACE INTO next_day_plan
            (plan_date, market, tasks, priorities, expected_outcomes, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (plan_date.isoformat(), market, tasks_json, priorities_json,
              outcomes_json, datetime.now()))

        plan_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return plan_id

    def get_daily_plan(self, plan_date: date, market: str) -> Dict:
        """获取每日计划"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tasks, expected_outcomes, priority
            FROM daily_plans
            WHERE plan_date = ? AND market = ?
        """, (plan_date.isoformat(), market))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"error": "Daily plan not found"}

        return {
            "plan_date": plan_date.isoformat(),
            "market": market,
            "tasks": json.loads(result[0]),
            "expected_outcomes": json.loads(result[1]),
            "priority": result[2]
        }

    def get_daily_execution(self, execution_date: date, market: str) -> Dict:
        """获取每日执行记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tasks_completed, tasks_incomplete, metrics, challenges, lessons_learned
            FROM daily_execution
            WHERE execution_date = ? AND market = ?
        """, (execution_date.isoformat(), market))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"error": "Daily execution not found"}

        return {
            "execution_date": execution_date.isoformat(),
            "market": market,
            "tasks_completed": json.loads(result[0]),
            "tasks_incomplete": json.loads(result[1]),
            "metrics": json.loads(result[2]),
            "challenges": json.loads(result[3]),
            "lessons_learned": json.loads(result[4])
        }

    def get_next_day_plan(self, plan_date: date, market: str) -> Dict:
        """获取次日计划"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tasks, priorities, expected_outcomes
            FROM next_day_plan
            WHERE plan_date = ? AND market = ?
        """, (plan_date.isoformat(), market))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {"error": "Next day plan not found"}

        return {
            "plan_date": plan_date.isoformat(),
            "market": market,
            "tasks": json.loads(result[0]),
            "priorities": json.loads(result[1]),
            "expected_outcomes": json.loads(result[2])
        }

    def generate_daily_summary(self, execution_date: date, market: str) -> Dict:
        """生成每日总结"""
        # 获取当日计划
        daily_plan = self.get_daily_plan(execution_date, market)

        # 获取当日执行
        daily_execution = self.get_daily_execution(execution_date, market)

        # 获取次日计划
        next_day = execution_date + timedelta(days=1)
        next_day_plan = self.get_next_day_plan(next_day, market)

        # 计算完成率
        completion_rate = 0
        if "error" not in daily_plan and "error" not in daily_execution:
            total_tasks = len(daily_plan["tasks"])
            completed_tasks = len(daily_execution["tasks_completed"])
            if total_tasks > 0:
                completion_rate = (completed_tasks / total_tasks) * 100

        # 生成总结
        summary = {
            "summary_date": execution_date.isoformat(),
            "market": market,
            "daily_plan": daily_plan,
            "daily_execution": daily_execution,
            "next_day_plan": next_day_plan,
            "completion_rate": round(completion_rate, 2),
            "key_achievements": self._extract_key_achievements(daily_execution),
            "areas_for_improvement": self._extract_areas_for_improvement(daily_execution),
            "recommendations": self._generate_daily_recommendations(daily_plan, daily_execution, completion_rate)
        }

        return summary

    def _extract_key_achievements(self, execution: Dict) -> List[str]:
        """提取关键成就"""
        achievements = []

        if "error" in execution:
            return achievements

        # 从完成任务中提取成就
        for task in execution["tasks_completed"]:
            if task.get("status") == "completed":
                achievements.append(f"✓ {task.get('description', '任务完成')}")

        # 从指标中提取成就
        if "metrics" in execution and execution["metrics"]:
            metrics = execution["metrics"]
            if "emails_sent" in metrics:
                achievements.append(f"✓ 发送邮件 {metrics['emails_sent']} 封")
            if "new_customers" in metrics:
                achievements.append(f"✓ 新增客户 {metrics['new_customers']} 个")
            if "replies_received" in metrics:
                achievements.append(f"✓ 收到回复 {metrics['replies_received']} 封")

        return achievements

    def _extract_areas_for_improvement(self, execution: Dict) -> List[str]:
        """提取改进领域"""
        areas = []

        if "error" in execution:
            return areas

        # 从未完成任务中提取改进领域
        for task in execution.get("tasks_incomplete", []):
            areas.append(f"✗ {task.get('description', '任务未完成')}")

        # 从挑战中提取改进领域
        for challenge in execution.get("challenges", []):
            areas.append(f"⚠ 挑战: {challenge}")

        return areas

    def _generate_daily_recommendations(self, plan: Dict, execution: Dict,
                                       completion_rate: float) -> List[str]:
        """生成每日建议"""
        recommendations = []

        # 基于完成率的建议
        if completion_rate >= 100:
            recommendations.append("🎯 今日任务全部完成，表现优秀！")
        elif completion_rate >= 80:
            recommendations.append("✅ 今日任务完成良好，继续保持")
        elif completion_rate >= 60:
            recommendations.append("⚠️ 今日任务完成一般，需要改进效率")
        else:
            recommendations.append("❌ 今日任务完成不理想，需要分析原因并改进")

        # 基于经验教训的建议
        if "error" not in execution:
            for lesson in execution.get("lessons_learned", []):
                recommendations.append(f"💡 经验: {lesson}")

        # 基于挑战的建议
        if "error" not in execution:
            for challenge in execution.get("challenges", []):
                recommendations.append(f"🔧 改进: 针对 '{challenge}' 制定应对策略")

        return recommendations

    def generate_weekly_plan(self, start_date: date, market: str) -> Dict:
        """生成周计划"""
        weekly_tasks = []

        # 工作日
        weekdays = [start_date + timedelta(days=i) for i in range(7)]

        for day in weekdays:
            daily_plan = self.get_daily_plan(day, market)

            if "error" not in daily_plan:
                weekly_tasks.append({
                    "date": day.isoformat(),
                    "weekday": day.strftime("%A"),
                    "tasks": daily_plan["tasks"]
                })

        return {
            "week_start": start_date.isoformat(),
            "week_end": (start_date + timedelta(days=6)).isoformat(),
            "market": market,
            "weekly_tasks": weekly_tasks,
            "total_tasks": sum(len(day["tasks"]) for day in weekly_tasks)
        }

def generate_sample_daily_plan():
    """生成示例每日计划"""
    planner = DailyPlanner()

    # 今天的日期
    today = date.today()

    # 创建示例每日计划
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

    planner.create_daily_plan(
        plan_date=today,
        market="USA",
        tasks=tasks,
        expected_outcomes=expected_outcomes,
        priority="high"
    )

    # 创建示例执行记录
    tasks_completed = [
        {
            "task_id": 1,
            "description": "执行客户搜索工作流",
            "status": "completed",
            "result": "成功搜索到25个潜在客户"
        },
        {
            "task_id": 2,
            "description": "发送开发邮件20封",
            "status": "completed",
            "result": "成功发送19封邮件，成功率95%"
        },
        {
            "task_id": 3,
            "description": "检查邮箱回复并跟进",
            "status": "completed",
            "result": "收到4封回复，已全部回复"
        }
    ]

    tasks_incomplete = [
        {
            "task_id": 4,
            "description": "更新CRM系统",
            "status": "incomplete",
            "reason": "时间不足，推迟到明天"
        },
        {
            "task_id": 5,
            "description": "分析当日数据并生成报告",
            "status": "incomplete",
            "reason": "时间不足，推迟到明天"
        }
    ]

    metrics = {
        "emails_sent": 19,
        "emails_success": 19,
        "new_customers": 25,
        "replies_received": 4,
        "reply_rate": 21.1
    }

    challenges = [
        "邮件发送成功率虽然高，但部分客户邮箱可能无效",
        "跟进回复需要更多时间，建议优化跟进流程"
    ]

    lessons_learned = [
        "客户搜索质量良好，过滤效果明显",
        "邮件模板有效，回复率高于预期",
        "需要预留更多时间处理客户回复"
    ]

    planner.record_daily_execution(
        execution_date=today,
        market="USA",
        tasks_completed=tasks_completed,
        tasks_incomplete=tasks_incomplete,
        metrics=metrics,
        challenges=challenges,
        lessons_learned=lessons_learned
    )

    # 创建次日计划
    tomorrow = today + timedelta(days=1)

    tomorrow_tasks = [
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
            "description": "更新CRM系统（补今日未完成）",
            "category": "数据管理",
            "priority": "high",
            "estimated_time": "1小时",
            "responsible": "人工"
        },
        {
            "task_id": 4,
            "description": "检查邮箱回复并跟进",
            "category": "客户跟进",
            "priority": "medium",
            "estimated_time": "1小时",
            "responsible": "人工"
        }
    ]

    tomorrow_priorities = {
        "high": ["执行客户搜索工作流", "发送开发邮件20封", "更新CRM系统"],
        "medium": ["检查邮箱回复并跟进"]
    }

    tomorrow_outcomes = [
        "成功搜索到20-30个潜在客户",
        "成功发送20封开发邮件",
        "CRM系统数据完整更新",
        "及时跟进所有客户回复"
    ]

    planner.create_next_day_plan(
        plan_date=tomorrow,
        market="USA",
        tasks=tomorrow_tasks,
        priorities=tomorrow_priorities,
        expected_outcomes=tomorrow_outcomes
    )

    # 生成每日总结
    summary = planner.generate_daily_summary(today, "USA")

    print("=" * 80)
    print("每日总结报告")
    print("=" * 80)
    print(f"日期: {summary['summary_date']}")
    print(f"市场: {summary['market']}")
    print(f"任务完成率: {summary['completion_rate']}%")

    print("\n🎯 关键成就:")
    for achievement in summary['key_achievements']:
        print(f"  {achievement}")

    print("\n⚠️ 改进领域:")
    for area in summary['areas_for_improvement']:
        print(f"  {area}")

    print("\n💡 建议:")
    for rec in summary['recommendations']:
        print(f"  {rec}")

    print("\n📅 次日计划:")
    if "error" not in summary['next_day_plan']:
        for task in summary['next_day_plan']['tasks'][:5]:
            print(f"  • {task['description']}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    generate_sample_daily_plan()
