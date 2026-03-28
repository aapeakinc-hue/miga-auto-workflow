"""
客户搜索节点
基于产品信息和关键词搜索潜在客户
"""
import re
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import CustomerSearchInput, CustomerSearchOutput

def is_fake_customer(customer: Dict[str, Any]) -> bool:
    """
    判断是否为伪客户（需要屏蔽）
    
    屏蔽条件：
    1. 公司名称包含 "PUJIANG" 或 "浦江"
    2. 地址在中国境内
    3. 电话号码以 +86 开头
    4. 其他本地公司特征
    """
    company_name = customer.get("company_name", "").lower()
    description = customer.get("description", "").lower()
    website = customer.get("website", "").lower()
    
    # 屏蔽浦江相关公司
    if "pujiang" in company_name or "浦江" in company_name:
        return True
    if "pujiang" in description or "浦江" in description:
        return True
    
    # 屏蔽中国境内地址（包含china、cn、中国等）
    china_keywords = ["china", "china ", "cn ", ".cn", "中国", "shanghai", "beijing", "guangzhou", "shenzhen"]
    if any(keyword in description for keyword in china_keywords):
        return True
    
    # 屏蔽中国电话号码（+86）
    if re.search(r'\+86', description) or re.search(r'\+86', website):
        return True
    
    # 屏屏水晶工厂、制造商（可能是本地工厂）
    factory_keywords = ["factory", "manufacturer", "production", "manufacturing"]
    if any(keyword in description.lower() for keyword in factory_keywords):
        # 如果同时包含china/中国，很可能是本地工厂
        if any(keyword in description.lower() for keyword in ["china", "中国"]):
            return True
    
    return False

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
                
                # 过滤伪客户
                if is_fake_customer(customer):
                    continue
                    
                all_customers.append(customer)
    
    # 限制返回5个最相关的客户
    customer_list = all_customers[:5] if all_customers else []
    
    return CustomerSearchOutput(customer_list=customer_list)
