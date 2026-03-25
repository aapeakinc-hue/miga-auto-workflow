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

try:
    import resend
except ImportError:
    # 如果 resend 库不可用，使用 requests
    import requests


def send_notification(status, workflow_name, summary=""):
    """
    发送工作流运行通知

    Args:
        status: 'success' | 'failure' | 'running'
        workflow_name: 工作流名称
        summary: 运行摘要
    """
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
    try:
        # 尝试使用 resend SDK
        resend.api_key = resend_api_key
        params = {
            "from": "外贸自动化系统 <noreply@aapeakinc.com>",
            "to": [notification_email],
            "subject": subject,
            "html": email_content
        }

        resend.Emails.send(params)
        print(f"✅ 通知已发送到 {notification_email}")
        return True

    except Exception as e1:
        # 如果 SDK 不可用，使用 REST API
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

            print(f"✅ 通知已发送到 {notification_email}")
            return True

        except Exception as e2:
            print(f"❌ 发送通知失败: {e2}")
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
