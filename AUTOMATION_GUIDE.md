# 工作流自动化配置指南

## 🎯 自动化方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|-----|------|------|-------|
| Cron 定时任务 | 灵活、免费、可控 | 需要服务器 | ⭐⭐⭐⭐⭐ |
| Cloudflare Cron | 免费、云端 | 配置较复杂 | ⭐⭐⭐⭐ |
| GitHub Actions | 免费、云端 | 运行时间限制 | ⭐⭐⭐ |

---

## 🚀 方案A：使用 Cron 定时任务（推荐）

### 步骤1：创建自动化脚本

**文件已创建**：`src/auto_workflow.py`

**功能**：
- ✅ 每天自动选择不同关键词
- ✅ 自动搜索客户并发送邮件
- ✅ 记录发送历史（避免重复）
- ✅ 生成每日报告

---

### 步骤2：配置 Cron 任务

#### Linux/Mac 系统

**编辑 crontab**：
```bash
crontab -e
```

**添加以下内容**（每天上午9点运行）：
```
0 9 * * * cd /path/to/your/project && python src/auto_workflow.py >> logs/cron.log 2>&1
```

**保存并退出**

#### Windows 系统

**使用任务计划程序**：

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天上午9点）
4. 设置操作（运行程序）
5. 程序：`python.exe`
6. 参数：`src/auto_workflow.py`
7. 起始于：`/path/to/your/project`

---

### 步骤3：创建日志目录

```bash
mkdir -p logs
```

---

### 步骤4：测试运行

```bash
python src/auto_workflow.py
```

**检查输出是否正常**

---

## ☁️ 方案B：使用 Cloudflare Cron

### 优势
- ✅ 完全免费
- ✅ 云端运行
- ✅ 无需服务器

### 步骤1：创建 Cloudflare Worker

**访问**：https://dash.cloudflare.com

**创建 Worker**：
1. 进入 Workers & Pages
2. 创建新 Worker
3. 粘贴以下代码：

```javascript
addEventListener('scheduled', event => {
  event.waitUntil(handleScheduled(event))
})

async function handleScheduled(event) {
  try {
    // 调用你的工作流（需要将工作流部署为 API）
    const response = await fetch('YOUR_WORKFLOW_API_URL', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_keywords: 'crystal candle wholesale',
        website_url: 'https://miga.cc'
      })
    })

    const result = await response.json()

    // 记录到 Cloudflare KV（可选）
    // await env.KV.put('last_run', JSON.stringify(result))

    console.log('Workflow completed:', result)

  } catch (error) {
    console.error('Scheduled task failed:', error)
  }
}
```

---

### 步骤2：配置 Cron Triggers

**在 Worker 设置中**：
1. 进入 Settings
2. 找到 Triggers
3. 添加 Cron Expression

**示例**：
```
0 9 * * *  # 每天 UTC 9点
0 9,15 * * *  # 每天 UTC 9点和15点
0 */6 * * *  # 每6小时一次
```

---

### 步骤3：部署

点击 "Deploy"

---

## 📋 方案C：手动但半自动化

### 使用 GitHub Actions

**创建文件**：`.github/workflows/auto-workflow.yml`

```yaml
name: Auto Customer Development

on:
  schedule:
    - cron: '0 1 * * *'  # 每天 UTC 1点（北京时间9点）
  workflow_dispatch:  # 支持手动触发

jobs:
  run-workflow:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run workflow
        run: python src/auto_workflow.py

      - name: Upload logs
        uses: actions/upload-artifact@v2
        with:
          name: logs
          path: logs/
```

**提交到 GitHub**：
```bash
git add .github/workflows/auto-workflow.yml
git commit -m "Add auto workflow"
git push
```

---

## ⚠️ 重要注意事项

### 1. 发送频率控制

**建议**：
- 每天最多发送 **10-20封** 邮件
- 避免被标记为垃圾邮件
- 同一客户 **30天内不要重复发送**

### 2. 关键词轮换

**自动化脚本已经实现**：
- 每天随机选择不同关键词
- 避免重复搜索相同客户
- 覆盖不同市场

### 3. 监控和记录

**自动化脚本会自动**：
- 记录所有已发送的邮箱
- 生成每日报告
- 保存日志文件

### 4. 异常处理

**自动化脚本会**：
- 捕获异常并记录
- 遇到错误继续执行
- 生成错误报告

---

## 📊 监控自动化运行

### 查看日志

```bash
# 查看 Cron 日志
tail -f logs/cron.log

# 查看每日报告
ls -lh logs/daily_report_*.txt

# 查看发送历史
cat logs/sent_emails.json
```

### 检查邮件发送

**在 Resend 控制台**：
- https://resend.com
- 查看发送记录
- 查看打开率、点击率

---

## 🔧 高级配置

### 1. 多关键词并行

修改 `auto_workflow.py`，每天运行多个关键词：

```python
# 每天运行3个不同关键词
for keyword in random.sample(OPTIMIZED_KEYWORDS, 3):
    params = {
        "target_keywords": keyword,
        "website_url": "https://miga.cc"
    }
    result = main_graph.invoke(params)
```

### 2. 智能关键词选择

根据发送历史动态选择关键词：

```python
# 选择最近30天使用最少的3个关键词
recent_keywords = [r['keyword'] for r in sent_emails[-30:]]
available_keywords = [k for k in OPTIMIZED_KEYWORDS if k not in recent_keywords]
selected_keyword = random.choice(available_keywords)
```

### 3. 邮件回复跟进

添加自动回复跟进功能：

```python
# 发送后3天，检查是否有回复
# 如果有回复，标记为"需要跟进"
# 如果没有回复，发送跟进邮件
```

---

## 💡 最佳实践

### 1. 渐进式启动

**第1周**：每天发送 **5封** 邮件
**第2周**：每天发送 **10封** 邮件
**第3周**：每天发送 **15封** 邮件
**第4周及以后**：每天发送 **20封** 邮件

### 2. 定期优化

**每周**：
- 检查发送成功率
- 检查回复率
- 优化关键词

**每月**：
- 分析转化率
- 更新关键词列表
- 优化邮件内容

### 3. 风险控制

**如果被标记为垃圾邮件**：
1. 立即停止发送
2. 检查邮件内容
3. 联系 Resend 支持
4. 等待 3-7 天后恢复

---

## 🎯 总结

### 现在的选择

**如果有服务器**：
→ 使用 **Cron 定时任务**（推荐）

**如果使用 Cloudflare**：
→ 使用 **Cloudflare Cron**

**如果使用 GitHub**：
→ 使用 **GitHub Actions**

### 自动化后的好处

- ✅ 无需每天手动操作
- ✅ 自动选择关键词
- ✅ 避免重复发送
- ✅ 生成每日报告
- ✅ 持续开发客户

---

**配置完成后，工作流将全自动运行！** 🚀
