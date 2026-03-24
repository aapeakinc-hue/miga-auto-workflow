"""
测试单个客户的邮件发送功能
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.getenv('COZE_WORKSPACE_PATH', ''), 'src'))

from graphs.graph import main_graph

# 测试单个客户
def test_single_customer():
    """测试发送邮件到单个客户"""
    print("🧪 测试单个客户邮件发送...")

    # 使用简单明确的英文关键词
    params = {
        "target_keywords": "crystal candle wholesale",  # 英文关键词
        "website_url": "https://miga.cc"  # 你的产品网站
    }

    print(f"📋 输入参数：")
    print(f"  - 关键词: {params['target_keywords']}")
    print(f"  - 网站: {params['website_url']}")
    print()

    try:
        # 运行工作流
        result = main_graph.invoke(params)

        print("✅ 工作流执行完成！")
        print()
        print("📊 结果统计：")
        print(f"  - 产品信息: {len(result.get('product_info', ''))} 字符")
        print(f"  - 搜索到的客户: {len(result.get('customer_list', []))}")
        print(f"  - 获取邮箱的客户: {len(result.get('customers_with_email', []))}")
        print(f"  - 生成的邮件模板: {len(result.get('email_templates', []))}")
        print()

        # 显示邮件发送结果
        send_results = result.get('send_results', {})
        print("📧 邮件发送结果：")
        print(f"  - 总数: {send_results.get('total', 0)}")
        print(f"  - 成功: {send_results.get('success', 0)}")
        print(f"  - 失败: {send_results.get('failed', 0)}")
        print()

        # 显示详细信息
        if send_results.get('details'):
            print("📝 详细信息：")
            for idx, detail in enumerate(send_results['details'], 1):
                print(f"  {idx}. 收件人: {detail.get('to_email', 'N/A')}")
                print(f"     状态: {detail.get('status', 'N/A')}")
                if detail.get('status') == 'success':
                    print(f"     消息ID: {detail.get('message_id', 'N/A')}")
                else:
                    print(f"     错误: {detail.get('error', 'N/A')}")
                print()

        # 显示生成的邮件模板
        email_templates = result.get('email_templates', [])
        if email_templates:
            print("📨 生成的邮件模板：")
            for idx, template in enumerate(email_templates, 1):
                print(f"  邮件 {idx}:")
                print(f"    收件人: {template.get('to_email', 'N/A')}")
                print(f"    姓名: {template.get('to_name', 'N/A')}")
                print(f"    公司: {template.get('to_company', 'N/A')}")
                print(f"    主题: {template.get('subject', 'N/A')}")
                print(f"    正文: {template.get('body', 'N/A')[:200]}...")
                print()

        # 显示客户列表
        customers_with_email = result.get('customers_with_email', [])
        if customers_with_email:
            print("👥 获取到的客户列表：")
            for idx, customer in enumerate(customers_with_email, 1):
                print(f"  客户 {idx}:")
                print(f"    公司: {customer.get('company_name', 'N/A')}")
                print(f"    邮箱: {customer.get('email', 'N/A')}")
                print(f"    状态: {customer.get('status', 'N/A')}")
                print(f"    网站: {customer.get('website', 'N/A')}")
                print()

        return result

    except Exception as e:
        print(f"❌ 执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_single_customer()
    print()
    if result:
        print("🎉 测试完成！")
    else:
        print("❌ 测试失败！")
