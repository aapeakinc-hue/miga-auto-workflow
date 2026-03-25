# MIGAC 网站部署文件

## 📁 文件说明

- **index.html** - 优化后的联系页面（32KB）
  - 包含产品展示、信任背书、SEO优化
  - Hero区域、产品卡片、公司介绍、联系表单
  - 完全响应式设计

- **products.html** - 产品展示页面（28KB）
  - 8个详细产品卡片
  - 分类筛选功能
  - 产品特性和起订量信息

---

## 🚀 部署步骤（Cloudflare Pages）

### 方法1: 直接上传（推荐，5分钟）

1. **登录 Cloudflare**
   - 访问 https://dash.cloudflare.com/
   - 进入 Workers & Pages
   - 点击 Create application → Upload assets

2. **上传文件**
   - 拖拽本文件夹到上传区域
   - 或选择文件夹上传

3. **配置项目**
   - Project name: miga-website
   - 点击 Deploy site

4. **配置域名**
   - 添加自定义域名: miga.cc
   - 等待DNS生效（几分钟）

5. **完成！**
   - 访问 https://miga.cc 查看效果

---

### 方法2: 使用 Git 部署（长期维护）

1. **将文件添加到项目根目录**
   ```bash
   cp cloudflare-deploy/index.html .
   cp cloudflare-deploy/products.html .
   ```

2. **提交到 Git**
   ```bash
   git add index.html products.html
   git commit -m "优化网站 - 添加产品展示"
   git push
   ```

3. **在 Cloudflare 中连接 Git**
   - Workers & Pages → Create application
   - Connect to Git → 选择仓库
   - Deploy

---

## 🖼️ 上传产品图片

### 步骤

1. **创建图片目录**
   ```bash
   mkdir cloudflare-deploy/images
   ```

2. **上传图片**
   - 将产品图片放到 `images/` 目录
   - 推荐尺寸: 800x600px
   - 格式: JPEG/PNG/WebP

3. **更新 HTML 中的图片路径**
   ```html
   <!-- 替换前 -->
   <img src="https://via.placeholder.com/400x300?text=Crystal+Candle+Holder">

   <!-- 替换后 -->
   <img src="/images/crystal-candle-holder-001.jpg" alt="经典水晶烛台">
   ```

4. **重新部署**

---

## 🧪 部署后测试

访问以下链接测试：

- ✅ 主页: https://miga.cc
- ✅ 产品页: https://miga.cc/products.html

### 检查项

- [ ] 页面正常加载
- [ ] 产品展示区域显示（6个产品卡片）
- [ ] 信任背书显示（10+年经验、182+客户）
- [ ] 联系表单可以正常填写
- [ ] WhatsApp按钮显示在右下角
- [ ] 点击链接正常跳转
- [ ] 移动端显示正常

---

## 📚 更多信息

详细部署指南请查看：`docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md`

---

## 📞 需要帮助？

- 📧 info@miga.cc
- 📞 +86-19879476613
- 💬 WhatsApp: +86-19879476613

---

**祝您部署顺利！🚀**
