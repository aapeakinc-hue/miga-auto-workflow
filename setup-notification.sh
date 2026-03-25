#!/bin/bash
# 快速配置工作流通知

echo "========================================="
echo "  工作流通知配置向导"
echo "========================================="
echo ""

# 检查是否安装了 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) 未安装"
    echo ""
    echo "请先安装 GitHub CLI："
    echo "  macOS: brew install gh"
    echo "  Linux: https://cli.github.com/"
    echo ""
    echo "安装完成后，请运行: gh auth login"
    exit 1
fi

# 检查是否已登录
echo "🔍 检查 GitHub CLI 登录状态..."
if ! gh auth status &> /dev/null; then
    echo "❌ 未登录 GitHub"
    echo "请运行: gh auth login"
    exit 1
fi

echo "✅ 已登录 GitHub"
echo ""

# 获取通知邮箱
echo "请输入您的通知邮箱地址："
read -p "> " NOTIFICATION_EMAIL

if [ -z "$NOTIFICATION_EMAIL" ]; then
    echo "❌ 邮箱地址不能为空"
    exit 1
fi

echo ""
echo "📧 配置通知邮箱: $NOTIFICATION_EMAIL"

# 设置 Secret
echo ""
echo "🔧 正在配置 GitHub Secrets..."

# 设置 NOTIFICATION_EMAIL
gh secret set NOTIFICATION_EMAIL -b"$NOTIFICATION_EMAIL" --repo aapeakinc-hue/miga-auto-workflow

if [ $? -eq 0 ]; then
    echo "✅ NOTIFICATION_EMAIL 配置成功"
else
    echo "❌ NOTIFICATION_EMAIL 配置失败"
    exit 1
fi

# 检查 RESEND_API_KEY 是否存在
echo ""
echo "🔍 检查 RESEND_API_KEY..."

RESEND_API_KEY=$(gh secret get RESEND_API_KEY --repo aapeakinc-hue/miga-auto-workflow 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ RESEND_API_KEY 已配置"
else
    echo "⚠️  RESEND_API_KEY 未配置"
    echo ""
    echo "请输入您的 Resend API 密钥："
    read -p "> " RESEND_API_KEY_INPUT

    if [ -z "$RESEND_API_KEY_INPUT" ]; then
        echo "❌ API 密钥不能为空"
        exit 1
    fi

    gh secret set RESEND_API_KEY -b"$RESEND_API_KEY_INPUT" --repo aapeakinc-hue/miga-auto-workflow

    if [ $? -eq 0 ]; then
        echo "✅ RESEND_API_KEY 配置成功"
    else
        echo "❌ RESEND_API_KEY 配置失败"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "  ✅ 配置完成！"
echo "========================================="
echo ""
echo "📧 通知邮箱: $NOTIFICATION_EMAIL"
echo ""
echo "📅 自动通知时间："
echo "  - 每天 9:00（北京时间）- 客户开发工作流"
echo "  - 每天 11:00（北京时间）- 自动化运维"
echo ""
echo "🧪 测试通知："
echo "  方法1: 访问 https://github.com/aapeakinc-hue/miga-auto-workflow/actions"
echo "         点击 'Run workflow' 手动触发"
echo ""
echo "  方法2: 运行以下命令"
echo "         gh workflow run auto-workflow.yml"
echo ""
echo "📚 详细说明："
echo "  查看 NOTIFICATION_GUIDE.md"
echo ""
