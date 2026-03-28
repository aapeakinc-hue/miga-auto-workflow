"""
邮件发送节点
使用 resend API 发送邮件
"""
import requests
import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import EmailSendInput, EmailSendOutput

def email_send_node(state: EmailSendInput, config: RunnableConfig, runtime: Runtime[Context]) -> EmailSendOutput:
    """
    title: 邮件发送
    desc: 使用 resend API 批量发送个性化开发邮件给潜在客户
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
    
    # 逐个发送邮件
    for email_template in state.email_templates:
        to_email = email_template.get("to_email", "")
        to_name = email_template.get("to_name", "")
        subject = email_template.get("subject", "")
        body = email_template.get("body", "")
        to_company = email_template.get("to_company", "")
        
        if not to_email:
            send_results["failed"] += 1
            send_results["details"].append({
                "to_email": to_email,
                "status": "failed",
                "error": "No email address provided"
            })
            continue
        
        try:
            # 调用 resend API
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {resend_api_key}",
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
<p>MIGA Team</p>
<p>Email: {from_email}</p>
<p>Website: https://miga.cc</p>
</body>
</html>
                """,
                "text": f"Dear {to_name},\n\n{body}\n\nBest regards,\nMIGA Team\nEmail: {from_email}\nWebsite: https://miga.cc"
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                send_results["success"] += 1
                send_results["details"].append({
                    "to_email": to_email,
                    "to_company": to_company,
                    "status": "success",
                    "message_id": result.get("id", "")
                })
            else:
                send_results["failed"] += 1
                send_results["details"].append({
                    "to_email": to_email,
                    "to_company": to_company,
                    "status": "failed",
                    "error": response.text
                })
                
        except Exception as e:
            send_results["failed"] += 1
            send_results["details"].append({
                "to_email": to_email,
                "to_company": to_company,
                "status": "failed",
                "error": str(e)
            })
    
    return EmailSendOutput(send_results=send_results)
