/**
 * Cloudflare Worker - 自动触发外贸客户开发工作流
 * 每天自动运行，无需服务器
 */

addEventListener('scheduled', event => {
  event.waitUntil(handleScheduled(event))
})

async function handleScheduled(event) {
  const timestamp = new Date().toISOString()
  console.log(`[${timestamp}] 🤖 自动化工作流启动`)

  try {
    // 工作流参数
    const params = {
      target_keywords: getRandomKeyword(),
      website_url: 'https://miga.cc'
    }

    console.log(`[${timestamp}] 🔍 关键词: ${params.target_keywords}`)

    // 这里需要替换为你的实际工作流 API 端点
    // 如果工作流在 Cloudflare Pages 上，可以调用 Pages Function
    // 如果工作流在其他地方，需要提供 API URL

    // 示例：调用 API（需要你提供实际的 API URL）
    const response = await callWorkflowAPI(params)

    if (response.success) {
      console.log(`[${timestamp}] ✅ 工作流执行成功`)
      console.log(`[${timestamp}] 📊 发送总数: ${response.total}`)
      console.log(`[${timestamp}] ✅ 成功: ${response.success}`)
      console.log(`[${timestamp}] ❌ 失败: ${response.failed}`)
    } else {
      console.log(`[${timestamp}] ❌ 工作流执行失败`)
      console.log(`[${timestamp}] 错误: ${response.error}`)
    }

  } catch (error) {
    console.error(`[${timestamp}] ❌ 执行异常:`, error)
  }
}

/**
 * 随机选择关键词
 */
function getRandomKeyword() {
  const keywords = [
    "crystal candle holders wholesale USA",
    "crystal candelabra importers America",
    "crystal home decor wholesalers United States",
    "luxury crystal decor buyers USA",
    "crystal candle holders wholesalers UK",
    "crystal candelabra importers Europe",
    "crystal home decor distributors Germany",
    "luxury crystal decor buyers France",
    "gift shops crystal decor wholesalers",
    "home decor stores crystal candle holders",
    "wedding planners crystal candelabra suppliers",
    "luxury hotels crystal decor suppliers",
    "crystal candle holders bulk buyers",
    "crystal candelabra wholesale importers"
  ]

  // 根据日期选择关键词，避免每天相同
  const dayOfMonth = new Date().getDate()
  return keywords[dayOfMonth % keywords.length]
}

/**
 * 调用工作流 API
 * 注意：需要替换为你的实际 API 端点
 */
async function callWorkflowAPI(params) {
  // 方案A：如果工作流在 Cloudflare Pages 上
  // const apiUrl = 'https://your-project.pages.dev/api/workflow'

  // 方案B：如果工作流在其他服务器
  // const apiUrl = 'https://your-server.com/api/workflow'

  // 方案C：暂时返回测试结果（需要配置实际API）
  console.log('⚠️  需要配置实际的工作流 API 端点')

  return {
    success: true,
    total: 0,
    success: 0,
    failed: 0,
    message: '需要配置实际的 API 端点'
  }

  // 实际调用示例（取消注释并修改URL）：
  /*
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'  // 如果需要认证
      },
      body: JSON.stringify(params)
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const result = await response.json()
    return {
      success: true,
      ...result
    }

  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
  */
}

/**
 * 手动触发（用于测试）
 */
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event))
})

async function handleRequest(event) {
  const url = new URL(event.request.url)

  // API 端点：GET /api/test
  if (url.pathname === '/api/test') {
    return new Response(JSON.stringify({
      message: 'Worker is running',
      timestamp: new Date().toISOString(),
      keyword: getRandomKeyword()
    }), {
      headers: { 'Content-Type': 'application/json' }
    })
  }

  return new Response('Worker is active. Visit /api/test to test.', { status: 200 })
}
