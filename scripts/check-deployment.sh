#!/bin/bash

# Cloudflare Pages 部署检查脚本

echo "🚀 MIGAC 网站部署检查"
echo "===================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查域名
echo "📋 检查 1: 域名 DNS 配置"
echo "----------------------------"
if command -v dig &> /dev/null; then
    DNS_RESULT=$(dig miga.cc +short)
    if [ -n "$DNS_RESULT" ]; then
        echo -e "${GREEN}✅ DNS 记录存在: $DNS_RESULT${NC}"
    else
        echo -e "${RED}❌ DNS 记录未找到${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  dig 命令未安装，跳过 DNS 检查${NC}"
fi
echo ""

# 检查 HTTP 响应
echo "📋 检查 2: HTTP 响应"
echo "----------------------------"
if command -v curl &> /dev/null; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://miga.cc)
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✅ 主页 HTTP 状态码: 200${NC}"
    else
        echo -e "${RED}❌ 主页 HTTP 状态码: $HTTP_CODE${NC}"
    fi

    PRODUCTS_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://miga.cc/products.html)
    if [ "$PRODUCTS_CODE" = "200" ]; then
        echo -e "${GREEN}✅ 产品页 HTTP 状态码: 200${NC}"
    else
        echo -e "${RED}❌ 产品页 HTTP 状态码: $PRODUCTS_CODE${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl 命令未安装，跳过 HTTP 检查${NC}"
fi
echo ""

# 检查页面内容
echo "📋 检查 3: 页面内容"
echo "----------------------------"
if command -v curl &> /dev/null; then
    # 检查主页内容
    HOME_CONTENT=$(curl -s https://miga.cc)
    if echo "$HOME_CONTENT" | grep -q "MIGAC"; then
        echo -e "${GREEN}✅ 主页包含品牌名称${NC}"
    else
        echo -e "${RED}❌ 主页未找到品牌名称${NC}"
    fi

    if echo "$HOME_CONTENT" | grep -q "产品展示"; then
        echo -e "${GREEN}✅ 主页包含产品展示区域${NC}"
    else
        echo -e "${RED}❌ 主页未找到产品展示区域${NC}"
    fi

    if echo "$HOME_CONTENT" | grep -q "WhatsApp"; then
        echo -e "${GREEN}✅ 主页包含 WhatsApp 联系${NC}"
    else
        echo -e "${RED}❌ 主页未找到 WhatsApp 联系${NC}"
    fi

    # 检查产品页内容
    PRODUCTS_CONTENT=$(curl -s https://miga.cc/products.html)
    if echo "$PRODUCTS_CONTENT" | grep -q "产品目录"; then
        echo -e "${GREEN}✅ 产品页包含产品目录${NC}"
    else
        echo -e "${RED}❌ 产品页未找到产品目录${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl 命令未安装，跳过内容检查${NC}"
fi
echo ""

# 检查 SSL 证书
echo "📋 检查 4: SSL 证书"
echo "----------------------------"
if command -v curl &> /dev/null; then
    SSL_INFO=$(curl -sI https://miga.cc | grep -i ssl)
    if [ -n "$SSL_INFO" ]; then
        echo -e "${GREEN}✅ SSL 证书已启用${NC}"
        echo "   $SSL_INFO"
    else
        echo -e "${RED}❌ SSL 证书未检测到${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl 命令未安装，跳过 SSL 检查${NC}"
fi
echo ""

# 检查本地文件
echo "📋 检查 5: 本地部署文件"
echo "----------------------------"
if [ -f "cloudflare-deploy/index.html" ]; then
    INDEX_SIZE=$(du -h cloudflare-deploy/index.html | cut -f1)
    echo -e "${GREEN}✅ index.html 存在 ($INDEX_SIZE)${NC}"
else
    echo -e "${RED}❌ index.html 不存在${NC}"
fi

if [ -f "cloudflare-deploy/products.html" ]; then
    PRODUCTS_SIZE=$(du -h cloudflare-deploy/products.html | cut -f1)
    echo -e "${GREEN}✅ products.html 存在 ($PRODUCTS_SIZE)${NC}"
else
    echo -e "${RED}❌ products.html 不存在${NC}"
fi
echo ""

# 总结
echo "===================="
echo "📊 检查完成！"
echo ""
echo "📌 下一步操作："
echo "1. 在浏览器中访问 https://miga.cc"
echo "2. 检查页面是否正常显示"
echo "3. 测试所有功能（表单、链接等）"
echo "4. 在移动设备上测试响应式布局"
echo ""
echo "📚 需要帮助？"
echo "   📖 查看部署指南: docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md"
echo "   📧 联系: info@miga.cc"
echo ""
