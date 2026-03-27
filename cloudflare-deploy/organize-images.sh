#!/bin/bash

# ========================================
# 图片重命名和组织脚本
# 用途：批量重命名图片并组织到正确的目录
# ========================================

# 配置
SOURCE_DIR="./images-source"  # 原始图片目录
TARGET_DIR="./images"        # 目标目录
PRODUCT_COUNT=50             # 产品数量

echo "📸 图片重命名和组织工具"
echo "================================"

# 创建目录结构
echo ""
echo "📁 创建目录结构..."
mkdir -p "$TARGET_DIR/products/main"
mkdir -p "$TARGET_DIR/products/side"
mkdir -p "$TARGET_DIR/products/detail"
mkdir -p "$TARGET_DIR/sets"
mkdir -p "$TARGET_DIR/scenes/wedding"
mkdir -p "$TARGET_DIR/scenes/event"
mkdir -p "$TARGET_DIR/scenes/hotel"
mkdir -p "$TARGET_DIR/brand"
mkdir -p "$TARGET_DIR/brand/factory"

echo "✅ 目录结构创建完成"

# 检查是否有原始图片
if [ ! -d "$SOURCE_DIR" ]; then
    echo ""
    echo "⚠️  警告：原始图片目录不存在: $SOURCE_DIR"
    echo ""
    echo "请执行以下步骤："
    echo "1. 创建原始图片目录: mkdir -p $SOURCE_DIR"
    echo "2. 将所有产品图片放到该目录"
    echo "3. 按以下命名格式命名："
    echo "   - 产品主图: MG-9A-001-main.jpg"
    echo "   - 侧面图: MG-9A-001-side.jpg"
    echo "   - 细节图: MG-9A-001-detail.jpg"
    echo ""
    exit 1
fi

# 产品图片组织
echo ""
echo "📦 组织产品图片..."
cd "$SOURCE_DIR"

# 主图
if ls MG-*-main.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 MG-*-main.jpg | wc -l) 张主图"
    cp MG-*-main.jpg "$TARGET_DIR/products/main/"
else
    echo "⚠️  未找到主图 (MG-*-main.jpg)"
fi

# 侧面图
if ls MG-*-side.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 MG-*-side.jpg | wc -l) 张侧面图"
    cp MG-*-side.jpg "$TARGET_DIR/products/side/"
else
    echo "⚠️  未找到侧面图 (MG-*-side.jpg)"
fi

# 细节图
if ls MG-*-detail.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 MG-*-detail.jpg | wc -l) 张细节图"
    cp MG-*-detail.jpg "$TARGET_DIR/products/detail/"
else
    echo "⚠️  未找到细节图 (MG-*-detail.jpg)"
fi

# 场景图片组织
echo ""
echo "🎨 组织场景图片..."

# 婚礼场景
if ls scene-wedding-*.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 scene-wedding-*.jpg | wc -l) 张婚礼场景图"
    cp scene-wedding-*.jpg "$TARGET_DIR/scenes/wedding/"
fi

# 活动场景
if ls scene-event-*.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 scene-event-*.jpg | wc -l) 张活动场景图"
    cp scene-event-*.jpg "$TARGET_DIR/scenes/event/"
fi

# 酒店场景
if ls scene-hotel-*.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 scene-hotel-*.jpg | wc -l) 张酒店场景图"
    cp scene-hotel-*.jpg "$TARGET_DIR/scenes/hotel/"
fi

# 套装图片
echo ""
echo "💒 组织套装图片..."
if ls set-*.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 set-*.jpg | wc -l) 张套装图"
    cp set-*.jpg "$TARGET_DIR/sets/"
fi

# 品牌图片
echo ""
echo "🏷️  组织品牌图片..."
if ls logo-*.png 1> /dev/null 2>&1; then
    echo "✅ 找到 Logo 文件"
    cp logo-*.png "$TARGET_DIR/brand/"
fi

if ls factory-*.jpg 1> /dev/null 2>&1; then
    echo "✅ 找到 $(ls -1 factory-*.jpg | wc -l) 张工厂照片"
    cp factory-*.jpg "$TARGET_DIR/brand/factory/"
fi

cd - > /dev/null

# 生成图片清单
echo ""
echo "📋 生成图片清单..."
cat > "$TARGET_DIR/IMAGE_INVENTORY.md" << EOF
# MIGAC 图片清单

生成时间: $(date)

## 产品图片

### 主图 (\`products/main/\`)

| SKU | 文件名 | 状态 |
|-----|--------|------|
EOF

cd "$TARGET_DIR/products/main"
for file in MG-*.jpg; do
    if [ -f "$file" ]; then
        sku=$(echo "$file" | sed 's/-main\.jpg$//' | tr '[:lower:]' '[:upper:]')
        echo "| $sku | $file | ✅ |" >> ../../IMAGE_INVENTORY.md
    fi
done

cd - > /dev/null

echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "### 侧面图 (\`products/side/\`)" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "| SKU | 文件名 | 状态 |" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "|-----|--------|------|" >> "$TARGET_DIR/IMAGE_INVENTORY.md"

cd "$TARGET_DIR/products/side"
for file in MG-*.jpg; do
    if [ -f "$file" ]; then
        sku=$(echo "$file" | sed 's/-side\.jpg$//' | tr '[:lower:]' '[:upper:]')
        echo "| $sku | $file | ✅ |" >> ../../IMAGE_INVENTORY.md
    fi
done

cd - > /dev/null

echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "### 细节图 (\`products/detail/\`)" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "| SKU | 文件名 | 状态 |" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "|-----|--------|------|" >> "$TARGET_DIR/IMAGE_INVENTORY.md"

cd "$TARGET_DIR/products/detail"
for file in MG-*.jpg; do
    if [ -f "$file" ]; then
        sku=$(echo "$file" | sed 's/-detail\.jpg$//' | tr '[:lower:]' '[:upper:]')
        echo "| $sku | $file | ✅ |" >> ../../IMAGE_INVENTORY.md
    fi
done

cd - > /dev/null

echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "## 场景图片" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "### 婚礼场景 (\`scenes/wedding/\`)" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "| 文件名 | 用途 | 状态 |" >> "$TARGET_DIR/IMAGE_INVENTORY.md"
echo "|--------|------|------|" >> "$TARGET_DIR/IMAGE_INVENTORY.md"

cd "$TARGET_DIR/scenes/wedding"
for file in scene-*.jpg; do
    if [ -f "$file" ]; then
        echo "| $file | 产品详情页/场景展示 | ✅ |" >> ../../../IMAGE_INVENTORY.md
    fi
done

cd - > /dev/null

echo "✅ 图片清单已生成: $TARGET_DIR/IMAGE_INVENTORY.md"

# 检查重复图片
echo ""
echo "🔍 检查重复图片..."
cd "$TARGET_DIR"

# 查找重复的MD5哈希值
find . -type f \( -name "*.jpg" -o -name "*.png" \) -exec md5sum {} \; | sort | uniq -d -w 32 > duplicate-check.txt

if [ -s duplicate-check.txt ]; then
    echo "⚠️  发现重复图片！"
    echo "重复文件："
    cat duplicate-check.txt
    echo ""
    echo "请删除重复文件，确保每个图片都是唯一的。"
else
    echo "✅ 未发现重复图片"
fi

rm -f duplicate-check.txt

cd - > /dev/null

# 统计信息
echo ""
echo "📊 图片统计："
echo ""
echo "产品图片："
echo "  主图: $(ls -1 $TARGET_DIR/products/main/*.jpg 2>/dev/null | wc -l) 张"
echo "  侧面图: $(ls -1 $TARGET_DIR/products/side/*.jpg 2>/dev/null | wc -l) 张"
echo "  细节图: $(ls -1 $TARGET_DIR/products/detail/*.jpg 2>/dev/null | wc -l) 张"
echo ""
echo "场景图片："
echo "  婚礼: $(ls -1 $TARGET_DIR/scenes/wedding/*.jpg 2>/dev/null | wc -l) 张"
echo "  活动: $(ls -1 $TARGET_DIR/scenes/event/*.jpg 2>/dev/null | wc -l) 张"
echo "  酒店: $(ls -1 $TARGET_DIR/scenes/hotel/*.jpg 2>/dev/null | wc -l) 张"
echo ""
echo "套装图片: $(ls -1 $TARGET_DIR/sets/*.jpg 2>/dev/null | wc -l) 张"
echo "品牌图片: $(ls -1 $TARGET_DIR/brand/*.{jpg,png} 2>/dev/null | wc -l) 张"
echo ""
echo "总计: $(find $TARGET_DIR -type f \( -name "*.jpg" -o -name "*.png" \) | wc -l) 张图片"

echo ""
echo "================================"
echo "✅ 图片组织完成！"
echo ""
echo "下一步："
echo "1. 查看图片清单: cat $TARGET_DIR/IMAGE_INVENTORY.md"
echo "2. 检查图片质量"
echo "3. 更新HTML文件中的图片路径"
echo ""
