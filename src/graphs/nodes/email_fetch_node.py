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
    
    for customer in state.customer_list:
        website = customer.get("website", "")
        company_name = customer.get("company_name", "")
        
        if not website:
            # 如果没有网站，尝试从公司名称推导域名（简单示例）
            domain = company_name.lower().replace(" ", "").replace(".", "") + ".com"
        else:
            # 从网站URL提取域名
            domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        
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
            
            # 如果未找到邮箱，添加标记
            customer_with_email = {
                "company_name": company_name,
                "website": website,
                "domain": domain,
                "email": f"contact@{domain}",  # 使用通用联系邮箱作为备选
                "first_name": "",
                "last_name": "",
                "position": "Contact",
                "status": "estimated"
            }
            customers_with_email.append(customer_with_email)
            
        except Exception as e:
            # 发生错误时，使用估计的邮箱
            customer_with_email = {
                "company_name": company_name,
                "website": website,
                "domain": domain,
                "email": f"contact@{domain}",
                "first_name": "",
                "last_name": "",
                "position": "Contact",
                "status": "error",
                "error": str(e)
            }
            customers_with_email.append(customer_with_email)
    
    return EmailFetchOutput(customers_with_email=customers_with_email)
