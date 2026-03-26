# 🚀 快速开始 - 5分钟完成部署

## 方案选择

### ⚡ 方案A: 立即部署（使用占位图片，10分钟）

**步骤1: 创建占位图片**
```bash
./scripts/prepare-images.sh
```
输入 `y` 创建占位图片

**步骤2: 更新图片路径**
```bash
./scripts/update-image-paths.sh
```

**步骤3: 上传到 Cloudflare Pages**
1. 访问 https://dash.cloudflare.com/
2. Workers & Pages → 您的项目
3. Upload assets → 上传 `cloudflare-deploy` 文件夹
4. 等待部署完成

**完成！** 访问 https://miga.cc 查看效果

---

### 📸 方案B: 准备真实图片（1-3天）

**步骤1: 准备14张产品图片**
- 参考: `docs/PRODUCT_IMAGE_GUIDE.md`
- 搜索链接: `DEPLOYMENT_README.md`
- 尺寸: 800x600px 或 400x300px
- 格式: JPEG/PNG

**步骤2: 复制图片**
```bash
mkdir -p cloudflare-deploy/images
cp /你的图片路径/*.jpg cloudflare-deploy/images/
```

**步骤3: 验证并更新**
```bash
./scripts/prepare-images.sh
./scripts/update-image-paths.sh
```

**步骤4: 上传到 Cloudflare Pages**
同方案A步骤3

**完成！** 访问 https://miga.cc 查看效果

---

### 🔄 方案C: 混合部署（30分钟）

**步骤1: 准备部分真实图片（4-6张）**
- 至少准备核心产品图片
- 其他使用占位图片

**步骤2: 复制图片**
```bash
mkdir -p cloudflare-deploy/images
cp /你的图片路径/*.jpg cloudflare-deploy/images/
```

**步骤3: 创建缺失的占位图片**
```bash
./scripts/prepare-images.sh
# 输入 y
```

**步骤4: 更新图片路径**
```bash
./scripts/update-image-paths.sh
```

**步骤5: 上传到 Cloudflare Pages**
同方案A步骤3

**完成！** 访问 https://miga.cc 查看效果

---

## 📋 图片清单（14张）

### 联系页面（6张）
1. crystal-candle-holder.jpg
2. luxury-candelabra.jpg
3. crystal-tealight.jpg
4. crystal-decor.jpg
5. crystal-wall-sconce.jpg
6. crystal-chandelier.jpg

### 产品页面（8张）
7. crystal-candle-holder-001.jpg
8. luxury-candelabra-002.jpg
9. crystal-tealight-003.jpg
10. crystal-decor-004.jpg
11. crystal-chandelier-005.jpg
12. modern-candle-holder-006.jpg
13. royal-candelabra-007.jpg
14. colorful-tealight-008.jpg

---

## 🔗 快速搜索链接

### 阿里巴巴
- https://www.alibaba.com/showroom/crystal-candle-holder.html

### Google Images
- https://www.google.com/search?tbm=isch&q=crystal+candle+holder+K9

### Made-in-China
- https://www.made-in-china.com/manufacturers-list/C_27647401.html

---

## ✅ 验证部署

部署完成后，访问以下链接验证：

- ✅ https://miga.cc - 主页
- ✅ https://miga.cc/products.html - 产品页

检查项：
- [ ] 页面正常加载
- [ ] 图片正常显示
- [ ] 链接正常工作
- [ ] 移动端显示正常

---

## 📞 需要帮助？

- 📖 `DEPLOYMENT_README.md` - 完整指南
- 📖 `docs/PRODUCT_IMAGE_GUIDE.md` - 图片指南
- 📧 info@miga.cc
- 📞 +86-19879476613

---

**立即开始部署吧！🚀**
