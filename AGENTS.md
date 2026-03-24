## 项目概述
- **名称**: 外贸客户开发工作流
- **功能**: 自动化搜索客户、获取邮箱、生成邮件、发送邮件

---

## 节点清单

| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| product_fetch | `nodes/product_fetch_node.py` | task | 从网站提取产品信息 | - | - |
| customer_search | `nodes/customer_search_node.py` | task | 基于关键词搜索潜在客户 | - | - |
| email_fetch | `nodes/email_fetch_node.py` | task | 使用 Snov.io API 获取客户邮箱 | - | Snov.io API Key |
| email_generate | `nodes/email_generate_node.py` | agent | 生成个性化开发邮件 | - | `config/email_generate_llm_cfg.json` |
| email_send | `nodes/email_send_node.py` | task | 使用 Resend API 发送邮件 | - | Resend API Key |

**类型说明**: task(任务节点) / agent(大模型节点) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

---

## 工作流流程

```
1. product_fetch (产品信息获取)
   ↓
2. customer_search (客户搜索)
   ↓
3. email_fetch (邮箱获取)
   ↓
4. email_generate (邮件生成)
   ↓
5. email_send (邮件发送)
   ↓
完成
```

---

## 技能使用

### 节点 customer_search
- 使用 Web Search 技能搜索潜在客户
- 支持中英文关键词
- 自动过滤无效网站

### 节点 email_fetch
- 使用 Snov.io API 获取客户邮箱
- API Key: fbf98546081c2793e21d6de6540ce2ca
- Client ID: 746628993ee9eda28e455e53751030bd
- 使用估计邮箱作为备选方案

### 节点 email_generate
- 使用大语言模型技能
- 生成个性化外贸开发邮件
- 模型: doubao-seed-2-0-lite-260215

### 节点 email_send
- 使用 Resend API 发送邮件
- API Key: re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat
- 发件邮箱: info@miga.cc

---

## 配置文件

### 邮件生成配置
- 文件: `config/email_generate_llm_cfg.json`
- 模型: doubao-seed-2-0-lite-260215
- 温度: 0.7

### 优化关键词配置
- 文件: `config/optimized_search_keywords.py`
- 包含多市场、多客户类型的关键词组合

---

## 测试脚本

### 单客户测试
- 文件: `src/test_single_customer.py`
- 功能: 测试单个客户的邮件发送流程
- 使用: `python src/test_single_customer.py`

---

## API 密钥

### Snov.io
- API Token: fbf98546081c2793e21d6de6540ce2ca
- Client ID: 746628993ee9eda28e455e53751030bd

### Resend
- API Key: re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat

---

## 使用示例

### 工作流输入

```json
{
  "target_keywords": "crystal candle wholesale",
  "website_url": "https://miga.cc"
}
```

### 工作流输出

```json
{
  "send_results": {
    "total": 3,
    "success": 3,
    "failed": 0,
    "details": [
      {
        "to_email": "contact@example.com",
        "status": "success",
        "message_id": "abc123"
      }
    ]
  }
}
```

---

## 优化建议

### 搜索关键词优化
1. 使用英文关键词提高搜索准确性
2. 针对目标市场定制关键词
3. 定期测试和优化关键词效果

### 邮件内容优化
1. 个性化邮件内容
2. 突出产品优势
3. 明确行动号召

### 客户筛选优化
1. 过滤无效网站（电商平台、B2B平台）
2. 过滤中文网站（针对海外市场）
3. 优先选择欧美客户

---

## 已知问题和解决方案

### 问题1: 搜索结果为空
- 原因: 中文关键词搜索效果差
- 解决: 自动转换为英文关键词搜索

### 问题2: 邮箱获取失败
- 原因: Snov.io API 没有返回邮箱
- 解决: 使用估计邮箱 (contact@{domain}) 作为备选

### 问题3: 邮件发送失败
- 原因: Resend API Key 无效
- 解决: 更新为有效的 API Key

---

## 更新日志

### 2026-03-25
- ✅ 修复中文关键词搜索问题
- ✅ 优化邮箱获取逻辑
- ✅ 添加估计邮箱备选方案
- ✅ 修复 Resend API Key
- ✅ 添加测试脚本
- ✅ 更新 AGENTS.md 文档
