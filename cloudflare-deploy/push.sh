#!/bin/bash

# 最简单的 GitHub 推送脚本

echo "🚀 开始推送到 GitHub..."

# 检查是否在正确的目录
cd "$(dirname "$0")"

# 添加远程仓库
echo "📦 添加远程仓库..."
git remote add origin https://github.com/aapeakinc-hue/miga-website-optimized.git

# 推送代码
echo "⬆️  推送代码到 GitHub..."
git push -u origin main

echo "✅ 完成！"
echo ""
echo "🌐 访问你的仓库：https://github.com/aapeakinc-hue/miga-website-optimized"
