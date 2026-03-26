"""
客户挖掘节点
功能：基于优化后的关键词和策略，挖掘新的潜在客户
"""
import logging
from typing import Dict, List, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import CustomerMiningInput, CustomerMiningOutput

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def customer_mining_node(
    state: CustomerMiningInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CustomerMiningOutput:
    """
    title: 客户挖掘
    desc: 基于优化后的关键词和挖掘策略，搜索新的潜在客户
    integrations: Web Search, Snov.io
    """
    ctx = runtime.context
    
    # 获取关键词和策略
    keywords = state.mining_keywords if state.mining_keywords else []
    strategy = state.mining_strategy if state.mining_strategy else {}
    
    # 模拟客户挖掘过程
    # 实际应用中，这里会调用 Web Search 和 Snov.io API
    new_customers = []
    
    # 基于策略生成模拟客户数据
    focus_markets = strategy.get("focus_markets", [])
    
    for market in focus_markets:
        market_name = market.get("market", "")
        target_count = market.get("target_count", 5)
        client_types = market.get("client_type", ["批发商"])
        market_keywords = market.get("keywords", [])
        
        # 为每个市场生成模拟客户
        for i in range(min(target_count, 10)):  # 限制每个市场最多10个
            client_type = client_types[i % len(client_types)]
            keyword = market_keywords[i % len(market_keywords)] if market_keywords else f"{client_type} {market_name}"
            
            # 生成模拟客户数据
            customer = {
                "name": f"{market_name} {client_type} {i+1}",
                "company": f"{market_name} {client_type} Co Ltd",
                "country": market_name,
                "type": client_type,
                "source": f"基于关键词: {keyword}",
                "priority": market.get("priority", "⭐⭐⭐"),
                "estimated_purchase": {
                    "批发商": "$100K-$300K",
                    "酒店供应商": "$200K-$500K",
                    "活动策划": "$20K-$100K",
                    "礼品商": "$30K-$150K",
                }.get(client_type, "$50K-$200K"),
            }
            
            # 模拟邮箱（实际应该从Snov.io获取）
            customer["email"] = f"contact{i+1}@{client_type.lower().replace(' ', '')}{market_name.lower()}.com"
            
            new_customers.append(customer)
    
    # 按优先级排序
    priority_order = {"⭐⭐⭐⭐⭐": 5, "⭐⭐⭐⭐": 4, "⭐⭐⭐": 3, "⭐⭐": 2, "⭐": 1}
    new_customers.sort(key=lambda x: priority_order.get(x.get("priority", "⭐⭐⭐"), 3), reverse=True)
    
    logger.info(f"客户挖掘完成：发现{len(new_customers)}个新客户，覆盖{len(focus_markets)}个市场")

    return CustomerMiningOutput(new_customers=new_customers)
