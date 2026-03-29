#!/usr/bin/env python3
"""
发送工作流通知的脚本
支持：成功/失败通知，包含运行摘要
注意：当前版本不依赖任何外部模块，只输出日志
"""

import os
import sys
import json
from datetime import datetime

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def send_notification(status, workflow_name, summary=""):
    """
    发送工作流运行通知

    Args:
        status: 'success' | 'failure' | 'running'
        workflow_name: 工作流名称
        summary: 运行摘要
    """
    # 获取当前时间
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # 获取环境变量
    resend_api_key = os.getenv('RESEND_API_KEY', '未配置')
    notification_email = os.getenv('NOTIFICATION_EMAIL', '未配置')

    # 输出通知信息（不实际发送）
    print("=" * 60)
    print(f"📧 工作流通知")
    print("=" * 60)
    print(f"时间: {current_time}")
    print(f"状态: {status}")
    print(f"工作流: {workflow_name}")
    print(f"摘要: {summary if summary else '无'}")
    print(f"RESEND_API_KEY: {resend_api_key[:10]}..." if resend_api_key != '未配置' else f"RESEND_API_KEY: {resend_api_key}")
    print(f"NOTIFICATION_EMAIL: {notification_email}")
    print("=" * 60)

    # 不实际发送邮件，只记录日志
    print("⚠️  通知功能已禁用，仅输出日志")
    print("💡 如需启用通知，请修复依赖问题后恢复 send 功能")

    return True


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
