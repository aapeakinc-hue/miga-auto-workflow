#!/usr/bin/env python3
"""
发送工作流通知的脚本
支持：成功/失败通知，包含运行摘要
"""

import os
import sys
import json
from datetime import datetime

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 检查是否可以发送通知
CAN_SEND_NOTIFICATION = False
USE_RESEND_SDK = False
requests = None
resend = None

try:
    import resend
    USE_RESEND_SDK = True
    CAN_SEND_NOTIFICATION = True
except ImportError:
    # 如果 resend 库不可用，尝试使用 requests
    USE_RESEND_SDK = False
    try:
        import requests
        CAN_SEND_NOTIFICATION = True
    except ImportError:
        print("⚠️ 警告：resend 和 requests 模块都未安装，无法发送通知")


def send_notification(status, workflow_name, summary=""):
    """
    发送工作流运行通知

    Args:
        status: 'success' | 'failure' | 'running'
        workflow_name: 工作流名称
        summary: 运行摘要
    """
    # 检查是否可以发送通知
    if not CAN_SEND_NOTIFICATION:
        print(f"⚠️ 无法发送通知：必需的模块未安装")
        print(f"   工作流状态：{status}")
        print(f"   工作流名称：{workflow_name}")
        return True  # 返回 True 表示通知步骤完成（即使没有实际发送）

    resend_api_key = os.getenv('RESEND_API_KEY')
    notification_email = os.getenv('NOTIFICATION_EMAIL')

    if not resend_api_key:
        print("❌ RESEND_API_KEY 未配置，无法发送通知")
        return False

    if not notification_email:
        print("❌ NOTIFICATION_EMAIL 未配置，使用默认邮箱")
        notification_email = "hue@aapeakinc.com"

    # 准备邮件内容
    status_emoji = {
        'success': '✅',
        'failure': '❌',
        'running': '⏳'
    }

    status_title = {
        'success': '运行成功',
        'failure': '运行失败',
        'running': '正在运行'
    }

    # 获取当前时间
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # 邮件主题
    subject = f"{status_emoji[status]} {workflow_name} - {status_title[status]}"

    # 根据状态设置背景色
    header_bg = '#d4edda' if status == 'success' else '#f8d7da'

    # 邮件正文
    email_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: {header_bg};
                       padding: 20px; border-radius: 5px; text-align: center; }}
            .status {{ font-size: 24px; font-weight: bold; }}
            .info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .summary {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .footer {{ text-align: center; color: #6c757d; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="status">{status_emoji[status]} {status_title[status]}</div>
            </div>

            <div class="info">
                <h3>📋 基本信息</h3>
                <p><strong>工作流：</strong> {workflow_name}</p>
                <p><strong>状态：</strong> {status_title[status]}</p>
                <p><strong>时间：</strong> {current_time}</p>
            </div>

            {f'<div class="summary"><h3>📊 运行摘要</h3><pre>{summary}</pre></div>' if summary else ''}

            <div class="footer">
                <p>此邮件由自动化系统发送，请勿直接回复。</p>
                <p>如需查看详细信息，请访问 GitHub Actions 页面。</p>
            </div>
        </div>
    </body>
    </html>
    """

    # 发送邮件
    if USE_RESEND_SDK:
        # 使用 resend SDK
        try:
            resend.api_key = resend_api_key
            params = {
                "from": "外贸自动化系统 <noreply@aapeakinc.com>",
                "to": [notification_email],
                "subject": subject,
                "html": email_content
            }

            resend.Emails.send(params)
            print(f"✅ 通知已发送到 {notification_email} (使用 SDK)")
            return True

        except Exception as e:
            print(f"❌ 使用 Resend SDK 发送失败: {e}")
            # 降级到 REST API
            USE_RESEND_SDK = False

    # 使用 REST API
    if not USE_RESEND_SDK and requests:
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "from": "外贸自动化系统 <noreply@aapeakinc.com>",
                "to": [notification_email],
                "subject": subject,
                "html": email_content
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            print(f"✅ 通知已发送到 {notification_email} (使用 REST API)")
            return True

        except Exception as e:
            print(f"❌ 使用 REST API 发送失败: {e}")
            return False

    # 如果两种方式都不可用
    print("❌ 无法发送通知：resend SDK 和 requests 模块都不可用")
    return False


if __name__ == "__main__":
    # 从命令行参数获取状态和摘要
    status = sys.argv[1] if len(sys.argv) > 1 else 'running'
    workflow_name = sys.argv[2] if len(sys.argv) > 2 else '未知工作流'
    summary = sys.argv[3] if len(sys.argv) > 3 else ''

    # 获取环境变量中的摘要
    if not summary and os.getenv('WORKFLOW_SUMMARY'):
        summary = os.getenv('WORKFLOW_SUMMARY')

    # 读取日志文件作为摘要
    if not summary:
        log_file = os.getenv('LOG_FILE')
        if log_file and os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                summary = f.read()[-2000:]  # 只取最后2000字符

    send_notification(status, workflow_name, summary)
