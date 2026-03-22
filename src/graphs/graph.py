"""
外贸客户开发工作流 - 主图编排
工作流功能：从网站抓取产品信息 -> 搜索客户 -> 获取邮箱 -> 生成邮件 -> 发送邮件
"""
from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.product_fetch_node import product_fetch_node
from graphs.nodes.customer_search_node import customer_search_node
from graphs.nodes.email_fetch_node import email_fetch_node
from graphs.nodes.email_generate_node import email_generate_node
from graphs.nodes.email_send_node import email_send_node

# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("product_fetch", product_fetch_node)
builder.add_node("customer_search", customer_search_node)
builder.add_node("email_fetch", email_fetch_node)
builder.add_node("email_generate", email_generate_node, metadata={"type": "agent", "llm_cfg": "config/email_generate_llm_cfg.json"})
builder.add_node("email_send", email_send_node)

# 设置入口点
builder.set_entry_point("product_fetch")

# 添加边（线性流程）
builder.add_edge("product_fetch", "customer_search")
builder.add_edge("customer_search", "email_fetch")
builder.add_edge("email_fetch", "email_generate")
builder.add_edge("email_generate", "email_send")
builder.add_edge("email_send", END)

# 编译图
main_graph = builder.compile()
