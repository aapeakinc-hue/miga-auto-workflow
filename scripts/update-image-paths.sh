#!/bin/bash

# 更新HTML中的图片路径
# 此脚本会自动更新 contact-optimized.html 和 products.html 中的图片路径

echo "🔄 更新 HTML 中的图片路径"
echo "========================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查文件
if [ ! -f "cloudflare-deploy/index.html" ]; then
    echo -e "${RED}❌ cloudflare-deploy/index.html 不存在${NC}"
    exit 1
fi

if [ ! -f "cloudflare-deploy/products.html" ]; then
    echo -e "${RED}❌ cloudflare-deploy/products.html 不存在${NC}"
    exit 1
fi

# 备份原始文件
echo "📦 备份原始文件..."
cp cloudflare-deploy/index.html cloudflare-deploy/index.html.backup
cp cloudflare-deploy/products.html cloudflare-deploy/products.html.backup
echo -e "${GREEN}✅ 备份完成${NC}"
echo ""

# 替换函数
replace_images() {
    local FILE=$1
    local COUNT=0
    
    echo "🔄 处理文件: $FILE"
    
    # 替换占位图片为真实图片路径
    # 使用 sed 进行替换
    
    # contact-optimized.html 的替换（6张图片）
    if [[ "$FILE" == *"index.html"* ]]; then
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Candle\+Holder|/images/crystal-candle-holder.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Luxury\+Candelabra|/images/luxury-candelabra.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Tealight|/images/crystal-tealight.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Centerpiece|/images/crystal-decor.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Wall\+Sconce|/images/crystal-wall-sconce.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Chandelier|/images/crystal-chandelier.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
    fi
    
    # products.html 的替换（8张图片）
    if [[ "$FILE" == *"products.html"* ]]; then
        sed -i 's|https://via\.placeholder\.com/400x300?text=Classic\+Candle\+Holder|/images/crystal-candle-holder-001.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Luxury\+Candelabra|/images/luxury-candelabra-002.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Tealight|/images/crystal-tealight-003.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Centerpiece|/images/crystal-decor-004.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Crystal\+Chandelier|/images/crystal-chandelier-005.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Modern\+Candle\+Holder|/images/modern-candle-holder-006.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Royal\+Candelabra|/images/royal-candelabra-007.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
        
        sed -i 's|https://via\.placeholder\.com/400x300?text=Colorful\+Tealight|/images/colorful-tealight-008.jpg|g' "$FILE"
        COUNT=$((COUNT + 1))
    fi
    
    echo -e "${GREEN}✅ 已替换 $COUNT 处图片路径${NC}"
    echo ""
}

# 执行替换
replace_images "cloudflare-deploy/index.html"
replace_images "cloudflare-deploy/products.html"

# 验证替换结果
echo "📊 验证替换结果..."
echo ""

echo "index.html 中的图片路径:"
grep -o 'src="/images/[^"]*"' cloudflare-deploy/index.html | head -6
echo ""

echo "products.html 中的图片路径:"
grep -o 'src="/images/[^"]*"' cloudflare-deploy/products.html | head -8
echo ""

# 检查是否还有未替换的占位图片
REMAINING=$(grep -c "via.placeholder.com" cloudflare-deploy/index.html cloudflare-deploy/products.html 2>/dev/null || echo "0")

if [ "$REMAINING" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  仍有 $REMAINING 处未替换的占位图片${NC}"
    echo "请手动检查并替换"
else
    echo -e "${GREEN}✅ 所有占位图片已替换完成！${NC}"
fi

echo ""
echo "========================"
echo "更新完成！"
echo "========================"
echo ""
echo "备份文件位置："
echo "  - cloudflare-deploy/index.html.backup"
echo "  - cloudflare-deploy/products.html.backup"
echo ""
echo "如需恢复，执行："
echo "  mv cloudflare-deploy/index.html.backup cloudflare-deploy/index.html"
echo "  mv cloudflare-deploy/products.html.backup cloudflare-deploy/products.html"
echo ""
echo "下一步："
echo "  1. 验证图片路径是否正确"
echo "  2. 将 cloudflare-deploy 目录上传到 Cloudflare Pages"
echo "  3. 测试网站访问"
echo ""
