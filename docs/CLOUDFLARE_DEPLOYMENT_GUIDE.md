# Cloudflare Pages 部署指南 - MIGAC

本文档提供详细的 Cloudflare Pages 部署步骤。

---

## 🚀 方案选择

根据您的情况，选择最适合的方案：

| 方案 | 时间 | 难度 | 适合场景 |
|------|------|------|---------|
| 方案A: 直接上传 | 5分钟 | ⭐ | 快速部署，无需Git |
| 方案B: Git仓库连接 | 10分钟 | ⭐⭐ | 长期维护，自动部署 |
| 方案C: Wrangler CLI | 10分钟 | ⭐⭐ | 开发者，命令行操作 |

**推荐**: 方案A（最快，5分钟完成）

---

## 方案A: 直接上传文件（推荐，5分钟）

### 步骤1: 登录 Cloudflare

1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 登录您的账号
3. 在左侧菜单找到 `Workers & Pages` 并点击

---

### 步骤2: 创建新项目或使用现有项目

#### 如果您已经有 Pages 项目：

1. 在 `Workers & Pages` 页面，找到 `miga.cc` 对应的项目
2. 点击项目名称进入项目详情
3. 跳转到"步骤4"

#### 如果您还没有 Pages 项目：

1. 在 `Workers & Pages` 页面，点击 `Create application` 按钮
2. 选择 `Pages` 标签（默认已选中）
3. 点击 `Upload assets` 按钮

---

### 步骤3: 上传文件

#### 3.1 准备文件

**在本地电脑执行以下操作**：

```bash
# 进入项目目录
cd /path/to/your/project

# 1. 创建部署目录
mkdir -p cloudflare-deploy

# 2. 复制优化后的页面
cp assets/contact-optimized.html cloudflare-deploy/index.html
cp assets/products.html cloudflare-deploy/products.html

# 3. （可选）复制现有网站的其他文件
# cp *.html cloudflare-deploy/
# cp -r images cloudflare-deploy/  # 如果有图片目录

# 4. 压缩文件（方便上传）
cd cloudflare-deploy
zip -r ../cloudflare-deploy.zip *
```

#### 3.2 上传到 Cloudflare

**在 Cloudflare Dashboard 中**：

1. 点击 `Upload assets` 按钮
2. 拖拽 `cloudflare-deploy.zip` 文件到上传区域
   - 或点击 `Select a folder` 选择 `cloudflare-deploy` 文件夹
3. 等待上传完成

---

### 步骤4: 配置项目设置

#### 4.1 命名项目

- **Project name**: `miga-website`（或您喜欢的名称）
- **Production branch**: `main`（如果使用Git，否则忽略）

点击 `Deploy site` 按钮

---

### 步骤5: 配置自定义域名

#### 5.1 等待部署完成

部署通常需要30秒-2分钟，您会看到：
- ✅ 部署成功的提示
- 一个临时的访问URL（如 `miga-website.pages.dev`）

#### 5.2 添加自定义域名

1. 在项目页面，点击 `Custom domains` 标签
2. 点击 `Set up a custom domain`
3. 输入您的域名：`miga.cc`
4. 点击 `Continue`

#### 5.3 配置DNS记录

Cloudflare 会自动添加或更新DNS记录：

- **类型**: CNAME
- **名称**: `@`（根域名）
- **目标**: `miga-website.pages.dev`（或其他项目名）

确认DNS记录后，点击 `Activate domain`

---

### 步骤6: 验证部署

#### 6.1 检查页面是否可访问

在浏览器中访问：
- `https://miga.cc` - 应该看到优化后的联系页面
- `https://miga.cc/products.html` - 应该看到产品展示页面

#### 6.2 功能测试

- [ ] 页面正常加载
- [ ] 产品展示区域显示（6个产品卡片）
- [ ] 信任背书显示（10+年经验、182+客户）
- [ ] 联系表单可以正常填写
- [ ] WhatsApp按钮显示在右下角
- [ ] 点击"浏览产品目录"可以滚动到产品区域
- [ ] 点击"获取免费报价"可以滚动到联系表单

---

## 方案B: 连接到 Git 仓库（长期维护）

### 优势
- ✅ 自动部署（推送代码自动更新）
- ✅ 版本管理
- ✅ 回滚方便
- ✅ 团队协作

### 步骤

#### 1. 准备 Git 仓库

```bash
# 进入项目目录
cd /path/to/your/project

# 1. 将优化后的页面复制到项目根目录
cp assets/contact-optimized.html index.html
cp assets/products.html products.html

# 2. 提交到Git
git add index.html products.html
git commit -m "优化网站 - 添加产品展示和信任元素"
git push
```

---

#### 2. 在 Cloudflare 中创建项目

1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 `Workers & Pages`
3. 点击 `Create application`
4. 选择 `Connect to Git`
5. 选择您的 Git 提供商（GitHub/GitLab/Bitbucket）
6. 授权 Cloudflare 访问您的仓库
7. 选择 `miga-crm` 项目

---

#### 3. 配置构建设置

在配置页面：

- **Project name**: `miga-website`
- **Production branch**: `main`
- **Framework preset**: `None`（静态HTML）
- **Build command**: 留空（无需构建）
- **Build output directory**: `/`（根目录）

点击 `Save and Deploy`

---

#### 4. 配置自定义域名

同"方案A"的"步骤5"

---

#### 5. 自动部署

以后每次您推送代码到Git仓库，Cloudflare会自动部署：

```bash
# 修改页面
nano index.html

# 提交并推送
git add index.html
git commit -m "更新首页"
git push

# Cloudflare 会自动部署，无需手动操作
```

---

## 方案C: 使用 Wrangler CLI（命令行）

### 安装 Wrangler

```bash
# 安装 Wrangler CLI
npm install -g wrangler

# 登录
wrangler login
```

---

### 创建并部署项目

```bash
# 进入项目目录
cd /path/to/your/project

# 1. 创建 Pages 项目
wrangler pages project create miga-website

# 2. 准备部署文件
mkdir -p deploy
cp assets/contact-optimized.html deploy/index.html
cp assets/products.html deploy/products.html

# 3. 部署
wrangler pages deploy deploy --project-name=miga-website
```

---

### 配置自定义域名

```bash
# 添加自定义域名
wrangler pages domain create miga.cc --project-name=miga-website
```

---

## 🧪 部署后测试

### 1. 基础访问测试

```bash
# 测试主页
curl -I https://miga.cc

# 测试产品页面
curl -I https://miga.cc/products.html

# 应该看到 HTTP/2 200 响应
```

---

### 2. 性能测试

访问 [Cloudflare Web Analytics](https://dash.cloudflare.com/ -> Analytics -> Web Analytics)

查看：
- 页面加载时间
- 流量统计
- 访问地域分布

---

### 3. SEO 检查

在浏览器中按 `F12` 打开开发者工具，检查：

```javascript
// 检查 Meta 标签
document.querySelector('meta[name="description"]').content

// 检查 Open Graph 标签
document.querySelector('meta[property="og:title"]').content

// 检查规范链接
document.querySelector('link[rel="canonical"]').href
```

---

## 📸 上传真实产品图片

### 步骤

#### 1. 准备图片

- 尺寸: 800x600px 或 400x300px
- 格式: JPEG/PNG/WebP
- 文件大小: 100-300KB
- 命名: `crystal-candle-holder-001.jpg` 等

#### 2. 创建图片目录

```bash
cd cloudflare-deploy
mkdir images
```

#### 3. 上传图片

将产品图片复制到 `cloudflare-deploy/images/` 目录

#### 4. 更新HTML中的图片路径

**修改 contact-optimized.html**：

```html
<!-- 查找所有占位图片 -->
<img src="https://via.placeholder.com/400x300?text=Crystal+Candle+Holder">

<!-- 替换为真实图片路径 -->
<img src="/images/crystal-candle-holder-001.jpg" alt="经典水晶烛台">
```

**修改 products.html**：

```html
<!-- 替换占位图片 -->
<img src="/images/crystal-candle-holder-001.jpg" alt="经典水晶烛台 - 型号CH-001">
```

#### 5. 重新部署

```bash
cd cloudflare-deploy
zip -r ../cloudflare-deploy.zip *
```

然后在 Cloudflare Dashboard 中重新上传，或使用 Git 推送。

---

## 🔧 常见问题

### 问题1: 上传后看到404错误

**原因**: 文件路径错误

**解决方案**:
```bash
# 检查文件结构
cd cloudflare-deploy
ls -la

# 确保有 index.html 文件
```

---

### 问题2: 图片不显示

**原因**: 图片路径错误或文件未上传

**解决方案**:
```bash
# 1. 确保图片在 images/ 目录
ls -la cloudflare-deploy/images/

# 2. 检查HTML中的路径
# 使用 /images/xxx.jpg 而不是 images/xxx.jpg
```

---

### 问题3: 自定义域名无法访问

**原因**: DNS配置错误或传播未完成

**解决方案**:
1. 检查DNS记录：`dig miga.cc`
2. 确认CNAME记录指向正确的Pages域名
3. 等待DNS传播（通常需要几分钟）
4. 在浏览器中使用隐身模式测试

---

### 问题4: 部署后看到旧版本

**原因**: 浏览器缓存

**解决方案**:
```bash
# 1. 清除浏览器缓存
# Windows/Linux: Ctrl + F5
# Mac: Cmd + Shift + R

# 2. 使用隐身模式测试

# 3. 添加版本号（高级）
# <link href="style.css?v=2.0" rel="stylesheet">
```

---

## 📊 部署检查清单

部署完成后，请确认：

### 文件检查
- [ ] index.html 已部署（优化后的联系页面）
- [ ] products.html 已部署
- [ ] 图片目录 images/ 已创建（如果上传了图片）
- [ ] 所有文件权限正确

### 功能测试
- [ ] https://miga.cc 可以访问
- [ ] https://miga.cc/products.html 可以访问
- [ ] 页面样式正常
- [ ] 产品卡片显示正确
- [ ] 联系表单可以正常填写
- [ ] WhatsApp链接正常工作

### SEO检查
- [ ] 页面标题正确
- [ ] Meta描述正确
- [ ] Open Graph标签存在
- [ ] 规范链接正确

### 性能检查
- [ ] 页面加载时间 < 3秒
- [ ] HTTPS已启用
- [ ] 移动端显示正常

---

## 🚀 下一步优化

### 短期（本周）
1. 上传真实产品图片
2. 测试所有功能
3. 提交到 Google Search Console

### 中期（本月）
4. 添加公司Logo
5. 收集客户评价
6. 创建FAQ页面

### 长期（持续）
7. 定期更新产品
8. 发布博客文章
9. 优化SEO关键词

---

## 📞 需要帮助？

如遇到问题：

1. 查看本文档的"常见问题"部分
2. 访问 [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
3. 联系 Cloudflare 支持

---

**文档版本**: 1.0
**更新日期**: 2024-01-01

---

## ✅ 快速开始（5分钟完成）

**最简单的部署步骤**：

1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 `Workers & Pages` → `Create application`
3. 点击 `Upload assets`
4. 上传 `cloudflare-deploy.zip`（包含 index.html 和 products.html）
5. 配置自定义域名 `miga.cc`
6. 完成！

**祝您部署顺利！🚀**
