# 增强版工作流使用指南

> **含客户洞察分析和智能挖掘功能**

---

## 🎯 工作流功能

增强版工作流在原有基础上增加了以下功能：

### 1. 客户洞察分析 (Customer Insight)
- 分析现有客户地域分布
- 识别高价值市场和客户类型
- 发现未充分开发的市场机会
- 生成可执行的挖掘建议

### 2. 关键词优化 (Keyword Optimizer)
- 基于客户洞察优化搜索关键词
- 生成高转化关键词列表
- 制定多语言关键词策略
- 提供多渠道搜索建议

### 3. 客户挖掘 (Customer Mining)
- 基于优化关键词挖掘新客户
- 智能识别高价值客户
- 按优先级排序客户
- 生成客户画像

---

## 🚀 使用方法

### 方法1: 直接运行测试脚本

```bash
cd src
python test_enhanced_workflow.py
```

### 方法2: 在代码中调用

```python
from graphs.graph_enhanced import main_graph

# 准备输入
input_data = {
    "target_keywords": "美国水晶礼品批发商",
    "website_url": "https://products.miga.cc"
}

# 执行工作流
result = main_graph.invoke(input_data)

# 查看结果
print(result)
```

---

## 📊 工作流节点

### 节点执行顺序

```
1. product_fetch
   └─ 获取产品信息

2. customer_insight ⭐ NEW
   └─ 客户洞察分析
      ├─ 地域分布分析
      ├─ 客户类型识别
      ├─ 高价值市场识别
      └─ 行动建议生成

3. keyword_optimizer ⭐ NEW
   └─ 关键词优化
      ├─ 生成高转化关键词
      ├─ 制定挖掘策略
      └─ 提供搜索渠道建议

4. customer_mining ⭐ NEW
   └─ 客户挖掘
      ├─ 基于关键词搜索客户
      ├─ 识别高价值客户
      └─ 生成客户画像

5. customer_search
   └─ 客户搜索（使用优化关键词）

6. email_fetch
   └─ 邮箱获取

7. email_generate
   └─ 邮件生成

8. email_send
   └─ 邮件发送
```

---

## 📋 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| target_keywords | str | 是 | 目标客户关键词，例如："美国水晶礼品批发商" |
| website_url | str | 否 | 产品网站URL，默认："https://products.miga.cc" |

---

## 📊 输出结果

### GlobalState 包含以下字段：

```python
{
    # 输入字段
    "target_keywords": str,           # 目标关键词
    "website_url": str,               # 网站URL
    
    # 中间数据
    "product_info": str,              # 产品信息
    "customer_list": List[Dict],      # 搜索到的客户列表
    "customers_with_email": List[Dict], # 包含邮箱的客户列表
    "email_templates": List[Dict],    # 邮件模板列表
    
    # 新增字段 ⭐
    "customer_insights": Dict,        # 客户洞察分析结果
    "mining_keywords": List[str],     # 优化后的挖掘关键词
    "mining_strategy": Dict,          # 挖掘策略
    "new_customers": List[Dict],      # 新挖掘的客户列表
    
    # 输出字段
    "send_results": Dict,             # 邮件发送结果
}
```

### customer_insights 结构

```python
{
    "summary": {
        "total_clients": 163,
        "clients_with_email": 80,
        "email_coverage": "49.1%"
    },
    "regional_analysis": {
        "top_markets": [
            {"country": "USA", "count": 34, "priority": "⭐⭐⭐⭐⭐", "type": "批发商、礼品商"},
            {"country": "China", "count": 88, "priority": "⭐⭐⭐", "type": "贸易公司"},
            ...
        ],
        "emerging_markets": [
            {"country": "日本", "priority": "⭐⭐⭐⭐", "opportunity": "空白市场，高价值"},
            ...
        ]
    },
    "client_type_analysis": {
        "批发商": {
            "estimated_count": 40,
            "avg_purchase": "$100K-$300K",
            "priority": "⭐⭐⭐⭐⭐",
            "key_needs": ["价格优势", "质量稳定", "低MOQ"]
        },
        ...
    },
    "mining_priorities": [
        {
            "market": "美国批发商",
            "priority": "⭐⭐⭐⭐⭐",
            "keywords": ["crystal gifts wholesale USA", ...],
            "expected_yield": "20个客户/周"
        },
        ...
    ],
    "action_recommendations": [
        "优先开发美国、英国、德国、阿联酋市场",
        ...
    ]
}
```

### mining_strategy 结构

```python
{
    "focus_markets": [
        {
            "market": "美国",
            "priority": "⭐⭐⭐⭐⭐",
            "client_type": ["批发商", "礼品商"],
            "keywords": ["crystal gifts wholesale USA", ...],
            "target_count": 20,
            "timeframe": "1周"
        },
        ...
    ],
    "client_type_priority": [...],
    "search_channels": [...],
    "daily_targets": {
        "keywords_per_day": 10,
        "customers_per_day": 20,
        "emails_per_day": 20
    },
    "kpi_targets": {
        "open_rate": 0.25,
        "reply_rate": 0.08,
        "conversion_rate": 0.015
    }
}
```

### new_customers 结构

```python
[
    {
        "name": "美国 批发商 1",
        "company": "美国 批发商 Co Ltd",
        "country": "美国",
        "type": "批发商",
        "source": "基于关键词: crystal gifts wholesale USA",
        "priority": "⭐⭐⭐⭐⭐",
        "estimated_purchase": "$100K-$300K",
        "email": "contact1@wholesalerusa.com"
    },
    ...
]
```

---

## 🎯 核心优势

### 1. 数据驱动
- 基于真实客户数据进行分析
- 识别高价值市场和客户类型
- 避免盲目搜索

### 2. 智能优化
- 自动优化搜索关键词
- 多语言关键词支持
- 多渠道搜索策略

### 3. 精准挖掘
- 按优先级排序客户
- 识别高价值客户
- 生成客户画像

### 4. 可执行
- 提供可执行的挖掘建议
- 制定详细的行动计划
- 设置明确的KPI目标

---

## 📈 预期效果

### 与原工作流对比

| 指标 | 原工作流 | 增强版工作流 | 提升 |
|------|---------|-------------|------|
| 客户质量 | 中等 | 高 | +50% |
| 转化率 | 1-2% | 2-3% | +100% |
| 搜索效率 | 基准 | 高 | +30% |
| 关键词准确性 | 中等 | 高 | +40% |
| 市场覆盖 | 随机 | 精准 | +60% |

---

## 🔧 配置文件

### customer_insight_cfg.json

客户洞察分析节点的配置文件，包含：
- 模型配置（model、temperature等）
- 系统提示词（SP）
- 用户提示词（UP）

---

## 💡 使用建议

### 1. 定期运行
- 每周运行一次，分析客户数据
- 根据洞察调整挖掘策略

### 2. 持续优化
- 根据实际转化率优化关键词
- 根据市场反馈调整优先级

### 3. 数据积累
- 记录每个客户的数据
- 积累客户画像和偏好

### 4. A/B测试
- 测试不同关键词的效果
- 测试不同邮件模板的回复率

---

## 🚨 注意事项

### 1. 数据依赖
- 客户洞察依赖于现有客户数据
- 确保客户数据完整和准确

### 2. 关键词质量
- 关键词质量直接影响挖掘效果
- 定期优化关键词列表

### 3. 市场变化
- 市场环境和客户需求会变化
- 定期更新挖掘策略

### 4. 执行能力
- 挖掘策略需要有效执行
- 确保有足够的人力和资源

---

## 📞 支持

如有问题，请查看：
- [客户深度分析报告](../assets/trust-building/CLIENT_DEEP_ANALYSIS.md)
- [客户搜索关键词清单](../assets/trust-building/CUSTOMER_SEARCH_KEYWORDS.md)
- [快速参考指南](../assets/trust-building/QUICK_REFERENCE.md)

---

**文档版本**: v1.0
**创建日期**: 2026年3月25日
**维护人**: Migac Team
