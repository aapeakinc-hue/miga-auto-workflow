#!/bin/bash

# Cloudflare Worker 快速部署脚本
# 用于快速部署和测试 Cloudflare Worker

echo "☁️  Cloudflare Worker 快速部署向导"
echo "===================================="
echo ""

# 检查是否安装了 wrangler
if ! command -v wrangler &> /dev/null; then
    echo "❌ 未检测到 wrangler CLI"
    echo ""
    echo "请先安装 wrangler:"
    echo "  npm install -g wrangler"
    exit 1
fi

echo "✅ 已检测到 wrangler CLI"
echo ""

# 进入 cloudflare 目录
cd "$(dirname "$0")"

# 检查 wrangler.toml 是否存在
if [ ! -f "wrangler.toml" ]; then
    echo "❌ 未找到 wrangler.toml 配置文件"
    exit 1
fi

echo "✅ 找到配置文件: wrangler.toml"
echo ""

# 显示当前配置
echo "📋 当前配置:"
echo ""
cat wrangler.toml
echo ""

# 询问是否部署
read -p "是否部署 Worker? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⏭️  取消部署"
    exit 0
fi

echo ""
echo "🚀 开始部署..."
echo ""

# 部署 Worker
wrangler deploy

# 检查部署是否成功
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Worker 部署成功!"
    echo ""
    echo "📋 下一步:"
    echo "1. 测试 Worker: curl https://miga-auto-workflow.YOUR_ACCOUNT.workers.dev/api/test"
    echo "2. 查看 Cloudflare 控制台配置 Cron Triggers"
    echo "3. 配置 API 端点（如果需要）"
    echo ""
    echo "📖 详细文档: cloudflare/DEPLOYMENT_GUIDE.md"
else
    echo ""
    echo "❌ Worker 部署失败"
    echo ""
    echo "请检查:"
    echo "1. 是否已登录 Cloudflare: wrangler login"
    echo "2. 网络连接是否正常"
    echo "3. wrangler.toml 配置是否正确"
    exit 1
fi
