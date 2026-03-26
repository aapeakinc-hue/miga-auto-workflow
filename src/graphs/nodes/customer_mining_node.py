"""
客户挖掘节点
功能：基于优化后的关键词和策略，挖掘新的潜在客户
"""
import logging
import re
from typing import Dict, List, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
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
    integrations: Web Search, LLM
    """
    ctx = runtime.context

    # 获取关键词和策略
    keywords = state.mining_keywords if state.mining_keywords else []
    strategy = state.mining_strategy if state.mining_strategy else {}

    new_customers = []

    # 初始化搜索客户端
    search_client = SearchClient(ctx=ctx)

    # 从策略中获取重点市场
    focus_markets = strategy.get("focus_markets", [])
    if not focus_markets:
        # 如果没有策略，使用默认搜索
        logger.info("没有挖掘策略，使用默认关键词搜索")
        for keyword in keywords[:10]:  # 限制搜索数量
            new_customers.extend(search_customers_by_keyword(search_client, keyword))
    else:
        # 按市场优先级搜索
        for market in focus_markets:
            market_name = market.get("market", "")
            market_keywords = market.get("keywords", [])
            target_count = market.get("target_count", 5)
            priority = market.get("priority", "⭐⭐⭐")

            logger.info(f"搜索 {market_name} 市场，优先级: {priority}")

            for keyword in market_keywords[:5]:  # 每个市场最多搜索5个关键词
                customers = search_customers_by_keyword(
                    search_client,
                    keyword,
                    market_name=market_name,
                    priority=priority
                )
                new_customers.extend(customers)

                # 达到目标数量后停止
                if len(new_customers) >= target_count:
                    break

    # 按优先级排序
    priority_order = {"⭐⭐⭐⭐⭐": 5, "⭐⭐⭐⭐": 4, "⭐⭐⭐": 3, "⭐⭐": 2, "⭐": 1}
    new_customers.sort(key=lambda x: priority_order.get(x.get("priority", "⭐⭐⭐"), 3), reverse=True)

    # 限制返回数量
    new_customers = new_customers[:50]

    logger.info(f"客户挖掘完成：发现{len(new_customers)}个新客户")

    return CustomerMiningOutput(new_customers=new_customers)

def search_customers_by_keyword(
    search_client: SearchClient,
    keyword: str,
    market_name: str = "",
    priority: str = "⭐⭐⭐"
) -> List[Dict[str, Any]]:
    """
    根据关键词搜索客户
    """
    customers = []

    try:
        # 执行搜索
        response = search_client.web_search(
            query=keyword,
            count=10,
            need_summary=False
        )

        if response.web_items:
            for item in response.web_items:
                # 提取客户信息
                customer = extract_customer_from_search_result(
                    item,
                    keyword=keyword,
                    market_name=market_name,
                    priority=priority
                )
                if customer:
                    customers.append(customer)

    except Exception as e:
        logger.warning(f"搜索关键词 '{keyword}' 失败: {e}")

    return customers

def extract_customer_from_search_result(
    item: Any,
    keyword: str,
    market_name: str = "",
    priority: str = "⭐⭐⭐"
) -> Dict[str, Any]:
    """
    从搜索结果中提取客户信息
    """
    try:
        # 从标题和摘要中提取公司名称
        title = item.title or ""
        snippet = item.snippet or ""
        url = item.url or ""

        # 简单提取公司名称
        company_name = title.split("|")[0].strip() if "|" in title else title.strip()

        # 从 URL 中提取域名
        domain = ""
        if url:
            match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            if match:
                domain = match.group(1)

        # 判断客户类型
        client_type = identify_client_type(title + " " + snippet)

        # 提取国家/地区
        country = identify_country(market_name, url, title)

        customer = {
            "name": company_name,
            "company": company_name,
            "country": country,
            "type": client_type,
            "source": f"基于关键词: {keyword}",
            "priority": priority,
            "url": url,
            "domain": domain,
            "snippet": snippet[:200] if snippet else "",
        }

        # 如果能从 URL 中提取邮箱（简单的启发式方法）
        email = extract_email_from_url(url, domain)
        if email:
            customer["email"] = email

        return customer

    except Exception as e:
        logger.warning(f"提取客户信息失败: {e}")
        return None

def identify_client_type(text: str) -> str:
    """
    识别客户类型
    """
    text_lower = text.lower()

    keywords_map = {
        "批发商": ["wholesale", "wholesaler", "distributor", "importer"],
        "酒店供应商": ["hotel", "hospitality", "resort", "hospitality supplier"],
        "活动策划": ["event", "planning", "wedding", "corporate", "awards"],
        "礼品商": ["gift", "souvenir", "retail", "shop", "store"],
        "贸易公司": ["trading", "export", "import", "trade"],
    }

    for client_type, keywords in keywords_map.items():
        for keyword in keywords:
            if keyword in text_lower:
                return client_type

    return "未知类型"

def identify_country(market_name: str, url: str, title: str) -> str:
    """
    识别国家/地区
    """
    # 如果有明确的市场名称，使用它
    if market_name:
        return market_name

    # 从 URL 中提取国家代码
    url_lower = url.lower()
    country_codes = {
        "美国": ["us", ".com", "united states", "usa"],
        "英国": ["uk", "gb", ".co.uk", "united kingdom"],
        "德国": ["de", ".de", "germany"],
        "法国": ["fr", ".fr", "france"],
        "日本": ["jp", ".jp", "japan"],
        "阿联酋": ["ae", ".ae", "uae", "dubai"],
        "澳大利亚": ["au", ".au", "australia"],
        "加拿大": ["ca", ".ca", "canada"],
    }

    for country, codes in country_codes.items():
        for code in codes:
            if code in url_lower or code in title.lower():
                return country

    return "未知"

def extract_email_from_url(url: str, domain: str) -> str:
    """
    从 URL 中提取邮箱（启发式方法）
    注意：这不是真实邮箱提取，仅用于演示
    真实场景需要调用 Snov.io 或类似 API
    """
    # 这里只是示例，真实场景需要调用专业 API
    # 例如：info@domain.com, sales@domain.com
    if domain:
        # 返回通用邮箱格式（用于测试）
        return f"contact@{domain}"

    return ""
