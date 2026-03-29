"""
邮件生成节点
使用大模型生成个性化开发邮件
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import EmailGenerateInput, EmailGenerateOutput

def email_generate_node(state: EmailGenerateInput, config: RunnableConfig, runtime: Runtime[Context]) -> EmailGenerateOutput:
    """
    title: 邮件生成
    desc: 根据产品信息和客户信息，使用大模型生成个性化的外贸开发邮件
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 初始化 LLMClient
    client = LLMClient(ctx=ctx)
    
    email_templates = []
    
    # 如果没有客户信息，返回空列表
    if not state.customers_with_email or len(state.customers_with_email) == 0:
        return EmailGenerateOutput(email_templates=[])
    
    # 为每个客户生成个性化邮件
    for customer in state.customers_with_email:
        company_name = customer.get("company_name", "")
        email = customer.get("email", "")
        first_name = customer.get("first_name", "")
        last_name = customer.get("last_name", "")
        position = customer.get("position", "")
        
        # 构建收件人姓名
        if first_name and last_name:
            recipient_name = f"{first_name} {last_name}"
        elif first_name:
            recipient_name = first_name
        else:
            recipient_name = "Sir/Madam"
        
        # 系统提示词
        system_prompt = """你是一名专业的外贸业务开发专家，擅长撰写吸引客户的外贸开发邮件。

你的任务是：
1. 根据产品信息，撰写专业、简洁、有吸引力的开发邮件
2. 邮件要体现产品优势和价值
3. 使用商务英语，语气专业但友好
4. 邮件长度控制在 150-200 词左右
5. 包含明确的行动号召（CTA）

输出格式：
返回一个JSON对象，包含以下字段：
{
  "subject": "邮件主题",
  "body": "邮件正文（纯文本格式）"
}

注意：
- 邮件主题要简洁明了，吸引人打开
- 邮件正文要有针对性，体现对客户公司的研究
- 避免过度推销，强调价值而非价格
- 包含发件人邮箱：info@aapeakinc.com
- 结尾要有专业的署名"""
        
        # 用户提示词
        user_prompt = f"""请为以下客户撰写一封外贸开发邮件：

**产品信息：**
{state.product_info[:2000]}

**客户信息：**
- 公司名称：{company_name}
- 联系人：{recipient_name}
- 职位：{position}
- 邮箱：{email}

请生成一个吸引人的邮件主题和正文。"""
        
        # 调用大模型
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        try:
            response = client.invoke(messages=messages, temperature=0.7, model="doubao-seed-2-0-lite-260215")
            
            # 提取响应内容
            if isinstance(response.content, str):
                content = response.content
            elif isinstance(response.content, list):
                text_parts = []
                for item in response.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                content = " ".join(text_parts)
            else:
                content = str(response.content)
            
            # 解析JSON
            try:
                # 尝试提取JSON部分
                import re
                json_match = re.search(r'\{[^{}]*"[^"]*"[^{}]*\}', content)
                if json_match:
                    json_str = json_match.group()
                    email_data = json.loads(json_str)
                else:
                    # 如果没有找到JSON，使用备用格式
                    email_data = {
                        "subject": f"Partnership Opportunity with Yiwu Bangye Handicraft Factory",
                        "body": content
                    }
            except:
                # 解析失败，使用备用格式
                email_data = {
                    "subject": f"Partnership Opportunity - {company_name}",
                    "body": content
                }
            
            email_template = {
                "to_email": email,
                "to_name": recipient_name,
                "to_company": company_name,
                "subject": email_data.get("subject", "Partnership Opportunity"),
                "body": email_data.get("body", "Please see attached information.")
            }
            email_templates.append(email_template)
            
        except Exception as e:
            # 生成失败，使用备用模板
            email_template = {
                "to_email": email,
                "to_name": recipient_name,
                "to_company": company_name,
                "subject": f"Partnership Opportunity with Yiwu Bangye Handicraft Factory - {company_name}",
                "body": f"""Dear {recipient_name},

I hope this email finds you well. I am reaching out from Yiwu Bangye Handicraft Factory to explore potential partnership opportunities with {company_name}.

Based on my research, I believe our products could be a great fit for your business needs. We specialize in providing high-quality products with competitive pricing and excellent service.

I would appreciate the opportunity to discuss how we can support your business goals. Please let me know a convenient time for a brief call or email exchange.

Best regards,
Your Name
Yiwu Bangye Handicraft Factory
Email: info@aapeakinc.com
Website: https://www.aapeakinc.com"""
            }
            email_templates.append(email_template)
    
    return EmailGenerateOutput(email_templates=email_templates)
