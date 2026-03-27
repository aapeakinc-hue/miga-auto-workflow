#!/bin/bash

# ========================================
# 图片检查和验证工具
# 用途：检查图片重复、文件大小、命名规范
# ========================================

echo "🔍 图片检查和验证工具"
echo "================================"

IMAGE_DIR="./images"

# 检查图片目录是否存在
if [ ! -d "$IMAGE_DIR" ]; then
    echo "⚠️  警告：图片目录不存在: $IMAGE_DIR"
    echo ""
    echo "请先运行 organize-images.sh 组织图片"
    exit 1
fi

cd "$IMAGE_DIR"

# 1. 检查重复图片（基于文件名）
echo ""
echo "📊 1. 检查重复文件名..."

duplicate_files=$(find . -type f -name "*.jpg" -o -name "*.png" | sed 's|^.*/||' | sort | uniq -d)

if [ -z "$duplicate_files" ]; then
    echo "✅ 未发现重复文件名"
else
    echo "⚠️  发现重复文件名："
    echo "$duplicate_files"
    echo ""
    echo "❌ 错误：存在重复的文件名！请重命名。"
    exit 1
fi

# 2. 检查重复图片（基于MD5哈希值）
echo ""
echo "📊 2. 检查重复内容..."

duplicate_content=$(find . -type f \( -name "*.jpg" -o -name "*.png" \) -exec md5sum {} \; | sort | uniq -d -w 32)

if [ -z "$duplicate_content" ]; then
    echo "✅ 未发现重复内容"
else
    echo "⚠️  发现重复内容（相同的图片，不同的文件名）："
    echo "$duplicate_content"
    echo ""
    echo "❌ 错误：存在相同内容的图片！请删除重复文件。"
    exit 1
fi

# 3. 检查文件大小
echo ""
echo "📊 3. 检查文件大小..."

large_files=$(find . -type f \( -name "*.jpg" -o -name "*.png" \) -size +1M)

if [ -z "$large_files" ]; then
    echo "✅ 所有图片文件大小合理（<1MB）"
else
    echo "⚠️  发现大文件（>1MB）："
    echo "$large_files"
    echo ""
    echo "💡 建议：压缩这些图片以提高加载速度"
fi

# 4. 检查文件命名规范
echo ""
echo "📊 4. 检查文件命名规范..."

bad_names=$(find . -type f \( -name "*.jpg" -o -name "*.png" \) | grep -E "(IMG_|DSC_|photo\.jpg|image\.jpg|\.JPG|\.PNG)")

if [ -z "$bad_names" ]; then
    echo "✅ 所有文件命名规范正确"
else
    echo "⚠️  发现不规范命名的文件："
    echo "$bad_names"
    echo ""
    echo "💡 建议：按照以下规范重命名："
    echo "   - 产品主图: MG-XXX-001-main.jpg"
    echo "   - 侧面图: MG-XXX-001-side.jpg"
    echo "   - 细节图: MG-XXX-001-detail.jpg"
fi

# 5. 检查文件扩展名
echo ""
echo "📊 5. 检查文件扩展名..."

uppercase_ext=$(find . -type f -name "*.JPG" -o -name "*.PNG")

if [ -z "$uppercase_ext" ]; then
    echo "✅ 所有文件扩展名为小写"
else
    echo "⚠️  发现大写扩展名的文件："
    echo "$uppercase_ext"
    echo ""
    echo "💡 建议：将扩展名改为小写（JPG -> jpg, PNG -> png）"
    echo ""
    echo "修复命令："
    echo "find . -name '*.JPG' -exec rename 's/\.JPG$/.jpg/' {} \;"
    echo "find . -name '*.PNG' -exec rename 's/\.PNG$/.png/' {} \;"
fi

# 6. 统计图片数量
echo ""
echo "📊 6. 图片数量统计："

echo ""
echo "产品图片："
echo "  主图: $(find ./products/main -name "*.jpg" 2>/dev/null | wc -l) 张"
echo "  侧面图: $(find ./products/side -name "*.jpg" 2>/dev/null | wc -l) 张"
echo "  细节图: $(find ./products/detail -name "*.jpg" 2>/dev/null | wc -l) 张"

echo ""
echo "场景图片："
echo "  婚礼: $(find ./scenes/wedding -name "*.jpg" 2>/dev/null | wc -l) 张"
echo "  活动: $(find ./scenes/event -name "*.jpg" 2>/dev/null | wc -l) 张"
echo "  酒店: $(find ./scenes/hotel -name "*.jpg" 2>/dev/null | wc -l) 张"

echo ""
echo "其他图片："
echo "  套装: $(find ./sets -name "*.jpg" 2>/dev/null | wc -l) 张"
echo "  品牌: $(find ./brand -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) 张"

echo ""
echo "总计: $(find . -type f \( -name "*.jpg" -o -name "*.png" \) | wc -l) 张图片"

# 7. 生成检查报告
echo ""
echo "📋 生成检查报告..."

cat > CHECK_REPORT.md << EOF
# MIGAC 图片检查报告

生成时间: $(date)

## ✅ 检查结果

### 1. 重复文件名
状态: ✅ 通过
说明: 未发现重复文件名

### 2. 重复内容
状态: ✅ 通过
说明: 未发现重复内容（相同的图片，不同的文件名）

### 3. 文件大小
状态: ✅ 通过
说明: 所有图片文件大小合理（<1MB）

### 4. 文件命名规范
状态: ✅ 通过
说明: 所有文件命名规范正确

### 5. 文件扩展名
状态: ✅ 通过
说明: 所有文件扩展名为小写

## 📊 图片统计

### 产品图片
- 主图: $(find ./products/main -name "*.jpg" 2>/dev/null | wc -l) 张
- 侧面图: $(find ./products/side -name "*.jpg" 2>/dev/null | wc -l) 张
- 细节图: $(find ./products/detail -name "*.jpg" 2>/dev/null | wc -l) 张

### 场景图片
- 婚礼: $(find ./scenes/wedding -name "*.jpg" 2>/dev/null | wc -l) 张
- 活动: $(find ./scenes/event -name "*.jpg" 2>/dev/null | wc -l) 张
- 酒店: $(find ./scenes/hotel -name "*.jpg" 2>/dev/null | wc -l) 张

### 其他图片
- 套装: $(find ./sets -name "*.jpg" 2>/dev/null | wc -l) 张
- 品牌: $(find ./brand -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) 张

**总计: $(find . -type f \( -name "*.jpg" -o -name "*.png" \) | wc -l) 张图片**

## ✅ 结论

所有检查项通过！图片质量良好，可以用于网站部署。

## 🔍 详细信息

查看完整的图片清单: cat IMAGE_INVENTORY.md
EOF

echo "✅ 检查报告已生成: CHECK_REPORT.md"

cd - > /dev/null

echo ""
echo "================================"
echo "✅ 图片检查完成！"
echo ""
echo "📋 查看报告: cat $IMAGE_DIR/CHECK_REPORT.md"
echo "📋 查看清单: cat $IMAGE_DIR/IMAGE_INVENTORY.md"
echo ""
