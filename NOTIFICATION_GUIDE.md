# 📧 工作流通知配置指南

## 🎯 功能说明

系统现已支持**实时邮件通知**，无论工作流成功或失败，您都会收到邮件通知。

## 📋 通知内容

每次通知包含：
- ✅/❌ 运行状态（成功/失败）
- 📋 工作流名称
- ⏰ 运行时间
- 📊 运行摘要
- 🔗 GitHub Actions 链接

## 🔧 配置步骤

### 1. 配置通知邮箱（必须）

在 GitHub 仓库中添加 `NOTIFICATION_EMAIL` 密钥：

1. 访问仓库设置：https://github.com/aapeakinc-hue/miga-auto-workflow/settings/secrets/actions
2. 点击 "New repository secret"
3. 添加以下密钥：
   - **Name**: `NOTIFICATION_EMAIL`
   - **Value**: 您的邮箱地址（例如：hue@aapeakinc.com）

### 2. 确认 Resend API 密钥

通知系统使用 Resend API 发送邮件，确保已配置：
- **RESEND_API_KEY**: Resend API 密钥（应该已经配置）

### 3. 测试通知

配置完成后，可以通过手动触发工作流来测试通知：

```bash
# 方法1：通过 GitHub 网页界面
# 1. 访问 https://github.com/aapeakinc-hue/miga-auto-workflow/actions
# 2. 选择 "外贸客户开发自动化" 工作流
# 3. 点击 "Run workflow"

# 方法2：通过 GitHub CLI（如果已安装）
gh workflow run auto-workflow.yml
```

## 📅 自动通知时间

| 任务 | 时间 | 通知内容 |
|------|------|---------|
| 客户开发工作流 | 每天 9:00（北京时间） | 搜索结果、发送邮件数量、成功/失败状态 |
| 自动化运维 | 每天 11:00（北京时间） | 监控结果、优化建议、系统健康状态 |

## 🔔 通知示例

### 成功通知
```
主题：✅ 外贸客户开发工作流 - 运行成功

内容：
- 状态：运行成功
- 时间：2026-03-25 01:00:00 UTC
- 摘要：成功搜索到 10 个客户，发送了 8 封邮件
```

### 失败通知
```
主题：❌ 外贸客户开发工作流 - 运行失败

内容：
- 状态：运行失败
- 时间：2026-03-25 01:00:00 UTC
- 摘要：工作流执行失败，请查看日志
- 错误详情：...
```

## 🎨 自定义通知

您可以通过修改 `src/send_notification.py` 来自定义：
- 邮件主题
- 邮件样式
- 通知内容
- 添加更多详细信息

## 🔍 故障排除

### 问题1：没有收到通知

**可能原因：**
1. `NOTIFICATION_EMAIL` 密钥未配置
2. `RESEND_API_KEY` 密钥未配置或已过期
3. 邮箱服务拦截了邮件（检查垃圾邮件）

**解决方案：**
1. 确认 GitHub Secrets 中已正确配置 `NOTIFICATION_EMAIL`
2. 确认 `RESEND_API_KEY` 有效
3. 检查垃圾邮件箱，将 `noreply@aapeakinc.com` 添加到白名单

### 问题2：通知发送失败

**检查步骤：**
1. 访问 GitHub Actions 页面查看详细日志
2. 检查 `send_notification.py` 步骤的输出
3. 验证 Resend API 密钥是否有效

### 问题3：收到重复通知

**可能原因：**
- 工作流被多次触发（手动触发 + 定时触发）

**解决方案：**
- 避免在定时任务时间附近手动触发工作流

## 📊 通知历史

所有通知都会在 GitHub Actions 页面保留：
- 访问：https://github.com/aapeakinc-hue/miga-auto-workflow/actions
- 可以查看每次运行的详细日志和摘要

## 🚀 下一步

配置完成后，您将：
1. ✅ 每天自动收到工作流运行通知
2. ✅ 及时了解系统运行状态
3. ✅ 在失败时立即收到告警
4. ✅ 无需手动检查 GitHub Actions 页面

---

**问题反馈：** 如有任何问题，请查看 GitHub Actions 日志或联系技术支持。
