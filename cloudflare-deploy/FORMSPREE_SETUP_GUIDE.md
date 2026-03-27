# Formspree 表单配置指南

## 📋 概述

本指南将帮助你在 5 分钟内完成 Formspree 表单配置，让 MIGAC 网站的 3 个表单（免费咨询、目录下载、样品申请）能够正常接收用户提交。

---

## 🚀 快速开始（推荐）

### 步骤 1：获取 Form ID

1. 登录 https://formspree.io/
2. 点击 **"New Form"**
3. 填写表单信息：
   - **Form Name**: `MIGAC Contact Form`
   - **Email**: `info@miga.cc`（你的接收邮箱）
4. 创建后，复制 **Form ID**（例如：`mzbwqqzj`）

### 步骤 2：运行配置脚本

```bash
# 编辑脚本，填入你的 Form ID
nano cloudflare-deploy/setup-formspree.sh

# 找到这一行：
FORM_ID="YOUR_FORM_ID"

# 替换为你的实际 Form ID：
FORM_ID="mzbwqqzj"  # 替换为你实际的 Form ID

# 保存并退出（Ctrl+X, Y, Enter）

# 执行脚本
bash cloudflare-deploy/setup-formspree.sh
```

### 步骤 3：验证配置

```bash
# 检查配置是否正确
grep 'formspree.io' cloudflare-deploy/free-audit.html | head -1
```

应该看到类似：
```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
```

**完成！** 🎉

---

## 📝 手动配置方法

如果你不熟悉使用脚本，可以手动编辑每个文件：

### 配置 free-audit.html

1. 打开 `cloudflare-deploy/free-audit.html`
2. 找到第 200 行左右的 `<form>` 标签：
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

3. 替换为：
```html
<form action="https://formspree.io/f/你的Form_ID" method="POST">
```

例如：
```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
```

### 配置 catalog.html

重复上述步骤，更新 `cloudflare-deploy/catalog.html` 中的表单。

### 配置 request-sample.html

重复上述步骤，更新 `cloudflare-deploy/request-sample.html` 中的表单。

---

## ✅ 配置清单

完成配置后，请检查以下项目：

### 表单字段映射

Formspree 会自动识别表单中的 `name` 属性。以下是我们使用的字段：

#### free-audit.html 表单字段：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `email` | text | 邮箱地址（必填） |
| `website` | url | 网站 URL |
| `industry` | select | 行业类型（必填） |
| `product` | select | 产品类型 |
| `quantity` | select | 预估数量 |
| `message` | textarea | 需求说明 |

#### catalog.html 表单字段：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `email` | text | 邮箱地址（必填） |

#### request-sample.html 表单字段：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `name` | text | 姓名（必填） |
| `email` | text | 邮箱（必填） |
| `phone` | text | 电话 |
| `company` | text | 公司名称 |
| `product` | select | 产品类型（必填） |
| `message` | textarea | 留言 |

---

## 🧪 测试表单

配置完成后，测试表单功能：

### 方法 1：本地测试

1. 在浏览器中打开文件：
   - `cloudflare-deploy/free-audit.html`
   - `cloudflare-deploy/catalog.html`
   - `cloudflare-deploy/request-sample.html`

2. 填写表单并提交

3. 检查邮箱 `info@miga.cc` 是否收到提交

### 方法 2：在线测试（部署后）

1. 部署到 Cloudflare Pages
2. 访问 https://miga.cc/free-audit.html
3. 填写并提交表单
4. 检查邮箱

---

## 📊 Formspree Dashboard 功能

### 查看提交记录

登录 Formspree Dashboard 后，你可以：

- 查看所有表单提交
- 导出提交数据为 CSV
- 查看表单统计（提交数量、时间等）

### 设置自动回复

1. 在 Formspree Dashboard 中，选择你的表单
2. 点击 **"Settings"**
3. 滚动到 **"Confirmation Emails"**
4. 启用 **"Send a confirmation email"**
5. 自定义确认邮件内容

示例确认邮件：
```
感谢您的咨询！

我们已收到您的请求，将在 2 小时内回复。

如有紧急需求，请直接联系我们：
📧 info@miga.cc
📞 +86-19879476613
💬 WhatsApp: +86-19879476613

MIGAC 团队
```

### 设置邮件转发

如果你希望表单提交同时发送给多个邮箱：

1. 在表单设置中，点击 **"Forwarding"**
2. 添加额外的转发邮箱
3. 保存设置

---

## 🔧 高级配置

### 验证码（ReCAPTCHA）

启用 ReCAPTCHA 可以防止垃圾邮件：

1. 在 Formspree Dashboard 中，找到你的表单
2. 点击 **"Settings"**
3. 滚动到 **"Spam Protection"**
4. 启用 **"ReCAPTCHA"**
5. 选择 ReCAPTCHA 版本（v2 或 v3）

### 自定义重定向页面

提交表单后，重定向到感谢页面：

在 `<form>` 标签中添加：
```html
<form action="https://formspree.io/f/你的Form_ID" method="POST">
  <!-- 添加隐藏字段 -->
  <input type="hidden" name="_subject" value="MIGAC 免费咨询请求">
  <input type="hidden" name="_next" value="https://miga.cc/thank-you.html">

  <!-- 表单字段 -->
  ...
</form>
```

### 创建感谢页面（可选）

创建 `cloudflare-deploy/thank-you.html`：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Thank You | MIGAC</title>
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #1a237e, #0d47a1);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            padding: 50px;
        }
        h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }
        p {
            font-size: 20px;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        .btn {
            display: inline-block;
            padding: 15px 40px;
            background: #ffd700;
            color: #1a237e;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ 提交成功！</h1>
        <p>感谢您的咨询！我们将在 2 小时内回复。</p>
        <a href="index.html" class="btn">返回首页</a>
    </div>
</body>
</html>
```

---

## 🐛 常见问题

### 问题 1：表单提交后显示 "Error 400"

**原因**：Form ID 错误或表单字段配置问题

**解决**：
1. 检查 Form ID 是否正确
2. 确保必填字段都已填写
3. 检查 Formspree Dashboard 中的错误日志

### 问题 2：没有收到邮件

**原因**：邮件被误判为垃圾邮件

**解决**：
1. 检查垃圾邮件文件夹
2. 在邮箱中添加 `info@miga.cc` 到白名单
3. 在 Formspree 检查提交记录是否成功

### 问题 3：表单显示不正确

**原因**：HTML 文件编码或路径问题

**解决**：
1. 确保文件使用 UTF-8 编码
2. 检查文件路径是否正确
3. 清除浏览器缓存后重试

---

## 📞 需要帮助？

- 📧 info@miga.cc
- 📞 +86-19879476613
- 💬 WhatsApp: +86-19879476613

---

**配置完成！🎉 现在可以测试表单了！**
