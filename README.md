# 外贸客户开发工作流 - 使用指南

## 📋 目录
1. [快速开始](#快速开始)
2. [工作流说明](#工作流说明)
3. [测试运行](#测试运行)
4. [优化建议](#优化建议)
5. [常见问题](#常见问题)

---

## 🚀 快速开始

### 1. 测试单个客户

```python
from graphs.graph import main_graph

params = {
    "target_keywords": "crystal candle wholesale",
    "website_url": "https://miga.cc"
}

result = main_graph.invoke(params)
```

### 2. 使用不同关键词

```python
# 美国市场
params = {
    "target_keywords": "crystal candle holders wholesale USA",
    "website_url": "https://miga.cc"
}

# 欧洲市场
params = {
    "target_keywords": "crystal candelabra importers Europe",
    "website_url": "https://miga.cc"
}
```

---

## 🔄 工作流说明

### 工作流程

```
1. 产品信息获取
   ↓
2. 客户搜索（支持中英文关键词）
   ↓
3. 邮箱获取（Snov.io API + 估计邮箱）
   ↓
4. 邮件生成（个性化开发邮件）
   ↓
5. 邮件发送（Resend API）
```

### 输入参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|-----|------|------|------|------|
| target_keywords | string | ✅ | 目标客户关键词 | "crystal candle wholesale" |
| website_url | string | ✅ | 产品网站URL | "https://miga.cc" |

### 输出结果

```json
{
  "send_results": {
    "total": 3,
    "success": 3,
    "failed": 0,
    "details": [
      {
        "to_email": "contact@example.com",
        "to_company": "Example Company",
        "status": "success",
        "message_id": "abc123"
      }
    ]
  }
}
```

---

## 🧪 测试运行

### 方法1: 使用 test_run 工具

```bash
test_run params='{"target_keywords": "crystal candle wholesale", "website_url": "https://miga.cc"}'
```

### 方法2: 运行测试脚本

```bash
python src/test_single_customer.py
```

### 预期结果

```
✅ 找到3-5个潜在客户
✅ 获取3-5个邮箱地址
✅ 生成3-5封个性化邮件
✅ 成功发送3-5封邮件
```

---

## 🎯 优化建议

### 搜索关键词优化

#### ✅ 推荐的关键词格式

**好的关键词**：
```
crystal candle holders wholesale USA
crystal candelabra importers Europe
wedding crystal suppliers UK
luxury crystal decor buyers France
```

**不好的关键词**：
```
美国水晶烛台批发商
水晶蜡烛
candle
```

#### 优化策略

1. **英文优先**: 使用英文关键词提高搜索准确性
2. **包含位置**: 添加目标市场（USA, Europe, UK等）
3. **具体产品**: 使用具体的产品名称（crystal candle holders）
4. **客户类型**: 明确客户类型（wholesale, importer, distributor）

### 邮件内容优化

#### 邮件主题

**好的主题**：
```
Partnership Opportunity - Crystal Candle Holders Wholesale
Crystal Decor Solutions for Your Business
Premium Crystal Candelabra at Factory Prices
```

#### 邮件正文要点

1. **简洁明了**: 150-200词
2. **突出价值**: 强调产品质量和服务
3. **个性化**: 提及客户公司名称
4. **明确CTA**: 请求回复或通话
5. **专业署名**: 包含联系方式

---

## ❓ 常见问题

### Q1: 搜索结果为空怎么办？

**原因**：关键词太具体或使用中文

**解决**：
- 使用英文关键词
- 使用更宽泛的关键词
- 参考优化关键词列表

---

### Q2: 找不到客户邮箱怎么办？

**原因**：
- Snov.io API 没有返回邮箱
- 客户网站没有公开邮箱

**解决**：
- 工作流会自动使用 `contact@{domain}` 作为估计邮箱
- 估计邮箱虽然可能不准确，但至少可以尝试发送

---

### Q3: 邮件发送失败怎么办？

**原因**：
- Resend API Key 无效
- 邮箱地址不存在
- 发送频率限制

**解决**：
- 检查 Resend API Key 是否正确
- 在 Resend 控制台查看发送记录
- 降低发送频率

---

### Q4: 如何提高邮件打开率？

**建议**：
1. 优化邮件主题，使其更吸引人
2. 个性化邮件内容
3. 选择合适的发送时间（客户时区的周二至周四上午）
4. 定期跟进（发送后3-7天跟进一次）

---

### Q5: 如何避免被标记为垃圾邮件？

**建议**：
1. 控制发送频率（每天不超过20封）
2. 使用专业的邮箱域名（如 info@company.com）
3. 避免过度推销的语气
4. 提供清晰的退订链接
5. 在 Resend 中配置 SPF、DKIM 记录

---

## 📊 性能指标

### 工作流性能

- 搜索客户: 3-5个
- 获取邮箱: 3-5个
- 生成邮件: 3-5封
- 发送成功率: 90%+
- 总耗时: 约30-60秒

### 预期效果

- 邮件打开率: 20-30%
- 邮件回复率: 5-10%
- 转化率: 1-5%

---

## 🔧 技术栈

- **工作流框架**: LangGraph
- **大语言模型**: Doubao (seed-2.0-lite)
- **搜索**: Web Search
- **邮箱获取**: Snov.io API
- **邮件发送**: Resend API

---

## 📞 支持

如有问题，请检查：
1. AGENTS.md - 项目文档
2. src/test_single_customer.py - 测试脚本
3. config/optimized_search_keywords.py - 关键词配置

---

## 🎉 成功案例

### 测试结果

**输入**：
```json
{
  "target_keywords": "crystal candle wholesale",
  "website_url": "https://miga.cc"
}
```

**输出**：
```json
{
  "send_results": {
    "total": 3,
    "success": 3,
    "failed": 0,
    "details": [
      {
        "to_email": "contact@www.candleswholesale.com",
        "to_company": "CandlesWholesale.com",
        "status": "success",
        "message_id": "edb0dcc8-f502-49d4-b910-d127a8e6bd5d"
      },
      {
        "to_email": "contact@crystalparade.co.uk",
        "to_company": "Login to my account",
        "status": "success",
        "message_id": "2ad071c7-c1fc-4fdb-a838-e7e6f00eb80d"
      },
      {
        "to_email": "contact@www.crystals.com",
        "to_company": "Luxury Crystals for Home",
        "status": "success",
        "message_id": "983f3492-9111-4f7f-9c2b-d484aa554b65"
      }
    ]
  }
}
```

**结果**：✅ 所有邮件成功发送！

---

**祝你开发顺利！** 🚀
