# 网站部署指南 - MIGAC

本文档提供多种网站部署方案，根据您的托管情况选择适合的方式。

---

## 🎯 快速部署选择指南

根据您的网站托管情况，选择对应的部署方案：

| 托管方式 | 方案 | 时间 | 难度 |
|---------|------|------|------|
| GitHub Pages | 方案1 | 5分钟 | ⭐ |
| Cloudflare Pages | 方案2 | 5分钟 | ⭐ |
| Vercel/Netlify | 方案3 | 5分钟 | ⭐ |
| 自己的服务器 | 方案4 | 10分钟 | ⭐⭐ |
| 虚拟主机/cPanel | 方案5 | 10分钟 | ⭐⭐ |
| 不确定 | 联系我帮你确认 | - | - |

---

## 📋 前置检查

在部署前，请确认以下信息：

- [ ] 您的网站域名: miga.cc
- [ ] 网站托管在哪里？（GitHub Pages/Cloudflare/服务器/其他）
- [ ] 您是否有服务器的SSH访问权限？（如果是服务器部署）
- [ ] 您是否有Git账号？（如果是GitHub Pages部署）

---

## 方案1: GitHub Pages 部署（最简单）

### 适用场景
- ✅ 网站托管在 GitHub Pages
- ✅ 有GitHub账号
- ✅ 项目已推送到GitHub

### 步骤

#### 1. 检查仓库设置

访问：`https://github.com/你的用户名/你的仓库名/settings/pages`

确认：
- Source 选择 `Deploy from a branch`
- Branch 选择 `main` 或 `master`
- `/ (root)` 目录

#### 2. 添加优化后的页面

**在本地执行**：

```bash
# 进入项目目录
cd /path/to/your/project

# 1. 将优化后的页面复制到项目根目录
cp assets/contact-optimized.html contact.html
cp assets/products.html products.html

# 2. 如果想将contact-optimized.html作为首页
cp assets/contact-optimized.html index.html

# 3. 提交到Git
git add contact.html products.html index.html
git commit -m "优化网站 - 添加产品展示和信任元素"
git push
```

#### 3. 等待部署

- GitHub Pages 会在1-3分钟内自动部署
- 访问 `https://你的用户名.github.io/你的仓库名/`
- 或直接访问 `https://miga.cc`（如果已配置域名）

#### 4. 配置域名（如果未配置）

在仓库的 `Settings > Pages > Custom domain` 添加：
- Domain: `miga.cc`
- DNS记录类型: CNAME
- DNS记录值: `你的用户名.github.io`

---

## 方案2: Cloudflare Pages 部署

### 适用场景
- ✅ 网站托管在 Cloudflare Pages
- ✅ 域名在 Cloudflare 管理

### 步骤

#### 1. 登录 Cloudflare

访问：`https://dash.cloudflare.com/`

#### 2. 创建 Pages 项目

1. 点击左侧菜单 `Workers & Pages`
2. 点击 `Create application`
3. 选择 `Pages` 标签
4. 点击 `Upload assets`

#### 3. 上传文件

1. 将 `assets/contact-optimized.html` 重命名为 `index.html`
2. 将 `assets/products.html` 上传
3. 点击 `Deploy site`

#### 4. 配置域名

1. 在项目设置中，点击 `Custom domains`
2. 添加 `miga.cc`
3. 按提示配置DNS记录

---

## 方案3: Vercel/Netlify 部署

### 适用场景
- ✅ 使用 Vercel 或 Netlify
- ✅ 有Git仓库

### Vercel 步骤

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 部署
vercel --prod

# 4. 将优化后的页面复制到根目录
cp assets/contact-optimized.html index.html
cp assets/products.html products.html

# 5. 重新部署
vercel --prod
```

### Netlify 步骤

```bash
# 1. 安装 Netlify CLI
npm install -g netlify-cli

# 2. 登录
netlify login

# 3. 部署
netlify deploy --prod --dir=.

# 4. 将优化后的页面复制到根目录
cp assets/contact-optimized.html index.html
cp assets/products.html products.html

# 5. 重新部署
netlify deploy --prod --dir=.
```

---

## 方案4: 自己的服务器部署（Ubuntu/CentOS）

### 适用场景
- ✅ 有自己的云服务器
- ✅ 域名指向服务器
- ✅ 安装了Nginx/Apache

### 步骤

#### 1. 连接到服务器

```bash
ssh root@你的服务器IP
```

#### 2. 备份现有文件

```bash
cd /var/www/html
cp contact-form.html contact-form-backup.html
```

#### 3. 上传新文件

**在本地电脑执行**：

```bash
# 使用SCP上传
scp assets/contact-optimized.html root@你的服务器IP:/var/www/html/
scp assets/products.html root@你的服务器IP:/var/www/html/
```

**或使用rsync**：

```bash
rsync -avz assets/contact-optimized.html root@你的服务器IP:/var/www/html/
rsync -avz assets/products.html root@你的服务器IP:/var/www/html/
```

#### 4. 设置文件权限

**在服务器上执行**：

```bash
cd /var/www/html
chmod 644 contact-optimized.html products.html
chown www-data:www-data contact-optimized.html products.html
```

#### 5. 配置Nginx（如果需要）

```bash
# 编辑Nginx配置
nano /etc/nginx/sites-available/miga.cc
```

**配置示例**：

```nginx
server {
    listen 80;
    server_name miga.cc www.miga.cc;

    root /var/www/html;
    index contact-optimized.html index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # 启用gzip压缩
    gzip on;
    gzip_types text/html text/css application/javascript;
}
```

**重启Nginx**：

```bash
nginx -t
systemctl restart nginx
```

#### 6. 配置SSL证书（推荐）

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx

# 获取SSL证书
certbot --nginx -d miga.cc -d www.miga.cc

# 自动续期
certbot renew --dry-run
```

---

## 方案5: cPanel/虚拟主机部署

### 适用场景
- ✅ 使用传统虚拟主机
- ✅ 有cPanel管理面板

### 步骤

#### 1. 登录cPanel

访问：`https://你的域名.com/cpanel`

#### 2. 使用文件管理器

1. 点击 `File Manager`
2. 进入 `public_html` 目录
3. 上传文件：
   - `assets/contact-optimized.html` → 重命名为 `index.html`
   - `assets/products.html`

#### 3. 设置权限

右键点击文件 → `Change Permissions` → 设置为 `644`

#### 4. 测试访问

访问 `https://miga.cc` 和 `https://miga.cc/products.html`

---

## 🧪 部署后测试

### 基础测试

```bash
# 1. 测试页面是否可访问
curl -I https://miga.cc
curl -I https://miga.cc/products.html

# 2. 检查HTTP状态码（应该是200）
```

### 功能测试

在浏览器中访问 `https://miga.cc`，检查：

- [ ] 页面正常加载
- [ ] 所有链接正常工作
- [ ] 表单可以正常提交
- [ ] WhatsApp链接正常
- [ ] 产品页面可以访问
- [ ] 移动端显示正常

---

## 🔍 常见问题

### 问题1: 部署后看到404错误

**原因**: 文件路径或配置错误

**解决方案**:
```bash
# 检查文件是否存在
ls -la /var/www/html/

# 检查Nginx配置
cat /etc/nginx/sites-available/miga.cc

# 重启Nginx
systemctl restart nginx
```

### 问题2: 页面样式混乱

**原因**: CSS未正确加载或浏览器缓存

**解决方案**:
```bash
# 1. 清除浏览器缓存（Ctrl+F5 或 Cmd+Shift+R）

# 2. 检查文件权限
ls -la /var/www/html/contact-optimized.html

# 3. 检查HTML语法（CSS内联在HTML中）
```

### 问题3: 域名无法访问

**原因**: DNS未配置或传播未完成

**解决方案**:
```bash
# 1. 检查DNS记录
dig miga.cc
nslookup miga.cc

# 2. 等待DNS传播（通常需要1-24小时）

# 3. 测试IP访问
curl http://你的服务器IP
```

### 问题4: 图片不显示

**原因**: 图片URL错误或文件不存在

**解决方案**:
```bash
# 1. 检查图片URL是否正确
grep "img src" /var/www/html/contact-optimized.html

# 2. 确保图片文件存在
ls -la /var/www/html/images/

# 3. 设置正确的文件权限
chmod 644 /var/www/html/images/*
```

---

## 📊 部署检查清单

部署完成后，请确认以下项目：

### 文件部署
- [ ] `contact-optimized.html` 已部署
- [ ] `products.html` 已部署
- [ ] 文件权限正确（644）
- [ ] 文件所有者正确（www-data）

### 功能测试
- [ ] 主页可以访问（https://miga.cc）
- [ ] 产品页面可以访问
- [ ] 所有链接正常工作
- [ ] 表单可以正常提交
- [ ] WhatsApp链接正常

### 性能测试
- [ ] 页面加载速度 < 3秒
- [ ] 移动端加载正常
- [ ] SEO标签正确
- [ ] Open Graph标签正确

### 安全检查
- [ ] HTTPS已启用
- [ ] SSL证书有效
- [ ] 没有敏感信息泄露
- [ ] 文件权限正确

---

## 🚀 部署脚本（自动化）

### 方案4的自动化部署脚本

创建 `deploy_website.sh`：

```bash
#!/bin/bash

# 配置变量
SERVER_IP="你的服务器IP"
SERVER_USER="root"
WEB_DIR="/var/www/html"

# 备份现有文件
echo "📦 备份现有文件..."
ssh $SERVER_USER@$SERVER_IP "cd $WEB_DIR && cp contact-form.html contact-form-backup.html"

# 上传新文件
echo "📤 上传优化后的页面..."
scp assets/contact-optimized.html $SERVER_USER@$SERVER_IP:$WEB_DIR/
scp assets/products.html $SERVER_USER@$SERVER_IP:$WEB_DIR/

# 设置权限
echo "🔐 设置文件权限..."
ssh $SERVER_USER@$SERVER_IP "cd $WEB_DIR && chmod 644 contact-optimized.html products.html && chown www-data:www-data contact-optimized.html products.html"

# 重启Nginx
echo "🔄 重启Nginx..."
ssh $SERVER_USER@$SERVER_IP "systemctl restart nginx"

echo "✅ 部署完成！"
echo "🌐 访问 https://miga.cc 查看效果"
```

**使用方法**：

```bash
# 1. 创建脚本
nano deploy_website.sh

# 2. 给执行权限
chmod +x deploy_website.sh

# 3. 执行部署
./deploy_website.sh
```

---

## 📞 需要帮助？

如果不确定使用哪种方案，或遇到部署问题，请联系：

- **邮箱**: info@miga.cc
- **WhatsApp**: +86-19879476613
- **电话**: +86-19879476613

---

**文档版本**: 1.0
**更新日期**: 2024-01-01

---

## ✅ 快速开始

**最简单的部署方式**（5分钟）：

1. 如果使用 **GitHub Pages** → 方案1
2. 如果使用 **Cloudflare** → 方案2
3. 如果使用 **Vercel/Netlify** → 方案3
4. 如果有 **自己的服务器** → 方案4
5. 如果使用 **cPanel** → 方案5

**不确定？** 请告诉我您的网站托管方式，我会提供具体的部署步骤！
