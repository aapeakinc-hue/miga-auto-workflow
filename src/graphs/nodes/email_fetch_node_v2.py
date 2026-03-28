"""
升级版邮箱获取节点
支持多 API 轮换使用
"""
import logging
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import EmailFetchInput, EmailFetchOutput
from tools.email_fetch_multi_api import fetch_emails_from_domain
from email_api_manager import setup_email_apis, email_api_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def email_fetch_node(
    state: EmailFetchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> EmailFetchOutput:
    """
    title: 邮箱获取
    desc: 从客户列表中获取邮箱，支持多 API 轮换
    integrations: Snov.io, Hunter.io, Clearbit
    """
    ctx = runtime.context
    
    # 设置邮箱 APIs
    setup_email_apis()
    
    customer_list = state.customer_list if state.customer_list else []
    customers_with_email = []
    
    logger.info(f"📧 开始获取 {len(customer_list)} 个客户的邮箱")
    
    for customer in customer_list:
        try:
            # 提取域名
            website = customer.get('website', '') or customer.get('url', '')
            if not website:
                logger.warning(f"⚠️  客户没有网站信息: {customer.get('name', 'N/A')}")
                continue
            
            # 提取域名
            import re
            domain_match = re.search(r'://(?:www\.)?([^/]+)', website)
            if not domain_match:
                logger.warning(f"⚠️  无法提取域名: {website}")
                continue
            
            domain = domain_match.group(1)
            logger.info(f"🔍 正在获取 {domain} 的邮箱...")
            
            # 使用多 API 获取邮箱
            emails = fetch_emails_from_domain(domain, max_results=3)
            
            if emails:
                # 添加邮箱信息到客户数据
                for email_info in emails[:1]:  # 只取第一个邮箱
                    customer_with_email = customer.copy()
                    customer_with_email['email'] = email_info['email']
                    customer_with_email['email_source'] = email_info['source']
                    customer_with_email['first_name'] = email_info.get('first_name', '')
                    customer_with_email['last_name'] = email_info.get('last_name', '')
                    customers_with_email.append(customer_with_email)
                    
                    logger.info(f"✅ 找到邮箱: {email_info['email']} (来源: {email_info['source']})")
                    break
            else:
                # 如果 API 都失败，使用估算邮箱
                estimated_email = f"contact@{domain}"
                customer_with_email = customer.copy()
                customer_with_email['email'] = estimated_email
                customer_with_email['email_source'] = 'estimated'
                customers_with_email.append(customer_with_email)
                
                logger.info(f"📝 使用估算邮箱: {estimated_email}")
        
        except Exception as e:
            logger.error(f"❌ 处理客户时出错: {e}")
            continue
    
    # 打印使用统计
    stats = email_api_manager.get_usage_stats()
    logger.info(f"\n📊 邮箱 API 使用统计:")
    logger.info(f"总 Key 数: {stats['total_keys']}")
    logger.info(f"总使用: {stats['total_used']}/{stats['total_limit']}")
    
    for detail in stats['details']:
        logger.info(f"  {detail['name']}: {detail['used']}/{detail['limit']} (剩余: {detail['remaining']})")
    
    logger.info(f"\n✅ 成功获取 {len(customers_with_email)} 个客户的邮箱")
    
    return EmailFetchOutput(customers_with_email=customers_with_email)
