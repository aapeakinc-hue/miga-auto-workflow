# GitHub Actions 配置指南

> **用途**: 配置GitHub Secrets，确保工作流正常运行
> **更新日期**: 2026年3月25日

---

## 🎯 概述

GitHub Actions 工作流需要以下环境变量（Secrets）才能正常运行：
- `SNOVIO_API_KEY` - Snov.io API密钥
- `RESEND_API_KEY` - Resend API密钥
- `NOTIFICATION_EMAIL` - 通知邮箱地址

---

## 📋 配置步骤

### 步骤1: 访问GitHub仓库设置

1. 打开你的GitHub仓库
2. 点击顶部的 `Settings` 标签
3. 在左侧菜单中找到 `Secrets and variables`
4. 点击 `Actions`

### 步骤2: 创建Secrets

点击 `New repository secret` 按钮，添加以下Secrets：

---

#### 2.1 SNOVIO_API_KEY

**名称**: `SNOVIO_API_KEY`

**说明**: Snov.io API密钥，用于客户搜索和邮箱验证

**获取方法**:
1. 访问 https://snov.io/
2. 登录或注册账号
3. 进入 API Settings 页面
4. 复制你的API密钥

**粘贴到Secrets**: 将API密钥粘贴到 `Value` 字段

---

#### 2.2 RESEND_API_KEY

**名称**: `RESEND_API_KEY`

**说明**: Resend API密钥，用于发送邮件和通知

**获取方法**:
1. 访问 https://resend.com/
2. 登录或注册账号
3. 进入 API Keys 页面
4. 创建新的API密钥
5. 复制API密钥

**粘贴到Secrets**: 将API密钥粘贴到 `Value` 字段

---

#### 2.3 NOTIFICATION_EMAIL

**名称**: `NOTIFICATION_EMAIL`

**说明**: 接收工作流通知的邮箱地址

**格式**: 标准邮箱格式，例如：`your-email@example.com`

**粘贴到Secrets**: 将你的邮箱地址粘贴到 `Value` 字段

**示例**: `hue@aapeakinc.com`

---

## ✅ 验证配置

### 检查Secrets是否正确配置

1. 在 `Secrets and variables → Actions` 页面
2. 检查以下Secrets是否存在：
   - ✅ `SNOVIO_API_KEY`
   - ✅ `RESEND_API_KEY`
   - ✅ `NOTIFICATION_EMAIL`

3. 点击每个Secret的眼睛图标，确认值已正确输入（不会显示完整内容，只显示部分）

---

## 🧪 测试工作流

### 手动触发工作流

1. 访问仓库的 `Actions` 标签页
2. 选择 `外贸客户开发自动化` 工作流
3. 点击 `Run workflow`
4. 选择分支（通常是 `main`）
5. 点击 `Run workflow` 按钮

### 查看运行结果

1. 等待工作流运行完成
2. 点击运行记录查看详情
3. 检查每个步骤是否成功

### 预期结果

如果配置正确，应该看到：
- ✅ 所有步骤都显示绿色（成功）
- ✅ 收到邮件通知（如果配置了`NOTIFICATION_EMAIL`）
- ✅ 日志文件已上传为附件

---

## 🚨 常见问题

### 问题1: 工作流失败，提示"RESEND_API_KEY 未配置"

**原因**: `RESEND_API_KEY` Secret未配置

**解决方法**:
1. 按照上面的步骤2.2配置 `RESEND_API_KEY`
2. 重新运行工作流

---

### 问题2: 工作流失败，提示"模块导入错误"

**原因**: Python路径问题（已在最新提交中修复）

**解决方法**:
1. 确保使用最新的代码
2. 检查是否包含以下修复：
   - `src/simple_auto_workflow_v2.py` 中的路径修复
   - `src/intelligent_auto_ops.py` 中的路径修复

---

### 问题3: 工作流成功，但没有收到邮件通知

**原因1**: `NOTIFICATION_EMAIL` 未配置

**解决方法**:
1. 按照上面的步骤2.3配置 `NOTIFICATION_EMAIL`
2. 重新运行工作流

**原因2**: 邮件被 spam 过滤

**解决方法**:
1. 检查垃圾邮件文件夹
2. 将 `noreply@aapeakinc.com` 添加到白名单

---

### 问题4: 工作流运行但没有发送邮件

**原因**: API调用失败

**解决方法**:
1. 检查工作流日志
2. 查找具体的错误信息
3. 确认API密钥是否有效
4. 确认Resend账户有足够的额度

---

## 📝 配置检查清单

在提交配置之前，请确保：

- [ ] `SNOVIO_API_KEY` 已配置
- [ ] `RESEND_API_KEY` 已配置
- [ ] `NOTIFICATION_EMAIL` 已配置
- [ ] `NOTIFICATION_EMAIL` 格式正确（包含@和域名）
- [ ] 所有Secrets的值都是有效的
- [ ] API密钥有足够的额度

---

## 🔒 安全提示

### 保护API密钥

1. **不要泄露Secrets**:
   - ❌ 不要在代码中硬编码API密钥
   - ❌ 不要在提交信息中包含API密钥
   - ❌ 不要在公开的聊天中分享API密钥

2. **定期更换API密钥**:
   - 建议每3-6个月更换一次
   - 如果怀疑密钥泄露，立即更换

3. **限制API密钥权限**:
   - 只授予必要的权限
   - 定期审查API密钥的使用情况

---

## 📞 获取帮助

如果遇到问题，请：

1. **查看文档**:
   - [GitHub Actions故障排查](GITHUB_ACTIONS_TROUBLESHOOTING.md)
   - [GitHub Actions修复指南](GITHUB_ACTIONS_FIX_GUIDE.md)

2. **检查日志**:
   - 在GitHub Actions页面查看详细日志
   - 查找具体的错误信息

3. **联系支持**:
   - 提供错误日志的完整堆栈跟踪
   - 说明配置了哪些Secrets
   - 说明错误发生在哪个步骤

---

## 🎉 配置完成

一旦配置完成并测试成功，工作流将：

- ✅ 每天北京时间上午9点自动运行
- ✅ 每天北京时间上午11点运行自动化运维
- ✅ 自动搜索潜在客户
- ✅ 自动发送开发邮件
- ✅ 自动发送运行通知

---

**文档版本**: v1.0
**创建日期**: 2026年3月25日
**维护人**: Migac Team
**最后更新**: 2026年3月25日
