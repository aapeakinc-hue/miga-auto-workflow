# 📧 通知邮箱配置

## ✅ 已配置邮箱

- **通知邮箱**: `aapeakinc@gmail.com`
- **配置状态**: ⚠️ 需要手动添加到 GitHub Secrets

## 🔧 手动配置步骤

由于本地环境没有安装 GitHub CLI，请在浏览器中手动配置：

### 1. 访问 GitHub Secrets 设置

点击以下链接：
```
https://github.com/aapeakinc-hue/miga-auto-workflow/settings/secrets/actions
```

### 2. 添加 Secret

1. 点击 **"New repository secret"** 按钮
2. 填写以下信息：
   - **Name**: `NOTIFICATION_EMAIL`
   - **Value**: `aapeakinc@gmail.com`
3. 点击 **"Add secret"** 保存

### 3. 验证配置

添加后，你应该在列表中看到：
- ✅ NOTIFICATION_EMAIL

---

## 📅 配置完成后

您将在以下时间收到通知：

| 任务 | 时间（北京时间） | 通知内容 |
|------|-----------------|---------|
| 客户开发工作流 | 每天 9:00 | 搜索结果、发送邮件数量 |
| 自动化运维 | 每天 11:00 | 监控结果、优化建议 |

---

## 🧪 测试通知

配置完成后，可以手动触发测试：

### 方法1：通过 GitHub 网页

1. 访问：https://github.com/aapeakinc-hue/miga-auto-workflow/actions
2. 点击 **"外贸客户开发自动化"** 工作流
3. 点击右侧 **"Run workflow"**
4. 点击 **"Run workflow"** 按钮

### 方法2：等待下次自动运行

- **今天 11:00** - 自动化运维（约 1 小时后）
- **明天 9:00** - 客户开发工作流

---

## 🔔 通知示例

### 成功通知
```
主题：✅ 外贸客户开发工作流 - 运行成功

收件人：aapeakinc@gmail.com

内容：
✅ 运行成功

📋 基本信息
- 工作流：外贸客户开发工作流
- 时间：2026-03-25 01:00:00 UTC

📊 运行摘要
成功搜索到 10 个客户，发送了 8 封邮件
```

### 失败通知
```
主题：❌ 外贸客户开发工作流 - 运行失败

收件人：aapeakinc@gmail.com

内容：
❌ 运行失败

📋 基本信息
- 工作流：外贸客户开发工作流
- 时间：2026-03-25 01:00:00 UTC

📊 运行摘要
工作流执行失败，请查看 GitHub Actions 日志
```

---

## ❓ 问题排查

### 没有收到通知？

1. **检查垃圾邮件箱**
   - 通知可能被误判为垃圾邮件
   - 将 `noreply@aapeakinc.com` 添加到白名单

2. **验证 Secret 配置**
   - 确认 NOTIFICATION_EMAIL 已正确添加
   - 值为：`aapeakinc@gmail.com`

3. **检查 GitHub Actions 日志**
   - 访问：https://github.com/aapeakinc-hue/miga-auto-workflow/actions
   - 查看最新运行的日志
   - 搜索 "send_notification" 步骤

---

## 📊 查看运行历史

所有运行记录都在 GitHub Actions 页面：

https://github.com/aapeakinc-hue/miga-auto-workflow/actions

可以看到：
- ✅ 运行状态（成功/失败）
- 📊 运行摘要
- 📋 详细日志
- 📥 下载的附件（日志文件）

---

**配置完成后，您将不再担心"不知道是否运行"的问题！** 🎉
