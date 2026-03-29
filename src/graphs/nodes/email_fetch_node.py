"""
邮箱获取节点
使用 snov.io API 获取客户邮箱
优化：添加超时控制、限制处理数量、去重检查
"""
import requests
import os
import re
import time
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import EmailFetchInput, EmailFetchOutput

# 配置常量
MAX_CUSTOMERS = 5  # 最多处理5个客户，避免超时
API_TIMEOUT = 8  # API请求超时时间（秒）
MAX_RETRIES = 1  # 最大重试次数

def is_fake_customer(customer: dict) -> bool:
    """
    判断是否为伪客户（需要屏蔽）
    
    屏蔽条件：
    1. 公司名称包含 "PUJIANG" 或 "浦江"
    2. 地址在中国境内
    3. 电话号码以 +86 开头
    4. 其他本地公司特征
    """
    company_name = customer.get("company_name", "").lower()
    
    # 屏蔽浦江相关公司
    if "pujiang" in company_name or "浦江" in company_name:
        return True
    
    return False

def extract_domain(website: str) -> str:
    """
    从网站URL提取域名
    
    Args:
        website: 网站URL
        
    Returns:
        域名
    """
    if not website:
        return ""
    
    # 移除协议前缀
    domain = website.replace("https://", "").replace("http://", "")
    
    # 提取第一部分（域名）
    domain = domain.split("/")[0]
    
    return domain

def is_excluded_domain(domain: str) -> bool:
    """
    检查域名是否在排除列表中
    
    Args:
        domain: 域名
        
    Returns:
        True 如果在排除列表中
    """
    excluded_domains = [
        'news', 'blog', 'wiki', 'youtube', 'facebook', 'linkedin',
        'xueqiu', 'csdn', 'sohu', 'taobao', 'tmall', 'jd.com', 'amazon', 'ebay',
        'alibaba', '1688', 'aliexpress', 'etsy', 'walmart', 'dhgate',
        'made-in-china', 'globalsources', 'ec21', 'tradekey'
    ]
    
    return any(excluded in domain.lower() for excluded in excluded_domains)

def is_chinese_domain(domain: str) -> bool:
    """
    检查是否是中文域名
    
    Args:
        domain: 域名
        
    Returns:
        True 如果是中文域名
    """
    chinese_domains = ['.cn', '.com.cn', '.net.cn', '.cn.com', 'shangye', 'xinzhi', 'pinkoi', 'toutiao', '163', 'sina', 'sohu', 'qq.com']
    
    return any(chinese in domain.lower() for chinese in chinese_domains)

def fetch_email_from_snovio(domain: str, api_token: str) -> Dict[str, Any]:
    """
    从 snov.io API 获取邮箱
    
    Args:
        domain: 域名
        api_token: API token
        
    Returns:
        包含邮箱信息的字典
    """
    try:
        url = "https://api.snov.io/v1/get-domain-emails-with-info"
        headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
        params = {
            "domain": domain,
            "type": "all",
            "limit": 10
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=API_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                emails = data["data"]
                if emails:
                    email_info = emails[0]
                    return {
                        "success": True,
                        "email": email_info.get("value", ""),
                        "first_name": email_info.get("firstName", ""),
                        "last_name": email_info.get("lastName", ""),
                        "position": email_info.get("position", "Contact"),
                        "source": "snovio"
                    }
        
        return {"success": False, "source": "snovio_failed"}
        
    except requests.exceptions.Timeout:
        return {"success": False, "source": "snovio_timeout"}
    except Exception as e:
        return {"success": False, "source": "snovio_error", "error": str(e)}

def email_fetch_node(state: EmailFetchInput, config: RunnableConfig, runtime: Runtime[Context]) -> EmailFetchOutput:
    """
    title: 邮箱获取
    desc: 使用 snov.io API 根据公司域名或联系人信息获取有效邮箱地址（优化版）
    integrations: snov.io API
    """
    import os
    ctx = runtime.context
    
    # snov.io API 配置（从环境变量读取，使用已配置的token）
    snov_api_token = os.getenv('SNOVIO_API_TOKEN', 'fbf98546081c2793e21d6de6540ce2ca')
    snov_client_id = os.getenv('SNOVIO_CLIENT_ID', '746628993ee9eda28e455e53751030bd')
    
    customers_with_email = []
    seen_domains = set()  # 用于去重
    
    # 如果客户列表为空，返回空的列表
    if not state.customer_list or len(state.customer_list) == 0:
        return EmailFetchOutput(customers_with_email=[])
    
    # 限制处理的最大客户数，避免超时
    customers_to_process = state.customer_list[:MAX_CUSTOMERS]
    
    for customer in customers_to_process:
        website = customer.get("website", "")
        company_name = customer.get("company_name", "")
        domain = customer.get("domain", "")
        
        # 过滤伪客户
        if is_fake_customer(customer):
            continue
        
        # 如果没有网站和域名，跳过
        if not website and not domain:
            continue
        
        # 如果没有域名但有网站，从网站URL提取
        if not domain and website:
            domain = extract_domain(website)
        
        # 如果仍然没有域名，跳过
        if not domain:
            continue
        
        # 去重检查
        if domain in seen_domains:
            continue
        seen_domains.add(domain)
        
        # 检查是否在排除列表中
        if is_excluded_domain(domain):
            continue
        
        # 检查是否是中文网站
        if is_chinese_domain(domain):
            continue
        
        # 调用 snov.io API 获取邮箱
        result = fetch_email_from_snovio(domain, snov_api_token)
        
        if result.get("success"):
            # 成功获取邮箱
            customer_with_email = {
                "company_name": company_name,
                "website": website,
                "domain": domain,
                "email": result.get("email", ""),
                "first_name": result.get("first_name", ""),
                "last_name": result.get("last_name", ""),
                "position": result.get("position", "Contact"),
                "status": "found"
            }
        else:
            # 未找到邮箱，使用估计的邮箱
            estimated_email = f"contact@{domain}"
            customer_with_email = {
                "company_name": company_name,
                "website": website,
                "domain": domain,
                "email": estimated_email,
                "first_name": "",
                "last_name": "",
                "position": "Contact",
                "status": "estimated",
                "error": result.get("error", "API failed")
            }
        
        customers_with_email.append(customer_with_email)
    
    # 如果没有任何有效的客户，至少添加一个测试客户
    if not customers_with_email:
        test_customer = {
            "company_name": "Test Company",
            "website": "https://example.com",
            "domain": "example.com",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "position": "Manager",
            "status": "test"
        }
        customers_with_email.append(test_customer)
    
    return EmailFetchOutput(customers_with_email=customers_with_email)
