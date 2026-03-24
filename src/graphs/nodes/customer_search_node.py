"""
客户搜索节点
基于产品信息和关键词搜索潜在客户
"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import CustomerSearchInput, CustomerSearchOutput

def customer_search_node(state: CustomerSearchInput, config: RunnableConfig, runtime: Runtime[Context]) -> CustomerSearchOutput:
    """
    title: 客户搜索
    desc: 基于产品信息和目标关键词，通过网络搜索找到潜在客户及其联系信息
    integrations: Web Search
    """
    ctx = runtime.context
    
    # 初始化 SearchClient
    client = SearchClient(ctx=ctx)
    
    # 将中文关键词转换为英文搜索词
    # 提取关键信息进行英文搜索
    keyword_lower = state.target_keywords.lower()
    
    # 如果是中文关键词，使用预定义的英文搜索词
    if any(ord(c) > 127 for c in state.target_keywords):
        search_queries = [
            "crystal candle holders wholesale distributors USA",
            "crystal candelabra importers America",
            "crystal home decor wholesalers USA",
            "luxury crystal decor buyers United States",
            "wedding supplies crystal distributors USA",
            "crystal crafts wholesale America"
        ]
    else:
        # 英文关键词，组合搜索
        search_queries = [
            f"{state.target_keywords} crystal candelabra wholesale",
            f"{state.target_keywords} crystal decor importer",
            f"{state.target_keywords} wedding supplies distributor",
            f"{state.target_keywords} luxury home decor buyer",
            f"{state.target_keywords} crystal products wholesalers"
        ]
    
    # 收集所有搜索结果
    all_customers = []
    seen_domains = set()
    
    # 执行多个搜索
    for search_query in search_queries[:2]:  # 限制搜索2个查询
        response = client.web_search(
            query=search_query,
            count=10
        )
        
        if response.web_items:
            for result in response.web_items:
                # 过滤掉非商业网站和B2B平台
                domain = result.url.split('/')[2] if len(result.url.split('/')) > 2 else ""
                
                # 排除新闻网站、博客、B2B平台等
                excluded_domains = [
                    'news', 'blog', 'wiki', 'youtube', 'facebook', 'linkedin',
                    'alibaba', '1688', 'taobao', 'tmall', 'jd.com', 'amazon', 'ebay',
                    'etsy', 'walmart', 'aliexpress', 'dhgate', 'made-in-china',
                    'global sources', 'ec21', 'tradekey'
                ]
                if any(excluded in domain.lower() for excluded in excluded_domains):
                    continue
                
                # 去重
                if domain and domain in seen_domains:
                    continue
                if domain:
                    seen_domains.add(domain)
                
                customer = {
                    "company_name": result.title if result.title else "未知公司",
                    "website": result.url if result.url else "",
                    "description": result.snippet if result.snippet else "",
                    "domain": domain
                }
                all_customers.append(customer)
    
    # 限制返回5个最相关的客户
    customer_list = all_customers[:5] if all_customers else []
    
    return CustomerSearchOutput(customer_list=customer_list)
