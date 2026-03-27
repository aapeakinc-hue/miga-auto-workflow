# 📸 图片准备快速参考卡片

## ⚠️ 核心原则（必须遵守）

**绝对禁止**：在catalog或产品页面中使用重复图片！

**必须做到**：
- ✅ 每个SKU有唯一的产品图片
- ✅ 每个套装有独特的组合图片
- ✅ 图片命名规范清晰
- ✅ 图片SEO优化（alt标签）

---

## 📋 图片需求快速清单

| 类型 | 数量 | 命名规范 | 规格 |
|------|------|----------|------|
| **产品主图** | 50+ | `MG-XXX-001-main.jpg` | 800x600px, JPG, 白底 |
| **产品侧面图** | 150+ | `MG-XXX-001-side.jpg` | 800x600px, JPG, 白底 |
| **产品细节图** | 150+ | `MG-XXX-001-detail.jpg` | 800x600px, JPG, 白底 |
| **婚礼场景** | 20-30 | `scene-wedding-001.jpg` | 1200x800px, JPG |
| **活动场景** | 15-20 | `scene-event-001.jpg` | 1200x800px, JPG |
| **酒店场景** | 15-20 | `scene-hotel-001.jpg` | 1200x800px, JPG |
| **套装图片** | 3-5 | `set-classic-romantic.jpg` | 1000x800px, JPG |

---

## 📁 目录结构（推荐）

```
cloudflare-deploy/
└── images/
    ├── products/
    │   ├── main/          # 主图
    │   ├── side/          # 侧面图
    │   └── detail/        # 细节图
    ├── sets/             # 套装图片
    ├── scenes/
    │   ├── wedding/       # 婚礼场景
    │   ├── event/         # 活动场景
    │   └── hotel/         # 酒店场景
    └── brand/            # 品牌图片
```

---

## 🎨 命名规范速查

### ✅ 好的命名
```
MG-9A-001-main.jpg              # 产品主图
MG-9A-001-side.jpg              # 产品侧面图
MG-9A-001-detail.jpg            # 产品细节图
scene-wedding-001.jpg           # 婚礼场景
set-classic-romantic.jpg        # 套装图片
logo-horizontal.png              # Logo
```

### ❌ 不好的命名
```
IMG_1234.jpg                    # ❌ 无意义
DSC0001.jpg                     # ❌ 相机默认
photo.jpg                       # ❌ 太通用
image.png                       # ❌ 太通用
IMG.JPG                         # ❌ 大写扩展名
```

---

## 🔧 快速工具

### 1. 组织图片
```bash
bash organize-images.sh
```
- 自动创建目录结构
- 自动分类图片
- 生成图片清单
- 检查重复文件

### 2. 更新HTML路径
```bash
bash update-image-paths.sh
```
- 自动更新HTML文件中的图片路径
- 创建备份文件

### 3. 检查图片
```bash
bash check-images.sh
```
- 检查重复文件名
- 检查重复内容
- 检查文件大小
- 检查命名规范
- 生成检查报告

---

## 📊 质量检查清单

### 图片质量
- [ ] 白色背景（产品图）
- [ ] 清晰无模糊
- [ ] 光线均匀
- [ ] 无阴影和反光
- [ ] 文件大小 <500KB（产品图）
- [ ] 文件大小 <1MB（场景图）

### 命名规范
- [ ] 使用小写字母
- [ ] 使用连字符分隔
- [ ] 包含SKU编号
- [ ] 包含类型标识
- [ ] 使用正确的扩展名

### SEO优化
- [ ] 每个图片有alt标签
- [ ] alt标签描述准确
- [ ] 文件名包含关键词
- [ ] 图片尺寸合理

---

## ⚠️ 常见错误和解决方案

| 错误 | 影响 | 解决方案 |
|------|------|----------|
| 重复图片 | 专业度↓ SEO↓ | 每个SKU拍摄独特图片 |
| 命名不规范 | SEO差 管理难 | 使用描述性文件名 |
| 文件过大 | 加载慢 | 压缩到目标大小 |
| 背景不纯 | 不专业 | 使用纯白背景 |
| 光线不均 | 效果差 | 使用专业灯光 |

---

## 🚀 实施步骤

### 第1步：准备图片
1. 拍摄所有产品图片
2. 拍摄场景图片
3. 准备套装图片
4. 准备品牌图片

### 第2步：组织图片
1. 创建目录结构
2. 按命名规范重命名
3. 分类到对应目录
4. 运行 `organize-images.sh`

### 第3步：检查图片
1. 运行 `check-images.sh`
2. 查看检查报告
3. 修复发现的问题
4. 重新检查

### 第4步：更新HTML
1. 运行 `update-image-paths.sh`
2. 添加alt标签
3. 测试图片加载
4. 验证SEO优化

---

## 📞 需要帮助？

### 文档
- 详细指南: `IMAGE_PREPARATION_GUIDE.md`
- 检查报告: `images/CHECK_REPORT.md`
- 图片清单: `images/IMAGE_INVENTORY.md`

### 工具
- 组织工具: `organize-images.sh`
- 更新工具: `update-image-paths.sh`
- 检查工具: `check-images.sh`

---

**记住：每个产品必须有独特、高质量、SEO优化的图片！** 📸✅
