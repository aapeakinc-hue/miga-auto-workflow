#!/usr/bin/env python3
"""
MIGA CRM 工具集
功能：批量导入客户、自动跟进提醒、客户分类管理
"""
import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict
from crm_system import CRMDatabase, Customer, Interaction, CRMAnalyzer

class CRMImporter:
    """CRM批量导入工具"""

    @staticmethod
    def import_from_json(crm: CRMDatabase, json_file: str) -> Dict:
        """从JSON文件批量导入客户"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "duplicates": 0
        }

        for customer_data in data.get("customers", []):
            results["total"] += 1

            customer = Customer(
                company_name=customer_data.get("company_name", ""),
                contact_name=customer_data.get("contact_name", ""),
                email=customer_data.get("email", ""),
                phone=customer_data.get("phone", ""),
                website=customer_data.get("website", ""),
                country=customer_data.get("country", ""),
                industry=customer_data.get("industry", ""),
                customer_type=customer_data.get("customer_type", "C"),
                notes=customer_data.get("notes", "")
            )

            customer_id = crm.add_customer(customer)
            if customer_id > 0:
                results["success"] += 1
            elif customer_id == -1:
                results["duplicates"] += 1
            else:
                results["failed"] += 1

        return results

    @staticmethod
    def import_from_csv(crm: CRMDatabase, csv_file: str) -> Dict:
        """从CSV文件批量导入客户"""
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "duplicates": 0
        }

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                results["total"] += 1

                customer = Customer(
                    company_name=row.get("company_name", ""),
                    contact_name=row.get("contact_name", ""),
                    email=row.get("email", ""),
                    phone=row.get("phone", ""),
                    website=row.get("website", ""),
                    country=row.get("country", ""),
                    industry=row.get("industry", ""),
                    customer_type=row.get("customer_type", "C"),
                    notes=row.get("notes", "")
                )

                customer_id = crm.add_customer(customer)
                if customer_id > 0:
                    results["success"] += 1
                elif customer_id == -1:
                    results["duplicates"] += 1
                else:
                    results["failed"] += 1

        return results

class CRMAutoFollowup:
    """CRM自动跟进工具"""

    @staticmethod
    def generate_followup_tasks(crm: CRMDatabase, days_ahead: int = 7) -> List[Dict]:
        """生成跟进任务列表"""
        pending = crm.get_pending_followups(days_ahead)

        tasks = []
        for item in pending:
            followup_date = datetime.fromisoformat(item['followup_date'])
            days_until = (followup_date.date() - datetime.now().date()).days

            task = {
                "customer_id": item['customer_id'],
                "company_name": item['company_name'],
                "email": item['email'],
                "customer_type": item['customer_type'],
                "followup_date": item['followup_date'],
                "days_until": days_until,
                "priority": "high" if days_until <= 3 else "medium",
                "last_interaction": item['notes'],
                "suggested_action": CRMAnalyzer._get_suggested_action(item['customer_type'], days_until)
            }
            tasks.append(task)

        return sorted(tasks, key=lambda x: x['days_until'])

    @staticmethod
    def get_followup_template(customer_type: str, stage: str) -> str:
        """获取跟进邮件模板"""
        templates = {
            "A": {
                "initial": """尊敬的{contact_name}，

感谢您对MIGA水晶产品的兴趣！
作为我们的VIP客户，我们为您准备了专属优惠。
本周内下单可享受15%折扣。

期待您的回复！

MIGA Team
info@miga.cc""",
                "followup": """尊敬的{contact_name}，

只是想确认一下您对我们产品的评估情况。
如果您有任何问题或需要更多信息，请随时联系我。

期待与您的合作！

MIGA Team
info@miga.cc"""
            },
            "B": {
                "initial": """尊敬的{contact_name}，

感谢您回复我们的邮件！
我已准备好产品目录和价格表，请查收附件。
如果您需要样品，我们可以免费寄送。

期待您的回复！

MIGA Team
info@miga.cc""",
                "followup": """尊敬的{contact_name}，

想确认一下您是否有时间查看我们的产品信息？
我们的水晶烛台和工艺品非常适合您的业务需求。
如有任何疑问，请随时联系我。

MIGA Team
info@miga.cc"""
            },
            "C": {
                "initial": """尊敬的合作伙伴，

我是MIGA的业务代表，我们专业生产高品质水晶烛台和工艺品。
我们的产品价格优惠，质量上乘，非常适合您的业务。

查看我们的产品目录：https://products.miga.cc

期待与您的合作！

MIGA Team
info@miga.cc""",
                "followup": """尊敬的合作伙伴，

想再次向您介绍我们的水晶产品系列。
近期我们有多款新品上市，价格特别优惠。
如果有兴趣，请回复邮件获取详细信息。

MIGA Team
info@miga.cc"""
            }
        }

        return templates.get(customer_type, {}).get(stage, "")

class CRMSegmentManager:
    """客户分类管理工具"""

    @staticmethod
    def classify_customer(crm: CRMDatabase, customer_id: int, new_type: str) -> bool:
        """更新客户分类"""
        return crm.update_customer_type(customer_id, new_type)

    @staticmethod
    def get_segment_summary(crm: CRMDatabase) -> Dict:
        """获取各分类客户摘要"""
        stats = crm.get_statistics()
        customer_types = stats['customer_types']

        summary = {}
        for customer_type, count in customer_types.items():
            customers = crm.get_customers_by_type(customer_type)

            summary[customer_type] = {
                "count": count,
                "percentage": round(count / stats['total_customers'] * 100, 2) if stats['total_customers'] > 0 else 0,
                "customers": [
                    {
                        "id": c.id,
                        "company_name": c.company_name,
                        "email": c.email,
                        "industry": c.industry,
                        "country": c.country
                    }
                    for c in customers
                ]
            }

        return summary

    @staticmethod
    def suggest_customer_upgrade(crm: CRMDatabase, customer_id: int) -> Dict:
        """建议客户升级"""
        conn = sqlite3.connect(crm.db_path)
        cursor = conn.cursor()

        # 获取客户信息和互动记录
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer_data = cursor.fetchone()

        if not customer_data:
            return {"error": "Customer not found"}

        customer = Customer(*customer_data)

        # 统计互动次数
        cursor.execute("""
            SELECT COUNT(*) FROM interactions WHERE customer_id = ?
        """, (customer_id,))
        interaction_count = cursor.fetchone()[0]

        # 统计订单数量
        cursor.execute("""
            SELECT COUNT(*), SUM(total_amount) FROM orders WHERE customer_id = ? AND status = 'completed'
        """, (customer_id,))
        order_stats = cursor.fetchone()

        conn.close()

        # 建议升级逻辑
        suggestion = {
            "current_type": customer.customer_type,
            "suggested_type": customer.customer_type,
            "reason": "",
            "interaction_count": interaction_count,
            "order_count": order_stats[0] if order_stats[0] else 0,
            "total_revenue": order_stats[1] if order_stats[1] else 0.0
        }

        if customer.customer_type == "C":
            if interaction_count >= 2:
                suggestion["suggested_type"] = "B"
                suggestion["reason"] = "已多次互动，建议升级为重点客户"
        elif customer.customer_type == "B":
            if order_stats[0] >= 1:
                suggestion["suggested_type"] = "A"
                suggestion["reason"] = f"已成交{order_stats[0]}单，总金额${order_stats[1]:,.2f}，建议升级为VIP客户"

        return suggestion

def main():
    """主函数 - 演示CRM工具使用"""
    print("=" * 80)
    print("MIGA CRM 工具集演示")
    print("=" * 80)

    # 初始化CRM
    crm = CRMDatabase("miga_crm.db")

    # 1. 自动跟进提醒
    print("\n--- 自动跟进提醒 ---")
    followup_tasks = CRMAutoFollowup.generate_followup_tasks(crm, days_ahead=7)

    if followup_tasks:
        print(f"发现 {len(followup_tasks)} 个跟进任务:")
        for task in followup_tasks[:5]:  # 显示前5个
            print(f"\n公司: {task['company_name']}")
            print(f"客户类型: {task['customer_type']}")
            print(f"跟进日期: {task['followup_date']} ({task['days_until']}天后)")
            print(f"优先级: {task['priority']}")
            print(f"建议操作: {task['suggested_action']}")
    else:
        print("暂无跟进任务")

    # 2. 客户分类摘要
    print("\n--- 客户分类摘要 ---")
    segment_summary = CRMSegmentManager.get_segment_summary(crm)
    for customer_type, data in segment_summary.items():
        print(f"\n{customer_type}类客户:")
        print(f"  数量: {data['count']}")
        print(f"  占比: {data['percentage']}%")
        print(f"  客户列表: {[c['company_name'] for c in data['customers'][:3]]}")

    # 3. 获取跟进模板
    print("\n--- 跟进邮件模板 ---")
    for customer_type in ["A", "B", "C"]:
        template = CRMAutoFollowup.get_followup_template(customer_type, "initial")
        if template:
            print(f"\n{customer_type}类客户初始邮件模板:")
            print(template[:100] + "...")

    print("\n" + "=" * 80)
    print("CRM工具演示完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
