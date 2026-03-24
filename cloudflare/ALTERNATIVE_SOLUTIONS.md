# Cloudflare Cron 方案说明

## ⚠️ 重要说明

### 当前限制

**问题**：
- 你的工作流代码是 **Python** 编写的
- Cloudflare Workers 只支持 **JavaScript**
- 需要一个额外的 API 端点供 Worker 调用

---

## 💡 解决方案对比

### 方案1：部署工作流为 API（推荐）

**步骤**：
1. 将工作流部署为 API 服务器（Flask/FastAPI）
2. 部署到免费平台（Render/Railway）
3. Cloudflare Worker 调用这个 API

**优点**：
- ✅ 利用现有工作流代码
- ✅ Worker 只负责定时触发
- ✅ API 服务器可以复用

**缺点**：
- ❌ 需要部署额外的服务
- ❌ 增加了一个依赖点

---

### 方案2：简化使用 Cron（最简单⭐）

**推荐使用原计划的 Cron 定时任务**

**原因**：
- ✅ 不需要额外的 API 服务器
- ✅ 直接运行 Python 工作流
- ✅ 配置更简单
- ✅ 完全免费

**配置**：
```bash
# 编辑 crontab
crontab -e

# 添加（每天上午9点）
0 9 * * * cd /path/to/project && python src/auto_workflow.py >> logs/cron.log 2>&1
```

---

### 方案3：重写工作流为 JavaScript（不推荐）

**将 Python 工作流重写为 JavaScript**

**优点**：
- ✅ 完全在 Cloudflare 上运行
- ✅ 无需额外服务

**缺点**：
- ❌ 需要重写所有代码
- ❌ 耗时较长
- ❌ 可能丢失功能

---

## 🎯 我的推荐

### 推荐使用 **方案2：Cron 定时任务**

**理由**：
1. 你已经有了完整的工作流代码（Python）
2. `src/auto_workflow.py` 已经测试成功
3. Cron 配置最简单
4. 无需任何额外服务
5. 完全免费

---

## 🚀 如果一定要用 Cloudflare

### 需要做的工作：

#### 1. 部署 API 服务器

**使用 Flask 创建 API**：

```python
# api_server.py
from flask import Flask, request, jsonify
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from graphs.graph import main_graph

app = Flask(__name__)

@app.route('/api/workflow', methods=['POST'])
def run_workflow():
    try:
        params = request.json

        # 运行工作流
        result = main_graph.invoke(params)

        send_results = result.get('send_results', {})

        return jsonify({
            "success": True,
            "total": send_results.get('total', 0),
            "success": send_results.get('success', 0),
            "failed": send_results.get('failed', 0)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

#### 2. 部署到免费平台

**选项A：Render**

1. 注册 https://render.com
2. 创建新的 Web Service
3. 上传代码
4. 设置环境变量
5. 部署

**选项B：Railway**

1. 注册 https://railway.app
2. 创建新项目
3. 上传代码
4. 部署

**选项C：PythonAnywhere**

1. 注册 https://www.pythonanywhere.com
2. 创建 Web App
3. 上传代码
4. 部署

---

#### 3. 配置 Worker 调用 API

**修改 `cloudflare/worker.js`**：

```javascript
async function callWorkflowAPI(params) {
  const apiUrl = 'https://your-api-server.com/api/workflow'

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const result = await response.json()
    return result

  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}
```

---

## 📊 方案对比总结

| 方案 | 复杂度 | 时间 | 成本 | 推荐度 |
|-----|-------|------|------|-------|
| Cron 定时任务 | ⭐ | 5分钟 | 免费 | ⭐⭐⭐⭐⭐ |
| Cloudflare + API | ⭐⭐⭐⭐ | 1-2小时 | 免费 | ⭐⭐⭐ |
| 重写为 JS | ⭐⭐⭐⭐⭐ | 数天 | 免费 | ⭐ |

---

## 💬 建议

### 如果你没有服务器

**选择**：**Cron 定时任务**

**原因**：
- 你的代码已经在当前环境运行
- `src/auto_workflow.py` 测试成功
- 可以设置定时任务（如果环境支持）

---

### 如果一定要用 Cloudflare

**选择**：**部署 API 服务器 + Cloudflare Worker**

**步骤**：
1. 部署 API 服务器到 Render
2. 部署 Cloudflare Worker
3. 配置 Worker 调用 API

---

## 🎯 立即行动

### 最简单方案：使用 Cron

**如果当前环境支持定时任务**：

```bash
# 每天上午9点运行
0 9 * * * cd /workspace/projects && python src/auto_workflow.py >> logs/cron.log 2>&1
```

### 或者：手动运行脚本

**每天手动运行一次**：

```bash
python src/auto_workflow.py
```

---

## 📞 需要帮助？

**如果你想配置 Cloudflare + API 方案**，告诉我：

1. 你想使用哪个免费平台部署 API？（Render/Railway/其他）
2. 我会帮你创建完整的部署文件和说明

**如果你想简化使用 Cron**，告诉我：

1. 你的环境是否支持定时任务？
2. 我会帮你配置

---

## 💡 总结

**对于你的情况，最推荐使用 Cron 定时任务**

原因：
- 代码已经准备好了
- 测试成功了
- 配置最简单
- 完全免费

**Cloudflare Worker 方案需要额外部署 API 服务器，增加了复杂度。**

---

**你想使用哪个方案？我可以帮你详细配置！** 💬
