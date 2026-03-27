# Formspree 配置检查清单

## 📋 准备工作

- [ ] 已登录 Formspree (https://formspree.io/)
- [ ] 准备好接收表单提交的邮箱（info@miga.cc）

---

## 🚀 配置步骤

### 步骤 1：创建 Formspree 表单

在 Formspree Dashboard 中：

1. 点击 **"New Form"** 或 **"Create Form"**
2. 填写表单信息：
   - **Form Name**: `MIGAC Contact Form`
   - **Email**: `info@miga.cc`
3. 点击 **"Create Form"**

### 步骤 2：获取 Form ID

创建成功后，复制 **Form ID**

示例：
```
Form ID: mzbwqqzj
Endpoint: https://formspree.io/f/mzbwqqzj
```

**记下这个 Form ID**（例如：`mzbwqqzj`）

---

### 步骤 3：更新 HTML 文件

你有两种方式：

#### 方式 A：使用脚本（快速）

```bash
# 编辑配置脚本
nano cloudflare-deploy/setup-formspree.sh

# 修改这一行：
FORM_ID="YOUR_FORM_ID"

# 替换为你的实际 Form ID：
FORM_ID="mzbwqqzj"

# 保存并运行
bash cloudflare-deploy/setup-formspree.sh
```

#### 方式 B：手动编辑

需要更新 3 个文件：

##### free-audit.html
1. 打开 `cloudflare-deploy/free-audit.html`
2. 找到第 600 行：
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```
3. 替换为：
```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
```

##### catalog.html
重复上述步骤，更新第 4 行左右的 `<form>` 标签。

##### request-sample.html
重复上述步骤，更新第 4 行左右的 `<form>` 标签。

---

### 步骤 4：验证配置

```bash
# 检查配置是否正确
grep 'formspree.io' cloudflare-deploy/free-audit.html | head -1
```

应该看到：
```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
```

---

### 步骤 5：测试表单

#### 本地测试

1. 在浏览器中打开 `cloudflare-deploy/free-audit.html`
2. 填写表单：
   - Email: test@example.com
   - Industry: 选择任意行业
3. 点击提交
4. 检查邮箱 `info@miga.cc` 是否收到邮件

#### 在线测试（部署后）

1. 部署到 Cloudflare Pages
2. 访问 https://miga.cc/free-audit.html
3. 填写并提交
4. 检查邮箱

---

## ✅ 验证清单

配置完成后，确认以下项目：

- [ ] Formspree 表单已创建
- [ ] Form ID 已复制
- [ ] 3 个 HTML 文件已更新（free-audit.html、catalog.html、request-sample.html）
- [ ] 表单可以正常提交
- [ ] 邮件可以正常接收
- [ ] Formspree Dashboard 可以查看提交记录

---

## 📊 Formspree Dashboard 功能

### 查看提交记录

登录 Formspree → 选择你的表单 → 查看所有提交

### 设置自动回复

1. 进入表单设置
2. 启用 "Send a confirmation email"
3. 自定义确认邮件内容

### 导出数据

- 导出提交数据为 CSV
- 集成到 Google Sheets
- 连接到 Zapier

---

## 🔧 可选配置

### 启用确认邮件

1. 在 Formspree Dashboard 中，选择你的表单
2. 点击 **"Settings"**
3. 滚动到 **"Confirmation Emails"**
4. 启用 **"Send a confirmation email"**
5. 自定义邮件内容：

```text
感谢您的咨询！

我们已收到您的请求，将在 2 小时内回复。

如有紧急需求，请直接联系我们：
📧 info@miga.cc
📞 +86-19879476613
💬 WhatsApp: +86-19879476613

MIGAC 团队
```

### 添加重定向页面

在 `<form>` 标签中添加隐藏字段：

```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
  <input type="hidden" name="_subject" value="MIGAC 免费咨询请求">
  <input type="hidden" name="_next" value="https://miga.cc/thank-you.html">

  <!-- 其他表单字段 -->
  ...
</form>
```

---

## 🐛 问题排查

### 问题：表单提交失败

**检查清单**：
- [ ] Form ID 是否正确
- [ ] 必填字段是否都已填写
- [ ] 网络连接是否正常
- [ ] 浏览器控制台是否有错误

### 问题：没有收到邮件

**检查清单**：
- [ ] 检查垃圾邮件文件夹
- [ ] 确认接收邮箱正确
- [ ] 在 Formspree Dashboard 检查提交记录
- [ ] 检查邮箱服务器设置

### 问题：提交成功但没显示

**原因**：Formspree 默认会显示其成功页面

**解决**：添加 `_next` 字段，重定向到自定义感谢页面

---

## 📞 需要帮助？

- 📧 info@miga.cc
- 📞 +86-19879476613
- 💬 WhatsApp: +86-19879476613

---

**配置完成！🎉**
