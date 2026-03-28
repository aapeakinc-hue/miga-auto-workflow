# API配置说明

## 问题解答

### Q: 为什么我已经配置过，还需要配置 Resend API 和 Snov.io token？

**A: 之前您的配置是硬编码在代码中的，现在已统一为环境变量配置。**

### 之前的配置方式

**在代码中硬编码**：
- `src/graphs/nodes/email_fetch_node.py`: `snov_api_token = "fbf98546081c2793e21d6de6540ce2ca"`
- `src/graphs/nodes/email_send_node.py`: `resend_api_key = "re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat"`

### 新的配置方式

**统一使用环境变量**（更安全、更灵活）：
```python
# 从环境变量读取，如果未设置则使用默认值
snov_api_token = os.getenv('SNOVIO_API_TOKEN', 'fbf98546081c2793e21d6de6540ce2ca')
resend_api_key = os.getenv('RESEND_API_KEY', 're_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat')
```

---

## 环境变量配置（必需）

### GitHub Secrets 配置

在 GitHub 仓库中配置以下 Secrets：

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `SNOVIO_API_TOKEN` | Snov.io API Token | ❌ | `fbf98546081c2793e21d6de6540ce2ca` |
| `SNOVIO_CLIENT_ID` | Snov.io Client ID | ❌ | `746628993ee9eda28e455e53751030bd` |
| `RESEND_API_KEY` | Resend API Key | ❌ | `re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat` |
| `OPENAI_API_KEY` | OpenAI API Key | ✅ | 无 |
| `NOTIFICATION_EMAIL` | 通知邮箱 | ❌ | `hue@aapeakinc.com` |

### 配置步骤

1. 进入 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加上述环境变量

---

## 当前配置状态

### ✅ 已完成的修改

1. **邮箱获取节点** (`src/graphs/nodes/email_fetch_node.py`)
   - ✅ 修改为从环境变量读取
   - ✅ 保留默认值（您的旧配置）

2. **邮件发送节点** (`src/graphs/nodes/email_send_node.py`)
   - ✅ 修改为从环境变量读取
   - ✅ 保留默认值（您的旧配置）

### ⚠️ 仍需环境变量的文件

以下文件**必须**配置环境变量，否则会报错：

1. **简化工作流** (`src/simple_auto_workflow.py`)
   ```python
   RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')  # 默认值为空
   SNOVIO_API_KEY = os.getenv('SNOVIO_API_KEY', '')  # 默认值为空
   ```

2. **通知系统** (`src/send_notification.py`)
   ```python
   resend_api_key = os.getenv('RESEND_API_KEY')  # 没有默认值
   ```

3. **GitHub Actions** (`.github/workflows/auto-workflow.yml`)
   ```yaml
   env:
     SNOVIO_API_KEY: ${{ secrets.SNOVIO_API_KEY }}
     RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
   ```

---

## 测试配置

### 方法1：本地测试

```bash
# 设置环境变量
export SNOVIO_API_TOKEN="fbf98546081c2793e21d6de6540ce2ca"
export SNOVIO_CLIENT_ID="746628993ee9eda28e455e53751030bd"
export RESEND_API_KEY="re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat"

# 测试工作流
python3 src/simple_auto_workflow.py
```

### 方法2：GitHub Actions 测试

1. 在 GitHub 仓库中配置 Secrets
2. 手动触发工作流：Actions → auto-workflow → Run workflow

---

## 常见问题

### Q1: 如果不配置环境变量会怎样？

**A**:
- **主工作流**（LangGraph）: ✅ 仍然可以使用（使用默认值）
- **简化工作流**: ❌ 会报错（默认值为空）
- **GitHub Actions**: ❌ 会报错（必须配置 Secrets）

### Q2: 为什么 GitHub Actions 必须配置环境变量？

**A**:
- GitHub Actions 无法读取代码中的硬编码值
- 出于安全考虑，GitHub 要求所有敏感信息都使用 Secrets
- 避免将 API Key 泄露到公共仓库

### Q3: 我可以使用其他邮箱服务吗？

**A**:
- 可以！修改 `email_send_node.py` 中的发送逻辑
- 支持的服务：SendGrid、Mailgun、AWS SES 等
- 只需修改 API 调用部分

---

## 总结

**您的旧配置**：
- ✅ 硬编码在代码中（已保留为默认值）
- ✅ 主工作流可以直接使用

**新配置要求**：
- ⚠️ 简化工作流需要环境变量
- ⚠️ GitHub Actions 需要配置 Secrets

**推荐做法**：
1. ✅ 在 GitHub Secrets 中配置所有 API Key
2. ✅ 这样所有工作流都可以正常工作
3. ✅ 更安全，避免泄露敏感信息

---

## 配置检查清单

- [ ] 在 GitHub Secrets 中配置 `SNOVIO_API_TOKEN`
- [ ] 在 GitHub Secrets 中配置 `SNOVIO_CLIENT_ID`
- [ ] 在 GitHub Secrets 中配置 `RESEND_API_KEY`
- [ ] 测试主工作流是否正常
- [ ] 测试简化工作流是否正常
- [ ] 检查 GitHub Actions 运行日志
