# Cloudflare Cron 自动化部署指南

## 🎯 方案概述

使用 Cloudflare Workers 和 Cron Triggers 实现外贸客户开发工作流的自动化运行，无需服务器。

---

## 📋 前置要求

- Cloudflare 账号（免费）
- 工作流 API 端点（需要部署）

---

## 🚀 部署步骤

### 步骤1：安装 Wrangler CLI

Wrangler 是 Cloudflare Workers 的命令行工具。

**安装**：
```bash
npm install -g wrangler
```

**验证安装**：
```bash
wrangler --version
```

---

### 步骤2：登录 Cloudflare

```bash
wrangler login
```

会打开浏览器，授权 Wrangler 访问你的 Cloudflare 账号。

---

### 步骤3：配置 Worker

**编辑 `cloudflare/wrangler.toml`**：

```toml
name = "miga-auto-workflow"
main = "worker.js"
compatibility_date = "2024-01-01"

[triggers]
crons = ["0 9 * * *"]  # 每天 UTC 9点
```

---

### 步骤4：部署 Worker

```bash
cd cloudflare
wrangler deploy
```

**成功后会显示**：
```
✨ Published miga-auto-workflow (X.XX sec)
  https://miga-auto-workflow.YOUR_ACCOUNT.workers.dev
```

---

### 步骤5：测试 Worker

**访问测试端点**：
```bash
curl https://miga-auto-workflow.YOUR_ACCOUNT.workers.dev/api/test
```

**应该返回**：
```json
{
  "message": "Worker is running",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "keyword": "crystal candle holders wholesale USA"
}
```

---

### 步骤6：配置 Cron Triggers

**在 Cloudflare 控制台**：

1. 登录 https://dash.cloudflare.com
2. 进入 Workers & Pages
3. 选择 `miga-auto-workflow`
4. 进入 Settings
5. 找到 Triggers
6. 确认 Cron Triggers 已配置

**或者使用命令行**：
```bash
wrangler cron schedule "0 9 * * *" --name miga-auto-workflow
```

---

## 🔧 配置工作流 API

### 方案A：将工作流部署为 API

**需要创建一个 API 端点**，Worker 可以调用。

**示例使用 Flask**：

```python
# api_server.py
from flask import Flask, request, jsonify
from graphs.graph import main_graph

app = Flask(__name__)

@app.route('/api/workflow', methods=['POST'])
def run_workflow():
    try:
        params = request.json

        # 运行工作流
        result = main_graph.invoke(params)

        return jsonify({
            "success": True,
            "total": result.get('send_results', {}).get('total', 0),
            "success": result.get('send_results', {}).get('success', 0),
            "failed": result.get('send_results', {}).get('failed', 0)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**部署 API 服务器**（可以使用 Render、Railway 等免费平台）。

---

### 方案B：使用 Cloudflare Pages Functions

**如果使用 Cloudflare Pages**：

1. 创建 `api/workflow.js`：
```javascript
export async function onRequestPost(context) {
  const { request } = context
  const params = await request.json()

  // 这里需要调用你的工作流逻辑
  // 如果工作流是 Python，可能需要使用 Cloudflare Workers AI 或其他服务

  return new Response(JSON.stringify({
    success: true,
    total: 0,
    success: 0,
    failed: 0
  }), {
    headers: { 'Content-Type': 'application/json' }
  })
}
```

---

### 方案C：简化方案（推荐）

**Worker 直接运行工作流逻辑**：

如果工作流逻辑不复杂，可以直接在 Worker 中实现。

**修改 `cloudflare/worker.js`**，添加实际的业务逻辑。

---

## 📊 监控和日志

### 查看 Worker 日志

**在 Cloudflare 控制台**：
1. 进入 Workers & Pages
2. 选择 `miga-auto-workflow`
3. 点击 Logs
4. 查看实时日志

**或使用命令行**：
```bash
wrangler tail miga-auto-workflow
```

### 查看发送记录

- 在 Resend 控制台查看邮件发送记录
- 在 `logs/sent_emails.json` 查看本地记录

---

## 🔄 常用命令

### 部署
```bash
cd cloudflare
wrangler deploy
```

### 查看日志
```bash
wrangler tail miga-auto-workflow
```

### 测试
```bash
curl https://miga-auto-workflow.YOUR_ACCOUNT.workers.dev/api/test
```

### 删除 Worker
```bash
wrangler delete miga-auto-workflow
```

---

## ⚙️ 高级配置

### 添加环境变量

**在 `wrangler.toml` 中**：
```toml
[vars]
API_ENDPOINT = "https://your-api.com"
KEYWORDS_FILE = "keywords.json"
```

**在 Worker 中使用**：
```javascript
const apiEndpoint = env.API_ENDPOINT
```

### 使用 KV 存储发送历史

**创建 KV 命名空间**：
```bash
wrangler kv:namespace create SENT_EMAILS
```

**在 `wrangler.toml` 中绑定**：
```toml
[[kv_namespaces]]
binding = "SENT_EMAILS"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**在 Worker 中使用**：
```javascript
const history = await env.SENT_EMAILS.get('history', { type: 'json' })
```

---

## 🎯 时区说明

### Cron Triggers 使用 UTC 时间

**常见时间转换**：

| 时间（北京） | UTC 时间 | Cron 表达式 |
|------------|---------|-----------|
| 上午 9:00 | 凌晨 1:00 | `0 1 * * *` |
| 下午 5:00 | 上午 9:00 | `0 9 * * *` |
| 晚上 9:00 | 下午 1:00 | `0 13 * * *` |

### 推荐配置

**北京时间下午 5 点（UTC 9点）运行**：
```toml
[triggers]
crons = ["0 9 * * *"]
```

---

## 🐛 故障排查

### 问题1：Worker 没有触发

**检查**：
1. Cron Triggers 是否配置正确
2. Worker 是否成功部署
3. 查看日志是否有错误

### 问题2：API 调用失败

**检查**：
1. API 端点是否正确
2. API 服务器是否运行
3. 网络是否可达

### 问题3：没有发送邮件

**检查**：
1. 工作流参数是否正确
2. Resend API Key 是否有效
3. 查看工作流日志

---

## 💡 最佳实践

### 1. 渐进式启动

- 第1周：每 3 天运行一次
- 第2周：每 2 天运行一次
- 第3周及以后：每天运行

### 2. 监控和告警

- 设置 Cloudflare 告警
- 定期查看 Worker 日志
- 检查邮件发送成功率

### 3. 备份和恢复

- 定期备份 KV 数据
- 保存发送历史记录
- 准备回滚方案

---

## 📞 支持

**文档**：
- Cloudflare Workers 文档：https://developers.cloudflare.com/workers/
- Wrangler CLI 文档：https://developers.cloudflare.com/workers/wrangler/

**社区**：
- Cloudflare Community：https://community.cloudflare.com/

---

## ✅ 部署检查清单

- [ ] 安装 Wrangler CLI
- [ ] 登录 Cloudflare
- [ ] 配置 `wrangler.toml`
- [ ] 部署 Worker
- [ ] 测试 Worker
- [ ] 配置 Cron Triggers
- [ ] 配置 API 端点
- [ ] 验证自动化运行

---

**配置完成后，工作流将每天自动运行！** 🚀
