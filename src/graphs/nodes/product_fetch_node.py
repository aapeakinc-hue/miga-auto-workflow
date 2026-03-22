"""
产品信息抓取节点
从网站URL提取产品信息
"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.fetch import FetchClient
from graphs.state import ProductFetchInput, ProductFetchOutput

def product_fetch_node(state: ProductFetchInput, config: RunnableConfig, runtime: Runtime[Context]) -> ProductFetchOutput:
    """
    title: 产品信息抓取
    desc: 从指定网站URL提取产品信息，包括产品名称、描述、特点等关键信息
    integrations: Fetch URL
    """
    ctx = runtime.context
    
    # 初始化 FetchClient
    client = FetchClient(ctx=ctx)
    
    # 抓取网站内容
    response = client.fetch(url=state.website_url)
    
    # 提取文本内容
    text_parts = []
    if response.status_code == 0:
        for item in response.content:
            if item.type == "text" and item.text:
                text_parts.append(item.text)
        
        product_info = "\n".join(text_parts)
        
        # 限制内容长度，避免过长
        if len(product_info) > 5000:
            product_info = product_info[:5000] + "...（内容已截断）"
    else:
        product_info = f"抓取失败: {response.status_message}"
    
    return ProductFetchOutput(product_info=product_info)
