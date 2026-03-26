# 🚀 Cloudflare Pages 部署指南

## 📋 部署前检查

### ✅ 文件清单
确保以下文件都在 `cloudflare-deploy/` 目录中：

```
✓ index.html (32KB) - 首页（全英文）
✓ products.html (28KB) - 产品页（全英文）
✓ contact.html (19KB) - 联系页（全英文）
✓ about.html (25KB) - 关于页（全英文）
✓ download.html (4.7KB) - 下载页（全英文）
✓ style.css (6.2KB) - 样式文件
✓ sitemap.xml (819B) - 网站地图
✓ robots.txt (196B) - 搜索引擎配置
✓ images/ - 图片文件夹（包含所有产品图片）
```

### 🌐 域名配置
- 主域名：`miga.cc`
- 预览域名：`www.miga.cc`
- 目标：全英文网站，无中文内容

---

## 📝 部署步骤

### 步骤 1：访问 Cloudflare Pages

1. 打开浏览器，访问：https://dash.cloudflare.com
2. 登录你的 Cloudflare 账户
3. 点击左侧菜单：**Workers & Pages**
4. 找到你的 Pages 项目：`migac-website`

---

### 步骤 2：创建新部署

#### 方式 A：直接上传（推荐）

1. 点击 **Create deployment**
2. 选择 **Upload assets**
3. 拖拽 `cloudflare-deploy` 文件夹到上传区域
   - **重要**：确保上传整个文件夹，而不是单个文件
4. 点击 **Deploy site**
5. 等待 2-3 分钟部署完成

#### 方式 B：使用 Direct Upload

1. 点击 **Create deployment**
2. 点击 **Direct Upload**
3. 按以下顺序上传文件：
   ```
   1. index.html
   2. products.html
   3. contact.html
   4. about.html
   5. download.html
   6. style.css
   7. sitemap.xml
   8. robots.txt
   9. images/ （整个文件夹）
   ```
4. 点击 **Deploy site**

---

### 步骤 3：配置自定义域名

1. 部署完成后，点击 **Custom domains**
2. 添加以下域名：
   - `miga.cc`
   - `www.miga.cc`
3. 点击 **Activate**
4. 等待 DNS 生效（通常 1-5 分钟）

---

### 步骤 4：验证部署

#### 访问以下 URL，检查是否正常：

```
✓ https://miga.cc （首页）
✓ https://miga.cc/products.html （产品页）
✓ https://miga.cc/contact.html （联系页）
✓ https://miga.cc/about.html （关于页）
✓ https://miga.cc/download.html （下载页）
```

#### 检查清单：

- [ ] 页面全部显示英文
- [ ] 公司名称：Yiwu Bangye Handicraft Factory
- [ ] 地址：Chengbei Road L38, Houzhai Street, Yiwu City
- [ ] 导航菜单：Browse, Catalog, Contact, About, Download
- [ ] 所有按钮：Send, Submit, Reset, View Details
- [ ] 产品描述：全英文
- [ ] 图片正常显示

---

## 🔧 故障排查

### 问题 1：页面显示 404

**原因**：文件上传不完整

**解决方案**：
1. 检查所有文件是否已上传
2. 特别检查 `images/` 文件夹是否上传
3. 重新上传缺失的文件

---

### 问题 2：图片无法显示

**原因**：图片路径错误

**解决方案**：
1. 确保 `images/` 文件夹已上传
2. 检查图片路径是否正确
3. 清除浏览器缓存后重试

---

### 问题 3：DNS 解析慢

**原因**：DNS 传播需要时间

**解决方案**：
1. 等待 5-10 分钟
2. 使用 `nslookup` 检查 DNS 解析：
   ```bash
   nslookup miga.cc
   ```
3. 检查 Cloudflare DNS 设置

---

### 问题 4：页面显示中文

**原因**：缓存问题或上传了旧文件

**解决方案**：
1. 强制刷新浏览器：`Ctrl + Shift + R`（Windows）或 `Cmd + Shift + R`（Mac）
2. 检查是否上传了最新的 HTML 文件
3. 查看文件修改日期，确保是最新的

---

## 📊 部署成功指标

### ✅ 成功标志

- 所有页面正常访问（HTTP 200）
- 全英文内容，无中文
- 图片正常显示
- 导航菜单工作正常
- 表单可以提交

### 🎯 性能目标

- 首页加载时间：< 2 秒
- 所有页面加载时间：< 3 秒
- 图片加载成功率：100%
- 移动端适配正常

---

## 📱 移动端测试

### 测试设备

- [ ] iPhone / iOS Safari
- [ ] Android / Chrome
- [ ] iPad / iPadOS
- [ ] 平板设备

### 检查项

- [ ] 页面响应式布局正常
- [ ] 触摸操作流畅
- [ ] 图片自适应缩放
- [ ] 导航菜单在移动端正常工作

---

## 🔍 SEO 检查

### 必须验证的 SEO 元素

- [ ] 页面标题正确
- [ ] Meta 描述存在
- [ ] sitemap.xml 可访问
- [ ] robots.txt 可访问
- [ ] 图片有 alt 属性
- [ ] 结构化数据正确

### 提交到搜索引擎

1. **Google Search Console**
   ```
   https://search.google.com/search-console
   → 添加属性 miga.cc
   → 验证域名所有权
   → 提交 sitemap.xml
   ```

2. **Bing Webmaster Tools**
   ```
   https://www.bing.com/webmasters
   → 添加网站 miga.cc
   → 验证域名所有权
   → 提交 sitemap.xml
   ```

---

## 📈 监控和分析

### 推荐工具

1. **Google Analytics**（可选）
2. **Cloudflare Analytics**（免费，内置）
3. **Google Search Console**（免费）

### 关键指标

- 页面浏览量（Page Views）
- 访问来源（Traffic Sources）
- 转化率（Conversion Rate）
- 停留时间（Time on Site）

---

## 🎉 部署完成

### 完成后

- [ ] 所有页面正常访问
- [ ] 全英文内容验证通过
- [ ] 移动端测试通过
- [ ] SEO 元素验证通过
- [ ] 监控工具已配置

### 📞 需要帮助？

如果遇到问题，检查以下资源：

1. Cloudflare Pages 文档：https://developers.cloudflare.com/pages
2. DNS 检查工具：https://dnschecker.org
3. 页面速度测试：https://pagespeed.web.dev

---

**祝部署成功！** 🚀
