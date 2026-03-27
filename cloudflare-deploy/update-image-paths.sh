#!/bin/bash

# ========================================
# HTML图片路径更新脚本
# 用途：批量更新HTML文件中的图片路径
# ========================================

echo "🔄 HTML图片路径更新工具"
echo "================================"

# 定义图片路径映射
# 旧路径 -> 新路径

echo ""
echo "📋 更新 product-template.html..."
if [ -f "product-template.html" ]; then
    # 创建备份
    cp product-template.html product-template.html.backup

    # 更新图片路径
    sed -i 's|🕯️|<img src="images/products/main/MG-9A-001-main.jpg" alt="MG-9A-001 9-Arms Crystal Candelabra">|g' product-template.html

    echo "✅ product-template.html 已更新"
    echo "📦 备份文件: product-template.html.backup"
else
    echo "⚠️  product-template.html 不存在"
fi

echo ""
echo "📋 更新 best-sellers.html..."
if [ -f "best-sellers.html" ]; then
    # 创建备份
    cp best-sellers.html best-sellers.html.backup

    # 这里需要根据实际产品数量批量替换
    # 示例：替换第一个产品的图片
    sed -i 's|product-1-image|<img src="images/products/main/MG-9A-001-main.jpg" alt="MG-9A-001">|g' best-sellers.html

    echo "✅ best-sellers.html 已更新"
    echo "📦 备份文件: best-sellers.html.backup"
else
    echo "⚠️  best-sellers.html 不存在"
fi

echo ""
echo "📋 更新 wedding-collection.html..."
if [ -f "wedding-collection.html" ]; then
    # 创建备份
    cp wedding-collection.html wedding-collection.html.backup

    # 更新套装图片
    sed -i 's|💒|<img src="images/sets/set-classic-romantic.jpg" alt="Classic Romantic Wedding Set">|g' wedding-collection.html
    sed -i 's|👑|<img src="images/sets/set-grand-luxury.jpg" alt="Grand Luxury Wedding Set">|g' wedding-collection.html
    sed -i 's|🎨|<img src="images/sets/set-modern-elegant.jpg" alt="Modern Elegant Wedding Set">|g' wedding-collection.html

    echo "✅ wedding-collection.html 已更新"
    echo "📦 备份文件: wedding-collection.html.backup"
else
    echo "⚠️  wedding-collection.html 不存在"
fi

echo ""
echo "================================"
echo "✅ 所有HTML文件已更新！"
echo ""
echo "📝 下一步："
echo "1. 检查更新后的HTML文件"
echo "2. 在浏览器中预览"
echo "3. 验证所有图片路径正确"
echo ""
echo "🔍 验证命令："
echo "grep -r 'images/' *.html"
echo ""
