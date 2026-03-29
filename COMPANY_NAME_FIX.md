# 公司名称和邮箱地址修复说明

## ✅ 已完成的修改

### 修改内容

已将所有文件中的公司名称和联系方式更新为正确的信息：

| 项目 | 之前 | 现在 |
|------|------|------|
| 公司名称 | MIGA / migac crystal co.ltd. | Yiwu Bangye Handicraft Factory |
| 发件人邮箱 | info@miga.cc | info@aapeakinc.com |
| 网站 | https://miga.cc | https://www.aapeakinc.com |

### 修改的文件

1. **src/graphs/nodes/email_generate_node.py**
   - 邮件生成节点，修改公司名称和邮箱

2. **src/graphs/nodes/email_send_node.py**
   - 邮件发送节点，修改发件人邮箱和署名

3. **src/graphs/state.py**
   - 状态定义，修改默认网站 URL

4. **src/auto_workflow_with_real_api.py**
   - 主工作流，修改默认网站 URL

5. **.github/workflows/main-workflow.yml**
   - GitHub Actions workflow，修改默认网站 URL

---

## ⚠️ 重要：域名验证问题

### 当前状态

测试运行时邮件发送失败，错误信息：

```
The aapeakinc.com domain is not verified.
Please, add and verify your domain on https://resend.com/domains
```

### 原因

Resend API 要求发送邮件的域名必须经过验证。使用 `info@aapeakinc.com` 发送邮件需要先在 Resend 控制台上验证 `aapeakinc.com` 域名。

---

## 🔧 解决方案

### 方案 1：验证 aapeakinc.com 域名（推荐）

#### 步骤 1：访问 Resend 控制台

```
https://resend.com/domains
```

#### 步骤 2：添加域名

1. 点击 "Add Domain"
2. 输入域名：`aapeakinc.com`
3. 点击 "Add Domain"

#### 步骤 3：验证域名

Resend 会提供 DNS 记录，需要在域名注册商处添加：

```
类型: TXT
主机记录: _resend
记录值: [Resend 提供的验证值]
```

或者使用 CNAME 记录：

```
类型: CNAME
主机记录: resend._domainkey
记录值: [Resend 提供的值]
```

#### 步骤 4：等待验证

DNS 记录生效后（通常 10-30 分钟），Resend 会自动验证域名。

#### 步骤 5：创建发件人

1. 在 Resend 控制台中点击 "Senders"
2. 点击 "Add Sender"
3. 输入发件人邮箱：`info@aapeakinc.com`
4. 发送验证邮件到该邮箱
5. 点击验证邮件中的链接

### 方案 2：使用 Resend 默认域名（临时方案）

如果不想验证域名，可以使用 Resend 提供的默认域名：

**@resend.dev** - Resend 开发测试域名

**注意**：
- 只用于测试
- 可能会进入垃圾邮件
- 不适合正式业务

**修改方法**：

将所有 `info@aapeakinc.com` 改为 `test@yourdomain.resend.dev`

---

## 📋 检查清单

### 域名验证

- [ ] 在 Resend 控制台添加 aapeakinc.com 域名
- [ ] 在域名注册商处添加 DNS 记录
- [ ] 等待 DNS 生效（10-30 分钟）
- [ ] Resend 自动验证域名
- [ ] 创建发件人 `info@aapeakinc.com`
- [ ] 验证发件人邮箱

### 测试

- [ ] 域名验证后，重新测试工作流
- [ ] 检查邮件是否能正常发送
- [ ] 检查收件人是否收到邮件
- [ ] 检查邮件内容是否正确

---

## 📊 邮件内容预览

### 修改后的邮件

```
Subject: Partnership Opportunity with Yiwu Bangye Handicraft Factory - [客户公司名]

Dear [客户姓名],

[个性化邮件内容...]

Best regards,
Yiwu Bangye Handicraft Factory Team
Email: info@aapeakinc.com
Website: https://www.aapeakinc.com
```

---

## ✅ 总结

- ✅ 公司名称已修正为 "Yiwu Bangye Handicraft Factory"
- ✅ 邮箱地址已修改为 info@aapeakinc.com
- ✅ 网站地址已修改为 https://www.aapeakinc.com
- ⚠️ 需要在 Resend 控制台验证 aapeakinc.com 域名
- ⚠️ 验证后才能正常发送邮件

---

## 📞 需要帮助？

如果域名验证遇到问题，可以：

1. 查阅 Resend 官方文档：https://resend.com/docs/domains/introduction
2. 联系域名注册商的客服
3. 使用临时方案：@resend.dev 域名进行测试
