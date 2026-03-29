"""
测试增强版工作流（含客户洞察和挖掘）
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from graphs.graph_enhanced import main_graph

def test_enhanced_workflow():
    """测试增强版工作流"""
    print("=" * 60)
    print("测试增强版工作流（含客户洞察和挖掘）")
    print("=" * 60)
    
    # 准备输入
    input_data = {
        "target_keywords": "美国水晶礼品批发商",
        "website_url": "https://products.miga.cc"
    }
    
    print(f"\n输入参数：")
    print(f"  目标关键词: {input_data['target_keywords']}")
    print(f"  网站URL: {input_data['website_url']}")
    
    print(f"\n工作流节点执行顺序：")
    print(f"  1. product_fetch - 产品信息获取")
    print(f"  2. customer_insight - 客户洞察分析")
    print(f"  3. keyword_optimizer - 关键词优化")
    print(f"  4. customer_mining - 客户挖掘")
    print(f"  5. customer_search - 客户搜索")
    print(f"  6. email_fetch - 邮箱获取")
    print(f"  7. email_generate - 邮件生成")
    print(f"  8. email_send - 邮件发送")
    
    print(f"\n开始执行工作流...")
    print("-" * 60)
    
    try:
        # 执行工作流
        result = main_graph.invoke(input_data)
        
        print("-" * 60)
        print(f"\n✅ 工作流执行完成！")
        print(f"\n输出结果：")
        
        # 输出客户洞察
        if "customer_insights" in result:
            insights = result["customer_insights"]
            print(f"\n📊 客户洞察分析：")
            if "summary" in insights:
                summary = insights["summary"]
                print(f"  总客户数: {summary.get('total_clients', 0)}")
                print(f"  有邮箱客户: {summary.get('clients_with_email', 0)}")
                print(f"  邮箱覆盖率: {summary.get('email_coverage', '0%')}")
            
            if "regional_analysis" in insights:
                regional = insights["regional_analysis"]
                if "top_markets" in regional:
                    print(f"\n  高价值市场 Top 5：")
                    for i, market in enumerate(regional["top_markets"][:5], 1):
                        print(f"    {i}. {market['country']}: {market['count']}个客户, 优先级{market['priority']}")
        
        # 输出优化关键词
        if "mining_keywords" in result:
            keywords = result["mining_keywords"]
            print(f"\n🔍 优化关键词（前10个）：")
            for i, keyword in enumerate(keywords[:10], 1):
                print(f"  {i}. {keyword}")
            print(f"  ... 总共{len(keywords)}个关键词")
        
        # 输出挖掘策略
        if "mining_strategy" in result:
            strategy = result["mining_strategy"]
            print(f"\n🎯 挖掘策略：")
            if "focus_markets" in strategy:
                print(f"  重点市场：")
                for i, market in enumerate(strategy["focus_markets"][:3], 1):
                    print(f"    {i}. {market['market']} - 目标{market.get('target_count', 0)}个客户")
        
        # 输出新挖掘的客户
        if "new_customers" in result:
            new_customers = result["new_customers"]
            print(f"\n🆕 新挖掘客户（前5个）：")
            for i, customer in enumerate(new_customers[:5], 1):
                print(f"  {i}. {customer['name']} ({customer['type']}) - {customer['country']}")
                print(f"     邮箱: {customer['email']}")
                print(f"     预估采购: {customer['estimated_purchase']}")
            print(f"  ... 总共{len(new_customers)}个新客户")
        
        # 输出搜索结果
        if "customer_list" in result and result["customer_list"]:
            print(f"\n🔍 搜索客户数: {len(result['customer_list'])}")
        
        # 输出发送结果
        if "send_results" in result and result["send_results"]:
            print(f"\n📧 邮件发送结果：")
            for key, value in result["send_results"].items():
                print(f"  {key}: {value}")
        
        print(f"\n{'=' * 60}")
        print(f"✅ 测试成功！增强版工作流运行正常。")
        print(f"{'=' * 60}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_enhanced_workflow()
