# 🚀 Formspree 快速配置（3 步完成）

## 步骤 1：获取 Form ID（1 分钟）

1. 访问 https://formspree.io/
2. 点击 **"New Form"**
3. 填写：
   - Form Name: `MIGAC Contact Form`
   - Email: `info@miga.cc`
4. 点击 **"Create Form"**
5. **复制 Form ID**（例如：`mzbwqqzj`）

---

## 步骤 2：运行配置脚本（1 分钟）

```bash
# 编辑脚本，替换 Form ID
nano cloudflare-deploy/setup-formspree.sh

# 找到第 6 行：
FORM_ID="YOUR_FORM_ID"

# 替换为你的实际 Form ID：
FORM_ID="mzbwqqzj"

# 保存（Ctrl+X, Y, Enter）并运行
bash cloudflare-deploy/setup-formspree.sh
```

**输出**：
```
📦 备份原文件...
🔧 更新 free-audit.html...
🔧 更新 catalog.html...
🔧 更新 request-sample.html...
✅ 配置完成！
```

---

## 步骤 3：测试表单（1 分钟）

```bash
# 验证配置
grep 'formspree.io' cloudflare-deploy/free-audit.html | head -1
```

应该看到：
```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
```

然后在浏览器中打开 `cloudflare-deploy/free-audit.html`，填写并提交表单，检查邮箱是否收到邮件。

---

## ✅ 完成！

**配置时间**：约 3 分钟

**配置文件**：
- ✅ free-audit.html
- ✅ catalog.html
- ✅ request-sample.html

---

## 📊 表单字段说明

### free-audit.html
| 字段 | 说明 | 必填 |
|------|------|------|
| email | 邮箱地址 | ✅ |
| website | 网站 URL | - |
| industry | 行业类型 | ✅ |
| product | 产品类型 | - |
| quantity | 预估数量 | - |
| message | 需求说明 | - |

### catalog.html
| 字段 | 说明 | 必填 |
|------|------|------|
| email | 邮箱地址 | ✅ |

### request-sample.html
| 字段 | 说明 | 必填 |
|------|------|------|
| name | 姓名 | ✅ |
| email | 邮箱 | ✅ |
| phone | 电话 | - |
| company | 公司名称 | - |
| product | 产品类型 | ✅ |
| message | 留言 | - |

---

## 🔧 手动配置（备用）

如果脚本无法运行，手动编辑：

### free-audit.html（第 600 行）
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```
替换为：
```html
<form action="https://formspree.io/f/mzbwqqzj" method="POST">
```

### catalog.html
找到 `<form>` 标签，进行同样替换。

### request-sample.html
找到 `<form>` 标签，进行同样替换。

---

## 📞 需要帮助？

- 📧 info@miga.cc
- 📞 +86-19879476613
- 💬 WhatsApp: +86-19879476613

---

**快速完成！🎉**
