#!/bin/bash

# ========================================
# Formspree 表单配置脚本
# ========================================

# 你的 Formspree Form ID（从 Formspree Dashboard 获取）
FORM_ID="mgopvdqo"

# 备份原文件
echo "📦 备份原文件..."
cp cloudflare-deploy/free-audit.html cloudflare-deploy/free-audit.html.backup
cp cloudflare-deploy/catalog.html cloudflare-deploy/catalog.html.backup
cp cloudflare-deploy/request-sample.html cloudflare-deploy/request-sample.html.backup

# 更新 free-audit.html
echo "🔧 更新 free-audit.html..."
sed -i "s|https://formspree.io/f/YOUR_FORM_ID|https://formspree.io/f/${FORM_ID}|g" cloudflare-deploy/free-audit.html

# 更新 catalog.html
echo "🔧 更新 catalog.html..."
sed -i "s|https://formspree.io/f/YOUR_FORM_ID|https://formspree.io/f/${FORM_ID}|g" cloudflare-deploy/catalog.html

# 更新 request-sample.html
echo "🔧 更新 request-sample.html..."
sed -i "s|https://formspree.io/f/YOUR_FORM_ID|https://formspree.io/f/${FORM_ID}|g" cloudflare-deploy/request-sample.html

echo "✅ 配置完成！"
echo ""
echo "📝 更新的文件："
echo "  - cloudflare-deploy/free-audit.html"
echo "  - cloudflare-deploy/catalog.html"
echo "  - cloudflare-deploy/request-sample.html"
echo ""
echo "🔍 验证配置："
echo "  grep 'formspree.io' cloudflare-deploy/free-audit.html | head -1"
