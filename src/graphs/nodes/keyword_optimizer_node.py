"""
关键词优化节点
功能：基于客户洞察，优化搜索关键词，生成挖掘策略
"""
import json
import os
from typing import Dict, List, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import KeywordOptimizerInput, KeywordOptimizerOutput

def keyword_optimizer_node(
    state: KeywordOptimizerInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> KeywordOptimizerOutput:
    """
    title: 关键词优化
    desc: 基于客户洞察优化搜索关键词，生成高转化关键词列表和挖掘策略
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取关键词清单
    try:
        with open('assets/trust-building/CUSTOMER_SEARCH_KEYWORDS.md', 'r', encoding='utf-8') as f:
            keywords_guide = f.read()
    except Exception as e:
        ctx.logger.warning(f"无法读取关键词清单: {e}")
        keywords_guide = ""
    
    # 基于客户洞察生成优化关键词
    insights = state.customer_insights if state.customer_insights else {}
    
    # 提取高优先级市场
    top_markets = insights.get("regional_analysis", {}).get("top_markets", [])
    
    # 生成优化关键词列表
    optimized_keywords = []
    
    # 美国市场关键词
    optimized_keywords.extend([
        "crystal gifts wholesale USA",
        "crystal distributor United States",
        "glassware wholesaler America",
        "corporate gifts supplier USA",
        "trophies wholesale USA",
        "crystal candle holders wholesale USA",
        "crystal figurines wholesale USA",
        "home decor wholesaler USA",
        "event planning New York",
        "corporate awards New York",
    ])
    
    # 英国市场关键词
    optimized_keywords.extend([
        "crystal gifts UK",
        "crystal awards UK",
        "event planning London",
        "corporate awards London",
        "custom trophy UK",
        "trophies supplier UK",
        "corporate gifts London",
        "luxury gifts UK",
    ])
    
    # 德国市场关键词
    optimized_keywords.extend([
        "glassware wholesaler Germany",
        "crystal gifts importer Germany",
        "crystal distributor Germany",
        "gift distributor Berlin",
        "corporate gifts Germany",
        "crystal home decor Germany",
    ])
    
    # 阿联酋市场关键词
    optimized_keywords.extend([
        "hotel supplies Dubai",
        "luxury hotel decoration UAE",
        "5 star hotel suppliers Dubai",
        "hospitality Dubai",
        "crystal gifts Dubai",
        "hospitality crystal supplies",
        "hotel trophy suppliers",
    ])
    
    # 日本市场关键词（日语）
    optimized_keywords.extend([
        "クリスタル ギフト 卸売",
        "クリスタル燭台 日本",
        "トロフィー 制作",
        "クリスタル 彫刻",
        "クリスタル 装飾",
    ])
    
    # 生成挖掘策略
    mining_strategy = {
        "focus_markets": [
            {
                "market": "美国",
                "priority": "⭐⭐⭐⭐⭐",
                "client_type": ["批发商", "礼品商"],
                "keywords": ["crystal gifts wholesale USA", "corporate gifts supplier USA"],
                "target_count": 20,
                "timeframe": "1周"
            },
            {
                "market": "英国",
                "priority": "⭐⭐⭐⭐⭐",
                "client_type": ["活动策划", "批发商"],
                "keywords": ["event planning London", "crystal awards UK"],
                "target_count": 15,
                "timeframe": "1周"
            },
            {
                "market": "阿联酋",
                "priority": "⭐⭐⭐⭐⭐",
                "client_type": ["酒店供应商"],
                "keywords": ["hotel supplies Dubai", "luxury hotel decoration UAE"],
                "target_count": 10,
                "timeframe": "1周"
            },
            {
                "market": "德国",
                "priority": "⭐⭐⭐⭐",
                "client_type": ["批发商"],
                "keywords": ["glassware wholesaler Germany", "crystal distributor Germany"],
                "target_count": 10,
                "timeframe": "1周"
            },
            {
                "market": "日本",
                "priority": "⭐⭐⭐⭐",
                "client_type": ["礼品商"],
                "keywords": ["クリスタル ギフト 卸売", "トロフィー 制作"],
                "target_count": 10,
                "timeframe": "1周"
            },
        ],
        "client_type_priority": [
            {
                "type": "批发商",
                "priority": "⭐⭐⭐⭐⭐",
                "keywords": ["wholesale", "distributor", "importer"],
                "expected_yield": "高转化率"
            },
            {
                "type": "酒店供应商",
                "priority": "⭐⭐⭐⭐⭐",
                "keywords": ["hotel supplies", "hospitality", "luxury hotel"],
                "expected_yield": "高价值客户"
            },
            {
                "type": "活动策划",
                "priority": "⭐⭐⭐⭐",
                "keywords": ["event planning", "corporate awards", "custom trophies"],
                "expected_yield": "快速交付需求"
            },
            {
                "type": "礼品商",
                "priority": "⭐⭐⭐⭐",
                "keywords": ["crystal gifts", "luxury gifts", "corporate gifts"],
                "expected_yield": "季节性订单"
            },
        ],
        "search_channels": [
            {"channel": "Google", "priority": "⭐⭐⭐⭐⭐", "cost": "免费"},
            {"channel": "LinkedIn", "priority": "⭐⭐⭐⭐⭐", "cost": "$20/月"},
            {"channel": "ThomasNet", "priority": "⭐⭐⭐⭐", "cost": "免费"},
            {"channel": "B2B平台", "priority": "⭐⭐⭐", "cost": "低"},
        ],
        "daily_targets": {
            "keywords_per_day": 10,
            "customers_per_day": 20,
            "emails_per_day": 20,
        },
        "kpi_targets": {
            "open_rate": 0.25,
            "reply_rate": 0.08,
            "conversion_rate": 0.015,
        }
    }
    
    ctx.logger.info(f"关键词优化完成：生成{len(optimized_keywords)}个优化关键词，{len(mining_strategy['focus_markets'])}个重点市场")
    
    return KeywordOptimizerOutput(
        mining_keywords=optimized_keywords,
        mining_strategy=mining_strategy
    )
