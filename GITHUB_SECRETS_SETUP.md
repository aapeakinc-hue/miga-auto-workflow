# GitHub Secrets 配置指南

## 📋 需要配置的 Secrets

### 必需配置

| 变量名 | 值 | 说明 |
|--------|------|------|
| `SNOVIO_API_TOKEN` | `fbf98546081c2793e21d6de6540ce2ca` | Snov.io API Token |
| `SNOVIO_CLIENT_ID` | `746628993ee9eda28e455e53751030bd` | Snov.io Client ID |
| `RESEND_API_KEY` | `re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat` | Resend API Key |
| `NOTIFICATION_EMAIL` | `hue@aapeakinc.com` | 通知邮箱 |

### 可选配置

| 变量名 | 说明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI API Key（如需使用 OpenAI） |
| `GITHUB_TOKEN` | GitHub API Token（GitHub 自动提供，无需配置） |

---

## 🔧 详细配置步骤

### 步骤 1：进入 GitHub 仓库

1. 访问您的仓库：
   ```
   https://github.com/aapeakinc-hue/miga-auto-workflow
   ```

2. 点击仓库顶部的 **Settings** 标签

3. 在左侧边栏中找到：
   ```
   Secrets and variables → Actions
   ```

### 步骤 2：添加 Secrets

点击 **New repository secret** 按钮，然后逐个添加：

#### ✅ Secret #1: SNOVIO_API_TOKEN

- **Name**: `SNOVIO_API_TOKEN`
- **Value**: `fbf98546081c2793e21d6de6540ce2ca`
- 点击 **Add secret**

#### ✅ Secret #2: SNOVIO_CLIENT_ID

- **Name**: `SNOVIO_CLIENT_ID`
- **Value**: `746628993ee9eda28e455e53751030bd`
- 点击 **Add secret**

#### ✅ Secret #3: RESEND_API_KEY

- **Name**: `RESEND_API_KEY`
- **Value**: `re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat`
- 点击 **Add secret**

#### ✅ Secret #4: NOTIFICATION_EMAIL

- **Name**: `NOTIFICATION_EMAIL`
- **Value**: `hue@aapeakinc.com`
- 点击 **Add secret**

---

## ✅ 配置验证

### 方法 1：在 GitHub 上验证

1. 回到 **Secrets and variables → Actions**
2. 查看 **Repository secrets** 列表
3. 确认所有 4 个 Secrets 都在列表中

### 方法 2：通过 Workflow 测试

1. 进入 **Actions** 标签
2. 选择 **外贸客户开发自动化** workflow
3. 点击 **Run workflow** → **Run workflow**
4. 查看运行日志，确认没有 Secret 相关错误

---

## 🔐 安全提示

### ⚠️ 重要注意事项

1. **不要提交到代码库**
   - 永远不要将 API Key 提交到代码中
   - 始终使用 GitHub Secrets

2. **定期轮换 API Keys**
   - 定期更换 Snov.io 和 Resend 的 API Keys
   - 更新 GitHub Secrets 中的值

3. **访问控制**
   - 确保只有授权人员可以访问 Secrets
   - 限制仓库的写权限

4. **监控使用情况**
   - 定期检查 API 使用量
   - 监控异常活动

---

## 🎯 配置完成后的功能

### 启用的功能

✅ **GitHub Actions 自动化**
- 每天 UTC 1:00 (北京时间 9:00) 自动运行主工作流
- 每天 UTC 3:00 (北京时间 11:00) 自动运行运维任务

✅ **简化工作流**
- 可以使用简化版自动化工作流
- 支持多种优化策略

✅ **通知系统**
- 工作流运行成功/失败时发送通知
- 包含运行摘要和日志链接

### 工作流程

```
触发（定时/手动）
  ↓
检出代码
  ↓
设置 Python 环境
  ↓
安装依赖
  ↓
运行工作流（使用 Secrets）
  ↓
上传日志和报告
  ↓
发送通知
```

---

## 📊 配置检查清单

配置完成后，请确认以下事项：

- [ ] SNOVIO_API_TOKEN 已添加
- [ ] SNOVIO_CLIENT_ID 已添加
- [ ] RESEND_API_KEY 已添加
- [ ] NOTIFICATION_EMAIL 已添加
- [ ] Secrets 显示在列表中（值被隐藏）
- [ ] 手动运行 workflow 测试
- [ ] 检查运行日志无错误
- [ ] 确认邮件发送成功

---

## 🐛 常见问题

### Q1: Secret 添加后不生效？

**A**: 检查以下几点：
1. 确认 Secret 名称完全匹配（区分大小写）
2. 确认没有多余的空格
3. 检查 workflow 文件中引用的变量名是否正确

### Q2: 如何更新 Secret？

**A**:
1. 进入 Secrets 列表
2. 找到要更新的 Secret
3. 点击 **Update** 按钮
4. 修改值并保存

### Q3: 如何删除 Secret？

**A**:
1. 进入 Secrets 列表
2. 找到要删除的 Secret
3. 点击 **Delete** 按钮
4. 确认删除

### Q4: Secret 有字符限制吗？

**A**: 是的
- 名称：最多 255 个字符
- 值：最多 1 MB
- 只能使用字母、数字、下划线

---

## 📚 参考文档

- [GitHub Secrets 官方文档](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Actions 官方文档](https://docs.github.com/en/actions)

---

## ✅ 配置完成确认

配置完成后，您应该能够：

1. ✅ 在 GitHub Secrets 列表中看到 4 个 Secrets
2. ✅ 手动运行 workflow 无错误
3. ✅ 自动化任务按时执行
4. ✅ 接收成功/失败通知

**配置完成后，请点击 "Run workflow" 进行测试！**
