#!/bin/bash

# 图片准备脚本 - MIGAC
# 此脚本帮助准备网站所需的产品图片

echo "🚀 MIGAC 网站图片准备脚本"
echo "========================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 图片列表
IMAGES=(
    # 联系页面图片（6张）
    "crystal-candle-holder.jpg:经典水晶烛台"
    "luxury-candelabra.jpg:奢华水晶吊灯烛台"
    "crystal-tealight.jpg:水晶茶烛灯"
    "crystal-decor.jpg:水晶装饰摆件"
    "crystal-wall-sconce.jpg:水晶壁灯"
    "crystal-chandelier.jpg:水晶吊灯"
    
    # 产品页面图片（8张）
    "crystal-candle-holder-001.jpg:CH-001"
    "luxury-candelabra-002.jpg:CD-002"
    "crystal-tealight-003.jpg:TL-003"
    "crystal-decor-004.jpg:DP-004"
    "crystal-chandelier-005.jpg:CHL-005"
    "modern-candle-holder-006.jpg:CH-006"
    "royal-candelabra-007.jpg:CD-007"
    "colorful-tealight-008.jpg:TL-008"
)

# 检查目录
echo "📋 检查目录结构..."
if [ ! -d "cloudflare-deploy" ]; then
    echo -e "${RED}❌ cloudflare-deploy 目录不存在${NC}"
    echo "请先创建 cloudflare-deploy 目录"
    exit 1
fi

if [ ! -d "cloudflare-deploy/images" ]; then
    echo -e "${YELLOW}⚠️  创建 images 目录...${NC}"
    mkdir -p cloudflare-deploy/images
    echo -e "${GREEN}✅ images 目录已创建${NC}"
else
    echo -e "${GREEN}✅ images 目录已存在${NC}"
fi

echo ""

# 检查现有图片
echo "📊 检查现有图片..."
FOUND=0
MISSING=0

for IMAGE_INFO in "${IMAGES[@]}"; do
    IMAGE_NAME="${IMAGE_INFO%%:*}"
    IMAGE_DESC="${IMAGE_INFO##*:}"
    
    if [ -f "cloudflare-deploy/images/$IMAGE_NAME" ]; then
        FOUND=$((FOUND + 1))
        SIZE=$(du -h "cloudflare-deploy/images/$IMAGE_NAME" | cut -f1)
        echo -e "${GREEN}✅${NC} $IMAGE_NAME ($SIZE) - $IMAGE_DESC"
    else
        MISSING=$((MISSING + 1))
        echo -e "${RED}❌${NC} $IMAGE_NAME - $IMAGE_DESC"
    fi
done

echo ""
echo "========================"
echo -e "已找到: ${GREEN}$FOUND${NC}/14 张图片"
echo -e "缺失: ${RED}$MISSING${NC}/14 张图片"
echo "========================"
echo ""

if [ $FOUND -eq 14 ]; then
    echo -e "${GREEN}🎉 所有图片已准备完毕！${NC}"
    echo ""
    echo "下一步："
    echo "1. 验证图片质量"
    echo "2. 更新HTML文件中的图片路径"
    echo "3. 部署到Cloudflare Pages"
    echo ""
    exit 0
fi

echo -e "${YELLOW}📝 缺失图片准备指南：${NC}"
echo ""
echo "方式1: 使用占位图片（快速测试）"
echo "  - 将使用在线占位图片服务"
echo "  - 适合快速测试和预览"
echo ""

echo "方式2: 拍摄真实产品图片（推荐）"
echo "  - 拍摄或准备14张产品图片"
echo "  - 尺寸: 800x600px 或 400x300px"
echo "  - 格式: JPEG/PNG"
echo "  - 大小: 100-300KB"
echo "  - 复制到: cloudflare-deploy/images/"
echo ""

echo "方式3: 使用供应商图片（快速）"
echo "  - 从阿里巴巴、Made-in-China等平台获取"
echo "  - 确保获得授权"
echo "  - 下载并重命名"
echo ""

echo "详细指南请查看："
echo "  - docs/PRODUCT_IMAGE_GUIDE.md"
echo "  - cloudflare-deploy/IMAGE_PREPARATION_CHECKLIST.md"
echo ""

echo "搜索链接："
echo "  - 阿里巴巴: https://www.alibaba.com/showroom/crystal-candle-holder.html"
echo "  - Google Images: https://www.google.com/search?tbm=isch&q=crystal+candle+holder"
echo ""

# 询问是否创建占位图片
read -p "是否创建占位图片用于测试？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📝 创建占位图片..."
    echo ""
    
    for IMAGE_INFO in "${IMAGES[@]}"; do
        IMAGE_NAME="${IMAGE_INFO%%:*}"
        IMAGE_DESC="${IMAGE_INFO##*:}"
        
        if [ ! -f "cloudflare-deploy/images/$IMAGE_NAME" ]; then
            # 创建简单的占位图片（使用ImageMagick）
            if command -v convert &> /dev/null; then
                convert -size 400x300 xc:#f0f0f0 \
                    -gravity center \
                    -pointsize 24 \
                    -fill "#333" \
                    -annotate +0+0 "$IMAGE_DESC" \
                    -pointsize 12 \
                    -annotate +0+30 "$IMAGE_NAME" \
                    "cloudflare-deploy/images/$IMAGE_NAME"
                
                if [ $? -eq 0 ]; then
                    SIZE=$(du -h "cloudflare-deploy/images/$IMAGE_NAME" | cut -f1)
                    echo -e "${GREEN}✅${NC} 创建: $IMAGE_NAME ($SIZE)"
                else
                    echo -e "${RED}❌${NC} 创建失败: $IMAGE_NAME"
                fi
            else
                echo -e "${YELLOW}⚠️${NC} ImageMagick 未安装，跳过: $IMAGE_NAME"
                echo "   请手动准备图片或安装 ImageMagick:"
                echo "   sudo apt install imagemagick"
            fi
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ 占位图片创建完成！${NC}"
    echo ""
    echo "注意: 这些只是占位图片，用于测试和预览。"
    echo "请尽快替换为真实的产品图片。"
    echo ""
fi

echo ""
echo "========================"
echo "准备完成！"
echo "========================"
echo ""
echo "下一步："
echo "1. 如果使用占位图片：直接部署测试"
echo "2. 如果准备真实图片：复制到 cloudflare-deploy/images/"
echo "3. 运行: ./scripts/update-image-paths.sh 更新HTML"
echo "4. 部署到 Cloudflare Pages"
echo ""
