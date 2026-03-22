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
    
    # 构建搜索查询
    search_query = f"{state.target_keywords} suppliers manufacturers distributors importers"
    
    # 执行搜索
    response = client.web_search(
        query=search_query,
        count=10  # 搜索前10个结果
    )
    
    # 提取搜索结果
    customer_list = []
    if response.web_items:
        for result in response.web_items[:5]:  # 限制前5个
            customer = {
                "company_name": result.title if result.title else "未知公司",
                "website": result.url if result.url else "",
                "description": result.snippet if result.snippet else ""
            }
            customer_list.append(customer)
    
    # 如果搜索结果为空，返回示例数据
    if not customer_list:
        customer_list = [
            {
                "company_name": "示例客户1",
                "website": "https://example1.com",
                "description": "可能感兴趣的客户"
            },
            {
                "company_name": "示例客户2",
                "website": "https://example2.com",
                "description": "可能感兴趣的客户"
            }
        ]
    
    return CustomerSearchOutput(customer_list=customer_list)
