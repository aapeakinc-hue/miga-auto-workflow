"""
邮箱获取节点
使用 snov.io API 获取客户邮箱
"""
import requests
import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import EmailFetchInput, EmailFetchOutput

def email_fetch_node(state: EmailFetchInput, config: RunnableConfig, runtime: Runtime[Context]) -> EmailFetchOutput:
    """
    title: 邮箱获取
    desc: 使用 snov.io API 根据公司域名或联系人信息获取有效邮箱地址
    integrations: snov.io API
    """
    ctx = runtime.context
    
    # snov.io API 配置
    snov_api_token = "fbf98546081c2793e21d6de6540ce2ca"
    snov_client_id = "746628993ee9eda28e455e53751030bd"
    
    customers_with_email = []
    
    # 如果客户列表为空，返回空的列表
    if not state.customer_list or len(state.customer_list) == 0:
        return EmailFetchOutput(customers_with_email=[])
    
    for customer in state.customer_list:
        website = customer.get("website", "")
        company_name = customer.get("company_name", "")
        domain = customer.get("domain", "")
        
        # 如果没有网站和域名，跳过
        if not website and not domain:
            continue
        
        # 如果没有域名但有网站，从网站URL提取
        if not domain and website:
            domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        
        # 如果仍然没有域名，跳过
        if not domain:
            continue
        
        # 如果没有域名，从网站URL提取
        if not domain:
            domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        
        # 进一步验证是否为企业网站（排除常见的非商业域名和电商平台/B2B平台）
        excluded_domains = [
            'news', 'blog', 'wiki', 'youtube', 'facebook', 'linkedin',
            'xueqiu', 'csdn', 'sohu', 'taobao', 'tmall', 'jd.com', 'amazon', 'ebay',
            'alibaba', '1688', 'aliexpress', 'etsy', 'walmart', 'dhgate',
            'made-in-china', 'globalsources', 'ec21', 'tradekey'
        ]
        
        # 优先选择欧美地区的企业
        preferred_tlds = ['.com', '.net', '.org', '.us', '.uk', '.eu', '.ca', '.au']
        
        # 检查是否在排除列表中
        if any(excluded in domain.lower() for excluded in excluded_domains):
            # 跳过这些平台，不添加到结果中
            continue
        
        # 检查是否是中文网站（排除）
        chinese_domains = ['.cn', '.com.cn', '.net.cn', '.cn.com', 'shangye', 'xinzhi', 'pinkoi', 'toutiao', '163', 'sina', 'sohu', 'qq.com']
        if any(chinese in domain.lower() for chinese in chinese_domains):
            # 跳过中文网站，不添加到结果中
            continue
        
        # 调用 snov.io API 获取邮箱
        try:
            url = "https://api.snov.io/v1/get-domain-emails-with-info"
            headers = {
                "Authorization": snov_api_token,
                "Content-Type": "application/json"
            }
            params = {
                "domain": domain,
                "type": "all",
                "limit": 10
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    emails = data["data"]
                    if emails:
                        # 获取第一个有效邮箱
                        email_info = emails[0]
                        customer_with_email = {
                            "company_name": company_name,
                            "website": website,
                            "domain": domain,
                            "email": email_info.get("value", ""),
                            "first_name": email_info.get("firstName", ""),
                            "last_name": email_info.get("lastName", ""),
                            "position": email_info.get("position", "Contact"),
                            "status": "found"
                        }
                        customers_with_email.append(customer_with_email)
                        continue
            
            # 如果未找到邮箱，使用估计的邮箱
            estimated_email = f"contact@{domain}"
            customer_with_email = {
                "company_name": company_name,
                "website": website,
                "domain": domain,
                "email": estimated_email,  # 使用通用联系邮箱作为备选
                "first_name": "",
                "last_name": "",
                "position": "Contact",
                "status": "estimated"
            }
            customers_with_email.append(customer_with_email)
            
        except Exception as e:
            # 发生错误时，使用估计的邮箱
            estimated_email = f"contact@{domain}"
            customer_with_email = {
                "company_name": company_name,
                "website": website,
                "domain": domain,
                "email": estimated_email,
                "first_name": "",
                "last_name": "",
                "position": "Contact",
                "status": "error",
                "error": str(e)
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
