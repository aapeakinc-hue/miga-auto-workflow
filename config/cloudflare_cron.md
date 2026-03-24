# Cloudflare Workers Cron Triggers 配置
# 用于在 Cloudflare Pages/Workers 中设置定时任务

# 每天上午 9 点 UTC（北京时间下午 5 点）
0 9 * * *

# 每天上午 9 点和下午 3 点 UTC
0 9,15 * * *

# 每隔 6 小时运行一次
0 */6 * * *

# 使用方法：
# 1. 在 Cloudflare Workers 中创建一个 Worker
# 2. 配置 Cron Triggers
# 3. 调用工作流 API
# 4. 记录发送历史

# 示例 Worker 代码：
"""
addEventListener('scheduled', event => {
  event.waitUntil(handleScheduled(event))
})

async function handleScheduled(event) {
  try {
    // 调用你的工作流 API
    const response = await fetch('https://your-api-endpoint/workflow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_keywords: 'crystal candle wholesale',
        website_url: 'https://miga.cc'
      })
    })

    const result = await response.json()
    console.log('Workflow result:', result)

  } catch (error) {
    console.error('Scheduled task failed:', error)
  }
}
"""
