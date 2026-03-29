"""
邮件发送节点
使用 resend API 发送邮件
优化：添加重试机制、速率限制、更好的错误处理
"""
import requests
import os
import time
from typing import Dict, List, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import EmailSendInput, EmailSendOutput

# 配置常量
API_TIMEOUT = 15  # API请求超时时间（秒）
MAX_RETRIES = 2  # 最大重试次数
RATE_LIMIT_DELAY = 1  # 发送间隔（秒），避免触发速率限制

def send_single_email(
    to_email: str,
    to_name: str,
    to_company: str,
    subject: str,
    body: str,
    from_email: str,
    api_key: str
) -> Dict[str, Any]:
    """
    发送单封邮件（带重试机制）
    
    Args:
        to_email: 收件人邮箱
        to_name: 收件人姓名
        to_company: 收件人公司
        subject: 邮件主题
        body: 邮件正文
        from_email: 发件人邮箱
        api_key: Resend API Key
        
    Returns:
        发送结果字典
    """
    for attempt in range(MAX_RETRIES + 1):
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "from": from_email,
                "to": [to_email],
                "subject": subject,
                "html": f"""
<html>
<body>
<p>Dear {to_name},</p>
<p>{body.replace('\n', '<br>')}</p>
<br>
<p>Best regards,</p>
<p>Yiwu Bangye Handicraft Factory Team</p>
<p>Email: {from_email}</p>
<p>Website: https://miga.cc</p>
</body>
</html>
                """,
                "text": f"Dear {to_name},\n\n{body}\n\nBest regards,\nYiwu Bangye Handicraft Factory Team\nEmail: {from_email}\nWebsite: https://miga.cc"
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "message_id": result.get("id", ""),
                    "attempt": attempt + 1
                }
            else:
                # 如果是速率限制错误，等待后重试
                if response.status_code == 429 and attempt < MAX_RETRIES:
                    wait_time = (attempt + 1) * 2  # 指数退避
                    time.sleep(wait_time)
                    continue
                
                # 其他错误，直接返回失败
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "attempt": attempt + 1
                }
                
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                wait_time = (attempt + 1) * 2
                time.sleep(wait_time)
                continue
            return {
                "status": "failed",
                "error": "Request timeout",
                "attempt": attempt + 1
            }
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = (attempt + 1) * 2
                time.sleep(wait_time)
                continue
            return {
                "status": "failed",
                "error": str(e),
                "attempt": attempt + 1
            }
    
    return {
        "status": "failed",
        "error": "Max retries exceeded",
        "attempt": MAX_RETRIES + 1
    }

def email_send_node(state: EmailSendInput, config: RunnableConfig, runtime: Runtime[Context]) -> EmailSendOutput:
    """
    title: 邮件发送
    desc: 使用 resend API 批量发送个性化开发邮件给潜在客户（优化版）
    integrations: resend API
    """
    ctx = runtime.context
    
    # Resend API Key（从环境变量读取，使用已配置的key作为默认值）
    resend_api_key = os.getenv('RESEND_API_KEY', 're_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat')
    from_email = "info@miga.cc"
    
    # 统计结果
    send_results = {
        "total": len(state.email_templates),
        "success": 0,
        "failed": 0,
        "details": []
    }
    
    # 逐个发送邮件（带速率限制）
    for i, email_template in enumerate(state.email_templates):
        to_email = email_template.get("to_email", "")
        to_name = email_template.get("to_name", "")
        subject = email_template.get("subject", "")
        body = email_template.get("body", "")
        to_company = email_template.get("to_company", "")
        
        # 验证邮箱地址
        if not to_email or "@" not in to_email:
            send_results["failed"] += 1
            send_results["details"].append({
                "to_email": to_email,
                "to_company": to_company,
                "status": "failed",
                "error": "Invalid email address"
            })
            continue
        
        # 发送邮件
        result = send_single_email(
            to_email=to_email,
            to_name=to_name,
            to_company=to_company,
            subject=subject,
            body=body,
            from_email=from_email,
            api_key=resend_api_key
        )
        
        # 记录结果
        detail = {
            "to_email": to_email,
            "to_company": to_company,
            "status": result["status"],
            "attempt": result.get("attempt", 1)
        }
        
        if result["status"] == "success":
            send_results["success"] += 1
            detail["message_id"] = result.get("message_id", "")
        else:
            send_results["failed"] += 1
            detail["error"] = result.get("error", "Unknown error")
        
        send_results["details"].append(detail)
        
        # 速率限制：发送间隔
        if i < len(state.email_templates) - 1:  # 最后一封邮件不需要等待
            time.sleep(RATE_LIMIT_DELAY)
    
    return EmailSendOutput(send_results=send_results)
