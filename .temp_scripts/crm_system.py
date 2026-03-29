#!/usr/bin/env python3
"""
MIGA CRM管理系统
功能：客户管理、跟进追踪、数据分析
"""
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from dataclasses import dataclass

@dataclass
class Customer:
    """客户数据类"""
    id: int = 0
    company_name: str = ""
    contact_name: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    country: str = ""
    industry: str = ""
    customer_type: str = "C"  # A, B, C, D
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""

@dataclass
class Interaction:
    """互动记录数据类"""
    id: int = 0
    customer_id: int = 0
    interaction_type: str = ""  # email, call, meeting
    interaction_date: str = ""
    notes: str = ""
    followup_date: str = ""
    status: str = "pending"

@dataclass
class Order:
    """订单数据类"""
    id: int = 0
    customer_id: int = 0
    order_date: str = ""
    total_amount: float = 0.0
    status: str = "pending"
    notes: str = ""

class CRMDatabase:
    """CRM数据库管理"""

    def __init__(self, db_path: str = "crm_database.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建客户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                contact_name TEXT,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                website TEXT,
                country TEXT,
                industry TEXT,
                customer_type TEXT DEFAULT 'C',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建互动记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                interaction_type TEXT,
                interaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                followup_date TEXT,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        # 创建订单表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_date TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        conn.commit()
        conn.close()

    def add_customer(self, customer: Customer) -> int:
        """添加客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO customers (company_name, contact_name, email, phone, website,
                                     country, industry, customer_type, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer.company_name, customer.contact_name, customer.email,
                customer.phone, customer.website, customer.country,
                customer.industry, customer.customer_type, customer.notes
            ))
            conn.commit()
            customer_id = cursor.lastrowid
            return customer_id
        except sqlite3.IntegrityError:
            return -1  # 邮箱已存在
        finally:
            conn.close()

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """根据邮箱获取客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Customer(*row)
        return None

    def get_customers_by_type(self, customer_type: str) -> List[Customer]:
        """根据类型获取客户列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers WHERE customer_type = ?", (customer_type,))
        rows = cursor.fetchall()
        conn.close()

        return [Customer(*row) for row in rows]

    def update_customer_type(self, customer_id: int, new_type: str) -> bool:
        """更新客户类型"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE customers SET customer_type = ?, updated_at = ? WHERE id = ?",
            (new_type, datetime.now().isoformat(), customer_id)
        )
        conn.commit()
        conn.close()
        return True

    def add_interaction(self, interaction: Interaction) -> int:
        """添加互动记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO interactions (customer_id, interaction_type, notes, followup_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            interaction.customer_id, interaction.interaction_type,
            interaction.notes, interaction.followup_date, interaction.status
        ))
        conn.commit()
        interaction_id = cursor.lastrowid
        conn.close()
        return interaction_id

    def get_pending_followups(self, days_ahead: int = 7) -> List[Dict]:
        """获取待跟进的客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        future_date = (datetime.now() + timedelta(days=days_ahead)).date()

        cursor.execute("""
            SELECT c.id, c.company_name, c.email, c.customer_type,
                   i.interaction_type, i.followup_date, i.notes
            FROM customers c
            JOIN interactions i ON c.id = i.customer_id
            WHERE i.followup_date <= ? AND i.status = 'pending'
            ORDER BY i.followup_date
        """, (future_date.isoformat(),))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "customer_id": row[0],
                "company_name": row[1],
                "email": row[2],
                "customer_type": row[3],
                "interaction_type": row[4],
                "followup_date": row[5],
                "notes": row[6]
            }
            for row in rows
        ]

    def get_statistics(self) -> Dict:
        """获取统计数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 客户总数
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]

        # 各类型客户数量
        cursor.execute("""
            SELECT customer_type, COUNT(*) FROM customers
            GROUP BY customer_type
        """)
        customer_types = dict(cursor.fetchall())

        # 订单统计
        cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM orders WHERE status = 'completed'")
        order_stats = cursor.fetchone()

        conn.close()

        return {
            "total_customers": total_customers,
            "customer_types": customer_types,
            "completed_orders": order_stats[0] if order_stats[0] else 0,
            "total_revenue": order_stats[1] if order_stats[1] else 0.0
        }

    def export_to_json(self, output_file: str = "crm_export.json"):
        """导出数据为JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 导出客户数据
        cursor.execute("SELECT * FROM customers")
        customers = [dict(zip([col[0] for col in cursor.description], row))
                    for row in cursor.fetchall()]

        # 导出互动记录
        cursor.execute("SELECT * FROM interactions")
        interactions = [dict(zip([col[0] for col in cursor.description], row))
                        for row in cursor.fetchall()]

        # 导出订单数据
        cursor.execute("SELECT * FROM orders")
        orders = [dict(zip([col[0] for col in cursor.description], row))
                  for row in cursor.fetchall()]

        conn.close()

        data = {
            "export_date": datetime.now().isoformat(),
            "customers": customers,
            "interactions": interactions,
            "orders": orders
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return output_file

class CRMAnalyzer:
    """CRM数据分析"""

    @staticmethod
    def analyze_conversion_funnel(crm: CRMDatabase) -> Dict:
        """分析客户转化漏斗"""
        stats = crm.get_statistics()

        # 计算转化率（示例）
        total = stats["total_customers"]
        if total == 0:
            return {"error": "No customers found"}

        a_count = stats["customer_types"].get("A", 0)
        b_count = stats["customer_types"].get("B", 0)
        c_count = stats["customer_types"].get("C", 0)

        return {
            "total_customers": total,
            "potential_customers": c_count,
            "prospects": b_count,
            "vip_customers": a_count,
            "conversion_rate": round((a_count + b_count) / total * 100, 2) if total > 0 else 0
        }

    @staticmethod
    def get_customers_needing_followup(crm: CRMDatabase, days_ahead: int = 7) -> List[Dict]:
        """获取需要跟进的客户"""
        return crm.get_pending_followups(days_ahead)

    @staticmethod
    def generate_monthly_report(crm: CRMDatabase, year: int, month: int) -> str:
        """生成月度报告"""
        conn = sqlite3.connect(crm.db_path)
        cursor = conn.cursor()

        # 本月新增客户
        cursor.execute("""
            SELECT COUNT(*) FROM customers
            WHERE strftime('%Y-%m', created_at) = ?
        """, (f"{year}-{month:02d}",))
        new_customers = cursor.fetchone()[0]

        # 本月订单
        cursor.execute("""
            SELECT COUNT(*), SUM(total_amount) FROM orders
            WHERE strftime('%Y-%m', order_date) = ?
        """, (f"{year}-{month:02d}",))
        order_data = cursor.fetchone()

        conn.close()

        report = f"""
# {year}年{month}月 CRM报告

## 客户统计
- 本月新增客户: {new_customers}
- 本月订单数: {order_data[0] if order_data[0] else 0}
- 本月营收: ${order_data[1] if order_data[1] else 0:,.2f}

## 客户分布
{json.dumps(crm.get_statistics()['customer_types'], indent=2, ensure_ascii=False)}
        """
        return report

def main():
    """主函数 - 演示CRM系统使用"""
    print("=" * 80)
    print("MIGA CRM 管理系统")
    print("=" * 80)

    # 初始化CRM数据库
    crm = CRMDatabase("miga_crm.db")
    print("\n✅ CRM数据库初始化完成")

    # 示例：添加客户
    print("\n--- 添加客户示例 ---")
    customer1 = Customer(
        company_name="Crystals Wholesale USA",
        contact_name="John Smith",
        email="john@crystalswholesaleusa.com",
        country="USA",
        industry="Crystal Wholesale",
        customer_type="B",
        notes="高价值客户，已回复，正在评估"
    )
    customer_id = crm.add_customer(customer1)
    print(f"✅ 添加客户: {customer1.company_name} (ID: {customer_id})")

    # 添加互动记录
    print("\n--- 添加互动记录 ---")
    interaction = Interaction(
        customer_id=customer_id,
        interaction_type="email",
        notes="发送产品目录和价格表",
        followup_date=(datetime.now() + timedelta(days=3)).date().isoformat()
    )
    crm.add_interaction(interaction)
    print("✅ 添加互动记录")

    # 获取统计数据
    print("\n--- CRM统计 ---")
    stats = crm.get_statistics()
    print(f"总客户数: {stats['total_customers']}")
    print(f"客户类型分布: {stats['customer_types']}")
    print(f"已完成订单: {stats['completed_orders']}")
    print(f"总营收: ${stats['total_revenue']:,.2f}")

    # 获取需要跟进的客户
    print("\n--- 需要跟进的客户 ---")
    pending = crm.get_pending_followups(days_ahead=7)
    if pending:
        for item in pending:
            print(f"- {item['company_name']} ({item['email']}) - 跟进日期: {item['followup_date']}")
    else:
        print("暂无待跟进客户")

    # 导出数据
    print("\n--- 导出数据 ---")
    export_file = crm.export_to_json()
    print(f"✅ 数据已导出到: {export_file}")

    # 生成分析报告
    print("\n--- 转化漏斗分析 ---")
    funnel = CRMAnalyzer.analyze_conversion_funnel(crm)
    print(json.dumps(funnel, indent=2, ensure_ascii=False))

    print("\n" + "=" * 80)
    print("CRM系统演示完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
