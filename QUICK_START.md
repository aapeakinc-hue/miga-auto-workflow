# 🚀 GitHub Actions 快速配置指南

## 📋 当前状态

### ✅ 已完成
- ✅ 所有代码已提交到本地 Git 仓库
- ✅ GitHub Actions 配置文件已创建
- ✅ 自动化脚本已创建
- ✅ 所有文档已创建

### ❌ 需要你操作
- ❌ 创建 GitHub 仓库
- ❌ 推送代码到 GitHub
- ❌ 配置 GitHub Secrets
- ❌ 测试运行

---

## 🎯 4 步完成配置（预计 10-15 分钟）

### 步骤 1：创建 GitHub 仓库（2 分钟）

1. 访问 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写信息：
   - **Repository name**: `miga-auto-workflow`
   - **Description**: 外贸客户开发自动化工作流
   - **Public/Private**: 都可以（推荐 Private）
4. 点击 "Create repository"

**注意**：创建仓库后，GitHub 会显示一个页面，包含仓库地址和推送命令。

---

### 步骤 2：推送代码到 GitHub（3 分钟）

**复制你的仓库地址**（类似这样）：
```
https://github.com/YOUR_USERNAME/miga-auto-workflow.git
```

**在项目目录执行以下命令**：

```bash
# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/miga-auto-workflow.git

# 推送代码到 GitHub
git branch -M main
git push -u origin main
```

**如果提示需要认证**：
- 使用 Personal Access Token（推荐）
- 或者使用 SSH 密钥

**成功后会显示**：
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/YOUR_USERNAME/miga-auto-workflow.git
 * [new branch]      main -> main
```

---

### 步骤 3：配置 GitHub Secrets（5 分钟）

**为什么要配置 Secrets？**

保护 API Keys，避免泄露到公开仓库。

**操作步骤**：

1. **进入 GitHub 仓库**
2. **点击 "Settings" 标签**（仓库页面顶部）
3. **在左侧菜单找到**：
   - "Secrets and variables"
   - → "Actions"
4. **点击 "New repository secret"**

**添加第一个 Secret（SNOVIO_API_KEY）**：

- **Name**: `SNOVIO_API_KEY`
- **Value**: `fbf98546081c2793e21d6de6540ce2ca`
- 点击 "Add secret"

**添加第二个 Secret（RESEND_API_KEY）**：

- **Name**: `RESEND_API_KEY`
- **Value**: `re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat`
- 点击 "Add secret"

**注意**：
- Name 必须完全一致（大写字母和下划线）
- Value 必须完全正确
- 添加后无法查看 Value（只能看到 Name）

---

### 步骤 4：测试运行（2 分钟）

**第一次运行（手动触发）**：

1. **进入 GitHub 仓库**
2. **点击 "Actions" 标签**
3. **在左侧找到**："外贸客户开发自动化"
4. **点击右侧的**："Run workflow" 按钮
5. **点击绿色的**："Run workflow" 按钮

**查看运行结果**：

1. **等待运行完成**（约 2-5 分钟）
2. **点击运行记录**查看详细日志
3. **检查每个步骤**是否成功

**预期结果**：
- ✅ 步骤 "检出代码" - 成功
- ✅ 步骤 "设置 Python 3.12" - 成功
- ✅ 步骤 "安装依赖" - 成功
- ✅ 步骤 "运行自动化工作流" - 成功
- ✅ 发送 3-5 封邮件
- ✅ 步骤 "上传日志" - 成功

**如果运行失败**：
- 查看错误信息
- 检查 Secrets 配置
- 查看 Actions 日志详情

---

## 📊 验证配置

### 检查定时任务

1. 进入 Actions 页面
2. 查看 "外贸客户开发自动化"
3. 应该显示 "Scheduled" 标记

**运行时间**：
- **每天 UTC 1:00**（北京时间上午 9:00）
- **下次运行时间**：在 Actions 页面可以看到

---

## 🔧 常见问题

### Q1: git push 失败，提示认证错误

**解决方案**：

1. 使用 Personal Access Token：
   - GitHub → Settings → Developer settings → Personal access tokens
   - 生成新 Token，选择 "repo" 权限
   - 使用 Token 作为密码（不是用户名）

2. 或者使用 SSH：
   ```bash
   # 生成 SSH 密钥
   ssh-keygen -t ed25519 -C "your_email@example.com"

   # 添加到 GitHub SSH keys
   # Settings → SSH and GPG keys → New SSH key

   # 使用 SSH 地址推送
   git remote set-url origin git@github.com:YOUR_USERNAME/miga-auto-workflow.git
   git push -u origin main
   ```

### Q2: Actions 运行失败

**检查**：
1. 查看错误信息
2. 检查 Secrets 是否配置正确
3. 检查 API Keys 是否有效

**常见错误**：
- `KeyError: 'SNOVIO_API_KEY'` → 检查 Secrets 配置
- `ModuleNotFoundError` → 检查依赖安装
- `API Key invalid` → 检查 API Keys

### Q3: 如何修改运行时间？

**编辑 `.github/workflows/auto-workflow.yml`**：

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # 修改这里
```

**修改后推送**：
```bash
git add .github/workflows/auto-workflow.yml
git commit -m "修改运行时间"
git push
```

---

## 📈 日常使用

### 查看运行历史

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看 "外贸客户开发自动化" 运行记录

### 查看发送记录

**方法1：在 GitHub Actions 中下载日志**
1. 点击运行记录
2. 滚动到页面底部
3. 在 "Artifacts" 区域下载 "workflow-logs"

**方法2：查看 Resend 控制台**
访问 https://resend.com

### 手动触发运行

**方法1：在 GitHub 网页界面**
1. 进入 Actions 页面
2. 点击 "Run workflow"

**方法2：使用 GitHub CLI**
```bash
gh workflow run "auto-workflow.yml"
```

---

## 🎯 配置完成后的效果

### 每天 9 点自动运行

✅ 自动搜索 3-5 个潜在客户
✅ 自动发送 3-5 封开发邮件
✅ 自动记录发送历史
✅ 自动生成每日报告

### 你只需要

📧 **每天检查邮箱回复**（info@miga.cc）
💬 **回复有兴趣的客户**
📝 **跟进潜在客户**
💰 **成交！**

---

## 📚 相关文档

- [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - 配置总结
- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - 详细指南
- [README.md](README.md) - 项目文档

---

## 💡 温馨提示

1. **配置完成后，从明天开始自动运行**
2. **可以随时手动触发测试**
3. **完全免费，无需服务器**
4. **无需电脑开机**

---

**🚀 开始配置吧！4 步搞定！**
