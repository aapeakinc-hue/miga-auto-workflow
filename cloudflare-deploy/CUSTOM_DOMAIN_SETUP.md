# Cloudflare Pages 自定义域名配置指南

## 🌐 当前状态

✅ **已部署成功**
- Pages 项目名称：migac-website
- 临时域名：migac-website.pages.dev
- 已配置域名：products.miga.cc
- 部署状态：成功（10 分钟前）

❌ **待配置**
- 主域名：miga.cc

---

## 🎯 目标

让用户可以通过以下地址访问网站：
- ✅ https://miga.cc （主域名）
- ✅ https://www.miga.cc （带 www）
- ✅ https://products.miga.cc （已配置）

---

## 📋 配置步骤

### 步骤 1：添加自定义域名

1. 访问 Cloudflare Dashboard：https://dash.cloudflare.com
2. 点击 `Workers & Pages` → `migac-website`
3. 点击 `Custom domains` 标签
4. 点击 `Set up a custom domain` 按钮
5. 输入域名：`miga.cc`
6. 点击 `Continue`

### 步骤 2：配置 DNS 记录

Cloudflare 会自动检测并建议你配置 DNS 记录：

**方式 A：通过 Cloudflare DNS（推荐）**

如果 `miga.cc` 域名已经在 Cloudflare 管理：

1. Cloudflare 会自动添加以下 DNS 记录：
   ```
   Type: CNAME
   Name: miga.cc
   Target: migac-website.pages.dev
   Proxy status: Proxied (橙色云朵)
   ```

2. 等待 DNS 生效（通常 5-15 分钟）

**方式 B：通过其他 DNS 提供商**

如果域名在其他 DNS 提供商管理（如 GoDaddy, Namecheap 等）：

1. 添加 CNAME 记录：
   ```
   Type: CNAME
   Name: @ 或 miga.cc
   Target: migac-website.pages.dev
   TTL: 3600
   ```

2. 如果不支持根域名 CNAME，添加 A 记录指向 Cloudflare IP：
   ```
   Type: A
   Name: @ 或 miga.cc
   Target: 192.0.2.1（示例，需要使用 Cloudflare 提供的 IP）
   ```

### 步骤 3：添加 www 子域名（可选但推荐）

1. 在 `Custom domains` 标签点击 `Set up a custom domain`
2. 输入：`www.miga.cc`
3. 点击 `Continue`

4. 添加 DNS 记录：
   ```
   Type: CNAME
   Name: www
   Target: miga.cc
   Proxy status: Proxied（橙色云朵）
   ```

---

## ⚙️ 自动重定向配置

为了让所有访问都指向主域名，配置自动重定向：

### 重定向 www.miga.cc → miga.cc

1. 在 Cloudflare Dashboard 中，选择 `miga.cc` 域名
2. 点击 `Rules` → `Page Rules`
3. 点击 `Create Page Rule`
4. 输入 URL 模式：`www.miga.cc/*`
5. 设置转发：
   - Setting: Forwarding URL
   - Status Code: 301 - Permanent Redirect
   - Destination URL: `https://miga.cc/$1`
6. 点击 `Save and Deploy`

---

## 🔍 验证配置

### 1. 检查 DNS 生效

等待 DNS 生效后（通常 5-15 分钟），运行：

```bash
# Windows
nslookup miga.cc

# Mac/Linux
dig miga.cc
```

应该看到指向 Cloudflare 或 migac-website.pages.dev 的记录。

### 2. 检查域名解析

访问：https://dnschecker.org
输入 `miga.cc`，查看全球 DNS 解析状态。

### 3. 测试访问

1. 访问：https://miga.cc
2. 访问：https://www.miga.cc
3. 确认两者都能正常访问网站
4. 检查 SSL 证书是否正常（浏览器显示锁图标 🔒）

---

## 🚨 常见问题

### 问题 1：域名无法访问

**原因**：DNS 未生效或配置错误

**解决方案**：
1. 等待 24 小时让 DNS 全球生效
2. 检查 DNS 记录是否正确
3. 确认域名未过期
4. 清除浏览器缓存

### 问题 2：SSL 证书错误

**原因**：SSL 证书尚未颁发

**解决方案**：
1. Cloudflare 会自动颁发 SSL 证书
2. 等待 15-30 分钟
3. 如果超时，在 `Custom domains` 标签点击 `Request certificate`

### 问题 3：页面 404

**原因**：域名配置成功，但页面路径错误

**解决方案**：
1. 确认访问的页面存在
2. 检查文件名大小写（Linux 区分大小写）
3. 确认 `index.html` 在根目录

### 问题 4：重定向循环

**原因**：配置了冲突的重定向规则

**解决方案**：
1. 检查 Page Rules 是否冲突
2. 检查网站代码中是否有重定向
3. 删除冲突的 Page Rules

---

## 📊 验证清单

配置完成后，确认以下项目：

- [ ] DNS 记录已添加并生效
- [ ] https://miga.cc 可以访问
- [ ] https://www.miga.cc 可以访问
- [ ] 浏览器显示 SSL 锁图标 🔒
- [ ] www.miga.cc 自动重定向到 miga.cc
- [ ] 所有页面都能正常访问
- [ ] 移动端显示正常
- [ ] 表单功能正常（配置 Formspree 后）
- [ ] WhatsApp 聊天功能正常

---

## 🎯 完成后

配置完成后，你的网站可以通过以下地址访问：

1. **主域名**：https://miga.cc（推荐）
2. **Pages 域名**：https://migac-website.pages.dev（备用）
3. **产品域名**：https://products.miga.cc（已配置）

---

## 📞 需要帮助？

如果遇到问题，可以：

1. 查看 Cloudflare 文档：https://developers.cloudflare.com/pages/
2. 使用 Cloudflare 诊断工具：https://1.1.1.1/help/
3. 联系技术支持：info@miga.cc

---

**预计完成时间**：10-30 分钟
**DNS 生效时间**：5-15 分钟
**SSL 颁发时间**：15-30 分钟

---

**状态**：✅ 部署成功，待配置主域名
**下一步**：添加 miga.cc 自定义域名
