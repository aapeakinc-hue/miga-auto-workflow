#!/usr/bin/env python3
"""
GitHub Secrets 配置验证脚本
检查所有必需的环境变量是否已配置
"""
import os
import sys

def check_secrets():
    """检查 GitHub Secrets 配置"""

    # 必需的 Secrets
    required_secrets = {
        'SNOVIO_API_TOKEN': 'fbf98546081c2793e21d6de6540ce2ca',
        'SNOVIO_CLIENT_ID': '746628993ee9eda28e455e53751030bd',
        'RESEND_API_KEY': 're_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat',
        'NOTIFICATION_EMAIL': 'hue@aapeakinc.com'
    }

    print("=" * 60)
    print("🔍 GitHub Secrets 配置检查")
    print("=" * 60)
    print()

    all_configured = True

    for secret_name, default_value in required_secrets.items():
        current_value = os.getenv(secret_name)

        if current_value:
            # 显示部分值（安全起见）
            masked_value = current_value[:8] + "..." + current_value[-4:]
            status = "✅ 已配置"
            source = "环境变量"
        else:
            # 检查是否有默认值
            status = "⚠️  未配置（使用默认值）"
            masked_value = default_value[:8] + "..." + default_value[-4:]
            source = "代码默认值"
            all_configured = False

        print(f"{secret_name}:")
        print(f"  状态: {status}")
        print(f"  值: {masked_value}")
        print(f"  来源: {source}")
        print()

    print("=" * 60)
    if all_configured:
        print("✅ 所有 Secrets 已配置！")
        print()
        print("🎉 GitHub Actions 将使用配置的 Secrets 运行")
    else:
        print("⚠️  部分 Secrets 未配置")
        print()
        print("💡 建议：在 GitHub Secrets 中配置所有 Secrets")
        print("📖 参考文档：GITHUB_SECRETS_SETUP.md")
    print("=" * 60)

    return 0 if all_configured else 1

if __name__ == "__main__":
    sys.exit(check_secrets())
