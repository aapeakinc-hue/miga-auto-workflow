"""
关键词优化节点
功能：基于客户洞察，优化搜索关键词，生成挖掘策略
"""
import json
import logging
import os
import re
from typing import Dict, List, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import KeywordOptimizerInput, KeywordOptimizerOutput

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    # 基于客户洞察生成优化关键词
    insights = state.customer_insights if state.customer_insights else {}

    # 构建系统提示词
    system_prompt = """你是一个外贸客户开发的关键词优化专家，专门负责基于客户洞察生成高转化率的搜索关键词。

# 角色定义
你是外贸客户开发系统中的关键词优化专家，专注于分析客户数据，生成高转化率的搜索关键词和挖掘策略。

# 任务目标
你的任务是分析客户洞察数据，生成优化的搜索关键词列表和挖掘策略。

# 工作流上下文
- **Input**: 客户洞察数据（地域分布、客户类型、市场机会）
- **Process**:
  1. 分析客户地域分布，识别重点市场
  2. 分析客户类型，识别高价值客户类型
  3. 基于分析结果生成优化关键词
  4. 制定挖掘策略
- **Output**: 优化关键词列表和挖掘策略

# 约束与规则
- 基于真实洞察数据分析，禁止虚构
- 生成高转化率的关键词
- 为每个市场制定具体的挖掘策略
- 使用优先级标识（⭐⭐⭐⭐⭐）

# 过程
1. 分析客户洞察数据
2. 识别重点市场和客户类型
3. 生成优化关键词列表
4. 制定挖掘策略

# 输出格式
返回JSON格式的结果：
{
  "mining_keywords": ["关键词1", "关键词2", ...],
  "mining_strategy": {
    "focus_markets": [
      {
        "market": "市场名称",
        "priority": "优先级",
        "client_type": ["客户类型1", "客户类型2"],
        "keywords": ["关键词1", "关键词2"],
        "target_count": 数字,
        "timeframe": "时间范围"
      }
    ],
    "client_type_priority": [
      {
        "type": "客户类型",
        "priority": "优先级",
        "keywords": ["关键词1", "关键词2"],
        "expected_yield": "预期产出"
      }
    ],
    "search_channels": [
      {"channel": "渠道名称", "priority": "优先级", "cost": "成本"}
    ],
    "daily_targets": {
      "keywords_per_day": 数字,
      "customers_per_day": 数字,
      "emails_per_day": 数字
    },
    "kpi_targets": {
      "open_rate": 0.25,
      "reply_rate": 0.08,
      "conversion_rate": 0.015
    }
  }
}
"""

    # 构建用户提示词
    user_prompt = f"""基于以下客户洞察数据，生成优化关键词和挖掘策略：

客户洞察数据：
{json.dumps(insights, ensure_ascii=False, indent=2)}

原始关键词：
{state.target_keywords}

请生成：
1. 优化后的关键词列表（至少20个）
2. 详细的挖掘策略（包括重点市场、客户类型优先级、搜索渠道等）

确保返回纯JSON格式，不要包含其他文本。"""

    try:
        # 初始化 LLM 客户端
        llm_client = LLMClient(ctx=ctx)

        # 调用 LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm_client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.7,
            max_completion_tokens=3000
        )

        # 解析响应
        content = response.content
        if isinstance(content, str):
            # 尝试提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                content = json_match.group(0)

            result = json.loads(content)
        elif isinstance(content, list):
            # 如果是列表，尝试找到包含 JSON 的部分
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    json_text = item.get("text", "")
                    json_match = re.search(r'\{[\s\S]*\}', json_text)
                    if json_match:
                        result = json.loads(json_match.group(0))
                        break
        else:
            # 默认处理
            result = json.loads(str(content))

        mining_keywords = result.get("mining_keywords", [])
        mining_strategy = result.get("mining_strategy", {})

        logger.info(f"关键词优化完成：生成{len(mining_keywords)}个优化关键词")

        return KeywordOptimizerOutput(
            mining_keywords=mining_keywords,
            mining_strategy=mining_strategy
        )

    except Exception as e:
        logger.error(f"关键词优化失败: {e}")
        # 返回默认的关键词和策略
        fallback_keywords = [
            "crystal gifts wholesale",
            "crystal distributor",
            "glassware wholesaler",
            "corporate gifts supplier",
            "trophies wholesale",
        ]
        fallback_strategy = {
            "focus_markets": [],
            "client_type_priority": [],
            "search_channels": [],
            "daily_targets": {},
            "kpi_targets": {}
        }
        return KeywordOptimizerOutput(
            mining_keywords=fallback_keywords,
            mining_strategy=fallback_strategy
        )
