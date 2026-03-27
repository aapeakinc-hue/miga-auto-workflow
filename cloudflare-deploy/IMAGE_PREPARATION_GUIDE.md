# 📸 MIGAC 图片准备和管理方案

## 🎯 核心原则

**绝对禁止**：在catalog或产品页面中使用重复图片

**必须做到**：
- ✅ 每个产品（SKU）有唯一的产品图片
- ✅ 每个套装有独特的组合图片
- ✅ 每个场景有不同的应用图片
- ✅ 图片命名规范清晰
- ✅ 图片SEO优化（alt标签）

---

## 📊 图片需求清单

### 1. 产品图片（必填）

#### 主产品图片
- **数量**：50+ 张（每个SKU一张）
- **用途**：产品卡片、产品详情页
- **规格**：
  - 尺寸：800x600px 或 1000x1000px
  - 格式：JPG（质量85%）或 WebP
  - 背景：纯白色背景 (#FFFFFF)
  - 拍摄角度：正面45度角
  - 命名规范：`MG-XXX-001-main.jpg`

#### 产品细节图片
- **数量**：150+ 张（每个SKU 3-5张）
- **用途**：产品详情页缩略图
- **规格**：
  - 尺寸：800x600px
  - 角度：侧面、背面、细节特写
  - 命名规范：`MG-XXX-001-side.jpg`、`MG-XXX-001-detail.jpg`

---

### 2. 场景图片（强烈推荐）

#### 婚礼场景图片
- **数量**：20-30 张
- **用途**：Wedding Collection页面、产品详情页
- **内容**：
  - 婚礼餐桌布置
  - 实际使用效果
  - 不同场地（花园、室内、海滩）
- **规格**：
  - 尺寸：1200x800px 或 1920x1080px
  - 格式：JPG（质量90%）
  - 命名规范：`scene-wedding-001.jpg`、`scene-wedding-garden.jpg`

#### 活动场景图片
- **数量**：15-20 张
- **用途**：产品详情页、案例研究
- **内容**：
  - 公司活动
  - 晚宴场景
  - 会议布置
- **命名规范**：`scene-event-001.jpg`

#### 酒店场景图片
- **数量**：15-20 张
- **用途**：酒店客户专用页面
- **内容**：
  - 酒店大堂
  - 宴会厅
  - VIP客房
- **命名规范：`scene-hotel-001.jpg`

---

### 3. 套装图片（必填）

#### 完整套装图片
- **数量**：3-5 张（每个套装一张）
- **用途**：Wedding Collection页面
- **内容**：
  - Classic Romantic Set
  - Grand Luxury Set
  - Modern Elegant Set
- **规格**：
  - 尺寸：1000x800px
  - 包含：烛台 + 花架 + 蜡烛
  - 命名规范：`set-classic-romantic.jpg`、`set-grand-luxury.jpg`

---

### 4. 品牌图片（选填）

#### Logo
- **数量**：2 张（横向和纵向）
- **用途**：网站头部、邮件签名
- **规格**：
  - 横向：200x60px（PNG透明背景）
  - 纵向：100x100px（圆形，PNG透明背景）
  - 命名：`logo-horizontal.png`、`logo-vertical.png`

#### 工厂照片
- **数量**：5-10 张
- **用途**：关于我们页面、信任背书
- **内容**：
  - 工厂外观
  - 生产线
  - 质检环节
  - 仓库
  - ISO证书
- **命名规范：`factory-exterior.jpg`、`production-line.jpg`

---

## 📁 目录结构方案

### 方案1：按类型组织（推荐）
```
cloudflare-deploy/
├── images/
│   ├── products/              # 产品图片
│   │   ├── main/              # 主图
│   │   │   ├── MG-9A-001-main.jpg
│   │   │   ├── MG-9A-002-main.jpg
│   │   │   └── ...
│   │   ├── side/              # 侧面图
│   │   │   ├── MG-9A-001-side.jpg
│   │   │   └── ...
│   │   └── detail/            # 细节图
│   │       ├── MG-9A-001-detail.jpg
│   │       └── ...
│   ├── sets/                 # 套装图片
│   │   ├── set-classic-romantic.jpg
│   │   ├── set-grand-luxury.jpg
│   │   └── set-modern-elegant.jpg
│   ├── scenes/               # 场景图片
│   │   ├── wedding/
│   │   │   ├── scene-wedding-001.jpg
│   │   │   └── ...
│   │   ├── event/
│   │   │   ├── scene-event-001.jpg
│   │   │   └── ...
│   │   └── hotel/
│   │       ├── scene-hotel-001.jpg
│   │       └── ...
│   ├── brand/                # 品牌图片
│   │   ├── logo-horizontal.png
│   │   ├── logo-vertical.png
│   │   └── factory/
│   │       ├── factory-exterior.jpg
│   │       └── ...
│   └── icons/                # 图标
│       ├── check.png
│       └── arrow.png
```

### 方案2：按产品组织（适合大量产品）
```
cloudflare-deploy/
├── images/
│   ├── MG-9A-001/            # 产品专属文件夹
│   │   ├── main.jpg
│   │   ├── side.jpg
│   │   ├── detail.jpg
│   │   └── scene-wedding.jpg
│   ├── MG-9A-002/
│   │   ├── main.jpg
│   │   ├── side.jpg
│   │   └── detail.jpg
│   ├── MG-12A-001/
│   │   └── ...
│   ├── sets/                 # 套装图片
│   │   ├── classic-romantic.jpg
│   │   └── ...
│   └── scenes/               # 场景图片
│       ├── wedding-001.jpg
│       └── ...
```

---

## 🎨 图片规格详细要求

### 产品图片

| 规格 | 要求 | 说明 |
|------|------|------|
| **尺寸** | 800x600px 或 1000x1000px | 正方形或4:3比例 |
| **格式** | JPG（85%质量）或 WebP | 平衡质量和文件大小 |
| **背景** | 纯白色 (#FFFFFF) | 便于后期合成和SEO |
| **拍摄角度** | 正面45度角 | 展示产品最佳角度 |
| **光线** | 柔和均匀光线 | 避免过曝和阴影 |
| **清晰度** | 至少72 DPI，建议150 DPI | 保证缩放后清晰 |
| **文件大小** | 不超过500KB | 加载速度优化 |
| **文件名** | 小写字母，用连字符分隔 | SEO友好 |

### 场景图片

| 规格 | 要求 | 说明 |
|------|------|------|
| **尺寸** | 1200x800px 或 1920x1080px | 高清展示 |
| **格式** | JPG（90%质量） | 保证高质量 |
| **内容** | 真实使用场景 | 增强可信度 |
| **构图** | 产品居中或黄金分割 | 突出产品 |
| **光线** | 自然光或专业灯光 | 营造氛围 |
| **文件大小** | 不超过1MB | 加载优化 |

---

## 🔍 图片SEO优化

### Alt标签（必填）

每个图片都必须添加alt标签：

```html
<!-- 产品主图 -->
<img src="images/products/main/MG-9A-001-main.jpg"
     alt="MG-9A-001 9-Arms Crystal Candelabra - Premium K9 crystal candle holder for weddings and events">

<!-- 场景图片 -->
<img src="images/scenes/wedding/scene-wedding-001.jpg"
     alt="Wedding centerpiece decoration with MG-9A-001 crystal candelabra in romantic garden setting">

<!-- 套装图片 -->
<img src="images/sets/set-classic-romantic.jpg"
     alt="Classic Romantic Wedding Set - Crystal candelabra with flower stand and LED candles">
```

### 图片命名规范

**好的命名**：
- ✅ `MG-9A-001-main.jpg`
- ✅ `crystal-candelabra-9-arms-wedding.jpg`
- ✅ `scene-wedding-garden-centerpiece.jpg`

**不好的命名**：
- ❌ `IMG_1234.jpg`
- ❌ `DSC0001.jpg`
- ❌ `photo.jpg`
- ❌ `image.png`

---

## 📸 拍摄指南

### 产品拍摄

1. **准备**
   - 专业摄影棚或白色背景纸
   - 柔光箱或反光板
   - 高质量单反相机
   - 三脚架（保证稳定）

2. **拍摄步骤**
   - 清洁产品（去除指纹和灰尘）
   - 设置白色背景
   - 调整光线（避免强烈阴影）
   - 多角度拍摄（正面、侧面、细节）
   - 使用三脚架（保证清晰度）

3. **后期处理**
   - 裁剪到标准尺寸
   - 调整亮度和对比度
   - 去除背景杂质
   - 保存为JPG/WebP格式
   - 压缩到目标文件大小

### 场景拍摄

1. **选择场地**
   - 婚礼：花园、室内宴会厅、海滩
   - 活动：酒店、会议中心、餐厅
   - 酒店：大堂、宴会厅、套房

2. **布置场景**
   - 搭建完整的餐桌布置
   - 添加餐具、花卉、蜡烛
   - 确保光线充足
   - 营造真实氛围

3. **拍摄技巧**
   - 使用真实场景（不是摆拍）
   - 展示产品实际效果
   - 捕捉光影反射
   - 拍摄不同时间段

---

## 🚀 图片上传和更新流程

### 第1步：准备图片
```bash
# 1. 创建目录结构
mkdir -p cloudflare-deploy/images/products/main
mkdir -p cloudflare-deploy/images/products/side
mkdir -p cloudflare-deploy/images/products/detail
mkdir -p cloudflare-deploy/images/sets
mkdir -p cloudflare-deploy/images/scenes/wedding
mkdir -p cloudflare-deploy/images/scenes/event
mkdir -p cloudflare-deploy/images/scenes/hotel
mkdir -p cloudflare-deploy/images/brand

# 2. 按命名规范重命名图片
# 使用批量重命名工具或脚本
```

### 第2步：优化图片
```bash
# 使用ImageMagick或其他工具批量优化
# 调整尺寸
convert input.jpg -resize 800x600 output.jpg

# 压缩质量
convert input.jpg -quality 85 output.jpg

# 批量处理
for f in *.jpg; do
    convert "$f" -resize 800x600 -quality 85 "optimized/$f"
done
```

### 第3步：更新HTML文件
```html
<!-- 更新产品页面图片路径 -->
<img src="images/products/main/MG-9A-001-main.jpg"
     alt="MG-9A-001 9-Arms Crystal Candelabra">

<!-- 更新套装图片 -->
<img src="images/sets/set-classic-romantic.jpg"
     alt="Classic Romantic Wedding Set">

<!-- 更新场景图片 -->
<img src="images/scenes/wedding/scene-wedding-001.jpg"
     alt="Wedding centerpiece decoration">
```

### 第4步：测试和验证
```bash
# 1. 检查所有图片是否存在
find cloudflare-deploy/images -name "*.jpg" -o -name "*.png"

# 2. 检查图片文件大小
du -h cloudflare-deploy/images/* | sort -h

# 3. 检查图片加载速度
# 在浏览器中打开页面，使用开发者工具检查加载时间
```

---

## ⚠️ 常见错误和解决方案

### 错误1：图片重复
**问题**：多个产品使用同一张图片
**影响**：专业度下降、SEO惩罚、客户困惑

**解决方案**：
- 为每个产品拍摄独特图片
- 使用产品编号作为文件名
- 创建图片清单，避免重复

### 错误2：图片命名不规范
**问题**：使用 `IMG_1234.jpg` 或 `DSC0001.jpg`
**影响**：SEO差、管理困难

**解决方案**：
- 使用描述性文件名
- 遵循命名规范
- 批量重命名工具

### 错误3：图片尺寸不统一
**问题**：图片尺寸各异，布局混乱
**影响**：用户体验差、不专业

**解决方案**：
- 统一图片尺寸标准
- 批量调整工具
- 设计规范文档

### 错误4：文件过大
**问题**：图片文件超过500KB或1MB
**影响**：加载慢、用户体验差、SEO惩罚

**解决方案**：
- 压缩图片质量
- 使用WebP格式
- 懒加载技术

---

## 📊 图片清单模板

### 产品图片清单

| SKU | 主图 | 侧面图 | 细节图 | 状态 |
|-----|------|--------|--------|------|
| MG-9A-001 | MG-9A-001-main.jpg | MG-9A-001-side.jpg | MG-9A-001-detail.jpg | ✅ |
| MG-9A-002 | MG-9A-002-main.jpg | MG-9A-002-side.jpg | MG-9A-002-detail.jpg | ✅ |
| MG-5A-001 | MG-5A-001-main.jpg | MG-5A-001-side.jpg | MG-5A-001-detail.jpg | ⏳ |
| ... | ... | ... | ... | ... |

### 场景图片清单

| 场景ID | 文件名 | 类型 | 用途 | 状态 |
|--------|--------|------|------|------|
| WED-001 | scene-wedding-001.jpg | 婚礼 | 产品详情页 | ✅ |
| WED-002 | scene-wedding-garden.jpg | 婚礼 | Wedding Collection | ✅ |
| EVT-001 | scene-event-001.jpg | 活动 | 案例研究 | ⏳ |
| ... | ... | ... | ... | ... |

---

## 🎯 实施时间表

### 第1周：产品图片
- [ ] 拍摄50+产品主图
- [ ] 拍摄150+产品细节图
- [ ] 优化和压缩图片
- [ ] 上传到指定目录

### 第2周：场景图片
- [ ] 拍摄20-30张婚礼场景
- [ ] 拍摄15-20张活动场景
- [ ] 拍摄15-20张酒店场景
- [ ] 优化和上传

### 第3周：套装和品牌图片
- [ ] 拍摄3-5张套装图片
- [ ] 准备Logo文件
- [ ] 拍摄工厂照片
- [ ] 上传所有图片

### 第4周：更新和测试
- [ ] 更新所有HTML文件
- [ ] 添加alt标签
- [ ] 测试图片加载
- [ ] SEO优化

---

## 📞 需要帮助？

如果需要：
1. **批量重命名脚本** → 我可以帮你生成
2. **图片优化工具** → 推荐ImageMagick、TinyPNG
3. **HTML更新脚本** → 自动替换图片路径
4. **图片检查工具** → 验证图片质量和命名

---

**记住：每个产品必须有独特、高质量、SEO优化的图片！** 📸
