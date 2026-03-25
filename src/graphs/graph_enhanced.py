"""
外贸客户开发工作流 - 增强版（含客户洞察和挖掘）
工作流功能：
1. 产品信息获取
2. 客户洞察分析（基于现有客户数据）
3. 关键词优化
4. 客户挖掘
5. 客户搜索
6. 邮箱获取
7. 邮件生成
8. 邮件发送
"""
from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.product_fetch_node import product_fetch_node
from graphs.nodes.customer_insight_node import customer_insight_node
from graphs.nodes.keyword_optimizer_node import keyword_optimizer_node
from graphs.nodes.customer_mining_node import customer_mining_node
from graphs.nodes.customer_search_node import customer_search_node
from graphs.nodes.email_fetch_node import email_fetch_node
from graphs.nodes.email_generate_node import email_generate_node
from graphs.nodes.email_send_node import email_send_node

# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("product_fetch", product_fetch_node)
builder.add_node("customer_insight", customer_insight_node)
builder.add_node("keyword_optimizer", keyword_optimizer_node)
builder.add_node("customer_mining", customer_mining_node)
builder.add_node("customer_search", customer_search_node)
builder.add_node("email_fetch", email_fetch_node)
builder.add_node("email_generate", email_generate_node, metadata={"type": "agent", "llm_cfg": "config/email_generate_llm_cfg.json"})
builder.add_node("email_send", email_send_node)

# 设置入口点
builder.set_entry_point("product_fetch")

# 添加边（增强版流程）
# 1. 获取产品信息
# 2. 客户洞察分析（基于现有客户数据）
# 3. 关键词优化
# 4. 客户挖掘（基于优化关键词）
# 5. 客户搜索（搜索新客户）
# 6. 邮箱获取
# 7. 邮件生成
# 8. 邮件发送
builder.add_edge("product_fetch", "customer_insight")
builder.add_edge("customer_insight", "keyword_optimizer")
builder.add_edge("keyword_optimizer", "customer_mining")
builder.add_edge("customer_mining", "customer_search")
builder.add_edge("customer_search", "email_fetch")
builder.add_edge("email_fetch", "email_generate")
builder.add_edge("email_generate", "email_send")
builder.add_edge("email_send", END)

# 编译图
main_graph = builder.compile()
