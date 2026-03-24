# GitHub Actions 自动化部署指南

## 🎯 方案概述

使用 GitHub Actions 实现外贸客户开发工作流的自动化运行，无需服务器、完全免费。

---

## 📋 前置要求

- GitHub 账号（免费）
- 项目代码上传到 GitHub 仓库

---

## 🚀 部署步骤（5分钟搞定）

### 步骤1：创建 GitHub 仓库

1. 访问 https://github.com
2. 点击右上角 "+" → "New repository"
3. 仓库名称：例如 `miga-auto-workflow`
4. 设置为 Public 或 Private（都免费）
5. 点击 "Create repository"

---

### 步骤2：上传代码

**方法A：使用 GitHub 网页界面（简单）**

1. 在仓库页面点击 "uploading an existing file"
2. 将所有项目文件拖拽上传
3. 滚动到页面底部，点击 "Commit changes"

**方法B：使用 Git 命令（推荐）**

在本地项目目录执行：

```bash
# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始提交"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/miga-auto-workflow.git

# 推送代码
git branch -M main
git push -u origin main
```

---

### 步骤3：配置 GitHub Secrets

**为什么要配置 Secrets？**

保护敏感信息（API Key），避免泄露到公开仓库。

**操作步骤**：

1. 进入 GitHub 仓库
2. 点击 "Settings" 标签
3. 在左侧菜单找到 "Secrets and variables" → "Actions"
4. 点击 "New repository secret"

**需要配置的 Secrets**：

| Secret 名称 | 值 | 说明 |
|------------|-----|------|
| `SNOVIO_API_KEY` | 你的 Snov.io API Key | 用于客户搜索 |
| `RESEND_API_KEY` | 你的 Resend API Key | 用于邮件发送 |

**配置示例**：

- Name: `SNOVIO_API_KEY`
- Value: `你的真实 API Key`
- 点击 "Add secret"

重复以上步骤，添加 `RESEND_API_KEY`。

---

### 步骤4：验证 Actions 配置

**检查配置文件**：

确保 `.github/workflows/auto-workflow.yml` 文件存在且内容正确。

**文件位置**：
```
miga-auto-workflow/
├── .github/
│   └── workflows/
│       └── auto-workflow.yml  ← 这个文件
├── src/
├── config/
└── ...
```

---

### 步骤5：手动测试运行

**第一次运行（手动触发）**：

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 在左侧找到 "外贸客户开发自动化"
4. 点击右侧的 "Run workflow"
5. 点击绿色的 "Run workflow" 按钮

**查看运行结果**：

1. 等待运行完成（约 2-5 分钟）
2. 点击运行记录查看详细日志
3. 检查是否成功发送邮件

---

### 步骤6：验证定时任务

**确认定时任务已设置**：

1. 进入 Actions 页面
2. 查看 "外贸客户开发自动化" 工作流
3. 应该显示 "Scheduled" 标记

**定时时间**：
- **运行时间**：每天 UTC 1:00（北京时间上午 9:00）
- **下次运行**：在 Actions 页面可以看到下次运行时间

---

## 📊 监控和管理

### 查看运行历史

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 点击 "外贸客户开发自动化"
4. 查看所有运行记录

### 查看运行日志

1. 点击具体的运行记录
2. 点击 "run-auto-workflow" 任务
3. 展开每个步骤查看详细日志

### 查看发送记录

**方法1：在 GitHub Actions 中下载**

1. 点击运行记录
2. 滚动到页面底部
3. 在 "Artifacts" 区域找到 "workflow-logs"
4. 点击下载

**方法2：查看 Resend 控制台**

访问 https://resend.com 查看所有发送记录。

---

## 🔧 常用操作

### 修改运行时间

**编辑 `.github/workflows/auto-workflow.yml`**：

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # UTC 时间
```

**常见时间设置**：

| 时间（北京） | Cron 表达式 |
|------------|-----------|
| 上午 9:00 | `0 1 * * *` |
| 中午 12:00 | `0 4 * * *` |
| 下午 6:00 | `0 10 * * *` |
| 晚上 9:00 | `0 13 * * *` |
| 每天两次（9点和15点） | `0 1,7 * * *` |

修改后提交代码即可生效。

### 手动触发运行

**方法1：在 GitHub 网页界面**

1. 进入 Actions 页面
2. 点击 "Run workflow"
3. 点击 "Run workflow"

**方法2：使用 GitHub CLI**

```bash
gh workflow run "auto-workflow.yml"
```

### 暂停定时任务

**方法1：禁用工作流**

1. 进入 Actions 页面
2. 点击 "外贸客户开发自动化"
3. 点击右侧的 "..." 菜单
4. 选择 "Disable workflow"

**方法2：注释掉 schedule**

编辑 `.github/workflows/auto-workflow.yml`，注释掉 schedule 部分：

```yaml
# on:
#   schedule:
#     - cron: '0 1 * * *'

on:
  workflow_dispatch:  # 只允许手动触发
```

---

## 🐛 故障排查

### 问题1：Actions 失败

**检查**：
1. 查看 Actions 日志，找到错误信息
2. 检查 Secrets 是否配置正确
3. 检查 Python 依赖是否安装成功

**常见错误**：
- `KeyError: 'SNOVIO_API_KEY'` → 检查 Secrets 配置
- `ModuleNotFoundError` → 检查依赖安装
- `API Key invalid` → 检查 API Key 是否正确

### 问题2：没有发送邮件

**检查**：
1. 查看 Actions 日志中的错误信息
2. 查看 Resend 控制台
3. 检查客户搜索结果是否为空

### 问题3：定时任务没有运行

**检查**：
1. 确认 schedule 配置正确
2. 确认工作流已启用
3. 检查 GitHub Actions 是否被限制（免费账户）

---

## 💡 最佳实践

### 1. 定期检查

- 每周查看一次 Actions 运行记录
- 每月检查一次发送成功率
- 定期优化关键词

### 2. 监控告警

在 `.github/workflows/auto-workflow.yml` 中添加失败通知：

```yaml
- name: 通知失败
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: '工作流执行失败',
        body: '工作流在 ' + new Date().toISOString() + ' 执行失败，请检查日志。'
      })
```

### 3. 版本管理

- 使用 Git 分支管理不同配置
- 使用 GitHub Releases 记录重要版本
- 定期备份发送历史记录

---

## 📊 成本说明

### GitHub Actions 免费额度

**公开仓库**：
- ✅ 无限制使用

**私有仓库**：
- ✅ 每月 2000 分钟
- ✅ 每次 30 分钟限制
- ✅ 你的用量：约 5-10 分钟/天（完全够用）

**超出费用**：
- ❌ 通常不会超出，无需担心

---

## 🎯 总结

### 配置完成后的效果

✅ **每天上午 9 点自动运行**
✅ **自动搜索潜在客户**
✅ **自动发送开发邮件**
✅ **完全免费使用**
✅ **无需服务器**
✅ **无需电脑开机**

### 你的日常工作

📧 **每天检查邮箱回复**
💬 **回复有兴趣的客户**
📝 **跟进潜在客户**
💰 **成交！**

---

## 📞 支持

**文档**：
- GitHub Actions 文档：https://docs.github.com/en/actions
- Cron 表达式：https://crontab.guru/

**社区**：
- GitHub Community：https://github.community/

---

**配置完成后，从明天开始每天自动运行！** 🚀
