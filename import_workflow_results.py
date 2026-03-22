#!/usr/bin/env python3
"""
集成工作流结果到CRM系统
功能：自动解析工作流发送结果，导入客户到CRM
"""
import json
from typing import List, Dict
from crm_system import CRMDatabase, Customer, Interaction
from datetime import datetime, timedelta

class WorkflowToCRM:
    """工作流结果导入CRM"""

    @staticmethod
    def parse_send_results(send_results: Dict) -> List[Dict]:
        """解析邮件发送结果"""
        customers = []

        for detail in send_results.get("details", []):
            if detail.get("status") == "success":
                customer_data = {
                    "company_name": detail.get("to_company", ""),
                    "email": detail.get("to_email", ""),
                    "website": "",  # 需要从其他来源获取
                    "country": "USA",  # 默认美国，可根据实际情况调整
                    "industry": "Crystal Decor",  # 默认行业
                    "customer_type": "C",  # 新客户默认C类
                    "notes": f"邮件发送成功，消息ID: {detail.get('message_id', '')}"
                }
                customers.append(customer_data)

        return customers

    @staticmethod
    def import_to_crm(crm: CRMDatabase, customers: List[Dict]) -> Dict:
        """导入客户到CRM"""
        results = {
            "total": len(customers),
            "success": 0,
            "failed": 0,
            "duplicates": 0
        }

        for customer_data in customers:
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

                # 自动添加初始互动记录
                interaction = Interaction(
                    customer_id=customer_id,
                    interaction_type="email",
                    notes="通过工作流自动发送的开发邮件",
                    followup_date=(datetime.now() + timedelta(days=3)).date().isoformat()
                )
                crm.add_interaction(interaction)

            elif customer_id == -1:
                results["duplicates"] += 1
            else:
                results["failed"] += 1

        return results

    @staticmethod
    def process_workflow_file(crm: CRMDatabase, json_file: str) -> Dict:
        """处理工作流结果JSON文件"""
        with open(json_file, 'r', encoding='utf-8') as f:
            workflow_results = json.load(f)

        send_results = workflow_results.get("send_results", {})

        customers = WorkflowToCRM.parse_send_results(send_results)
        import_results = WorkflowToCRM.import_to_crm(crm, customers)

        return {
            "workflow_file": json_file,
            "total_emails": send_results.get("total", 0),
            "success_emails": send_results.get("success", 0),
            "imported_customers": import_results["success"],
            "duplicates": import_results["duplicates"],
            "failed_imports": import_results["failed"]
        }

def import_all_development_results():
    """导入所有客户开发结果"""
    print("=" * 80)
    print("导入工作流结果到CRM系统")
    print("=" * 80)

    # 初始化CRM
    crm = CRMDatabase("miga_crm.db")

    # 模拟工作流结果（实际使用时替换为真实的发送结果）
    # 这里使用之前测试的真实数据
    workflow_results_examples = [
        {
            "send_results": {
                "total": 5,
                "success": 4,
                "failed": 1,
                "details": [
                    {
                        "to_email": "john@crystalswholesaleusa.com",
                        "to_company": "Crystals Wholesale USA",
                        "status": "success",
                        "message_id": "msg-001"
                    },
                    {
                        "to_email": "info@tocrystal.com",
                        "to_company": "Tocrystal",
                        "status": "success",
                        "message_id": "msg-002"
                    },
                    {
                        "to_email": "sales@stonebridgeimports.com",
                        "to_company": "Stonebridge Imports",
                        "status": "success",
                        "message_id": "msg-003"
                    },
                    {
                        "to_email": "contact@sunbeauty.com",
                        "to_company": "Sunbeauty.com",
                        "status": "success",
                        "message_id": "msg-004"
                    },
                    {
                        "to_email": "",
                        "to_company": "Unknown",
                        "status": "failed",
                        "error": "No email address provided"
                    }
                ]
            }
        },
        {
            "send_results": {
                "total": 5,
                "success": 5,
                "failed": 0,
                "details": [
                    {
                        "to_email": "contact@bestdealsusa.com",
                        "to_company": "Best crystals Deals Online",
                        "status": "success",
                        "message_id": "msg-005"
                    },
                    {
                        "to_email": "orders@gabriel.com",
                        "to_company": "Gabrielle's The Classic Bride Salon",
                        "status": "success",
                        "message_id": "msg-006"
                    },
                    {
                        "to_email": "info@completewedo.com",
                        "to_company": "Complete Wedo",
                        "status": "success",
                        "message_id": "msg-007"
                    },
                    {
                        "to_email": "sales@prezi.com",
                        "to_company": "Prezi",
                        "status": "success",
                        "message_id": "msg-008"
                    },
                    {
                        "to_email": "contact@hotelcis.com",
                        "to_company": "Hotel CIS",
                        "status": "success",
                        "message_id": "msg-009"
                    }
                ]
            }
        }
    ]

    print("\n--- 开始导入客户 ---")

    total_imported = 0
    total_duplicates = 0

    for idx, results in enumerate(workflow_results_examples, 1):
        print(f"\n批次 {idx}:")
        customers = WorkflowToCRM.parse_send_results(results["send_results"])
        import_results = WorkflowToCRM.import_to_crm(crm, customers)

        print(f"  总客户数: {import_results['total']}")
        print(f"  成功导入: {import_results['success']}")
        print(f"  重复客户: {import_results['duplicates']}")
        print(f"  失败导入: {import_results['failed']}")

        total_imported += import_results['success']
        total_duplicates += import_results['duplicates']

    print(f"\n--- 导入汇总 ---")
    print(f"总导入客户: {total_imported}")
    print(f"重复客户: {total_duplicates}")

    # 显示CRM统计
    print(f"\n--- CRM当前统计 ---")
    stats = crm.get_statistics()
    print(f"客户总数: {stats['total_customers']}")
    print(f"客户类型分布: {stats['customer_types']}")

    # 导出数据
    export_file = crm.export_to_json("miga_crm_export.json")
    print(f"\n数据已导出到: {export_file}")

    print("\n" + "=" * 80)
    print("导入完成！")
    print("=" * 80)

if __name__ == "__main__":
    import_all_development_results()
