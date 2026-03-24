# 🤖 智能自动化运维系统

## 🎯 系统概述

这是一个完整的自动化运维系统，实现：

1. **自动监控** - 监控工作流运行状态
2. **自动修复** - 检测和修复常见问题
3. **数据驱动优化** - 基于数据分析优化策略
4. **A/B测试** - 测试不同方案的效果
5. **智能知识库** - 记录和学习成功经验

---

## 📊 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    智能自动化运维系统                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  监控告警   │───▶│  自动修复   │───▶│  数据分析   │     │
│  │  Monitoring │    │  Auto-Fix   │    │  Analytics  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  A/B测试   │    │  智能优化   │    │  知识库     │     │
│  │  A/B Test  │    │  Optimization│   │  Knowledge  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 核心功能

### 1. 监控告警 (Monitoring)

**文件**: `src/monitoring/auto_monitor.py`

**功能**:
- 监控 GitHub Actions 工作流运行状态
- 检测失败率和连续失败次数
- 自动发送告警通知

**使用示例**:
```python
from monitoring.auto_monitor import WorkflowMonitor

monitor = WorkflowMonitor(github_token, 'aapeakinc-hue/miga-auto-workflow')
health = monitor.check_health()

if health['status'] == 'critical':
    print(f"⚠️ 严重: {health['message']}")
```

---

### 2. 自动修复 (Auto-Fix)

**文件**: `src/monitoring/auto_monitor.py`

**功能**:
- 检测常见错误类型
- 提供自动修复建议
- 记录修复历史

**支持修复的错误**:
- `ModuleNotFoundError` - 缺失模块
- `KeyError` - 缺失密钥
- `ConnectionError` - 网络连接问题
- `TimeoutError` - 超时问题

**使用示例**:
```python
from monitoring.auto_monitor import AutoFixer

fixer = AutoFixer()
fix_plan = fixer.attempt_fix(error_log)

if fix_plan['auto_fixable']:
    print(f"✅ 可自动修复: {fix_plan['fix']}")
else:
    print(f"⚠️ 需要手动修复: {fix_plan['fix']}")
```

---

### 3. 性能跟踪 (Performance Tracking)

**文件**: `src/monitoring/auto_monitor.py`

**功能**:
- 跟踪每日统计数据
- 分析关键词性能
- 生成优化报告

**跟踪指标**:
- 发送邮件数量
- 回复数量
- 回复率
- 关键词效果

**使用示例**:
```python
from monitoring.auto_monitor import PerformanceTracker

tracker = PerformanceTracker()

# 记录每日统计
tracker.record_daily_stats('2024-03-25', {
    'emails_sent': 10,
    'responses': 3,
    'success_rate': 30.0
})

# 分析关键词性能
top_keywords = tracker.analyze_keyword_performance(10)
print(f"最佳关键词: {top_keywords}")
```

---

### 4. A/B测试 (A/B Testing)

**文件**: `src/monitoring/ab_testing.py`

**功能**:
- 创建关键词A/B测试
- 创建邮件模板A/B测试
- 分析测试结果

**测试类型**:
- 关键词测试 - 测试不同关键词的效果
- 邮件模板测试 - 测试不同邮件模板的效果

**使用示例**:
```python
from monitoring.ab_testing import ABTestManager

ab_manager = ABTestManager()

# 创建关键词测试
test_id = ab_manager.create_keyword_test(
    "美国市场测试",
    ["crystal candle holders USA", "luxury crystal USA"]
)

# 分配测试变体
variant = ab_manager.assign_variant(test_id)

# 记录结果
ab_manager.record_result(test_id, variant, {
    'emails_sent': 5,
    'responses': 2,
    'response_received': True
})
```

---

### 5. 智能优化 (Optimization Engine)

**文件**: `src/monitoring/ab_testing.py`

**功能**:
- 基于数据优化关键词选择
- 基于数据优化邮件模板
- 生成优化计划

**优化策略**:
- 优先使用高回复率的关键词
- 建议新的关键词变体
- 推荐最佳邮件模板

**使用示例**:
```python
from monitoring.ab_testing import OptimizationEngine

optimizer = OptimizationEngine()

# 优化关键词
top_keywords = optimizer.optimize_keywords()

# 建议新关键词
new_keywords = optimizer.suggest_new_keywords(top_keywords)

# 生成优化计划
plan = optimizer.generate_optimization_plan()
print(f"优化计划: {plan}")
```

---

### 6. 智能知识库 (Knowledge Base)

**文件**: `src/monitoring/knowledge_base.py`

**功能**:
- 记录客户信息
- 记录关键词性能
- 记录成功案例
- 记录经验教训
- 智能搜索和推荐

**知识库内容**:
- 客户信息
- 关键词库
- 邮件模板库
- 成功案例库
- 经验教训库

**使用示例**:
```python
from monitoring.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# 添加客户
kb.add_customer({
    'email': 'contact@example.com',
    'company': 'Example Corp',
    'region': 'USA',
    'status': 'new'
})

# 更新客户状态
kb.update_customer_status('contact@example.com', 'contacted', '已发送邮件')

# 搜索客户
customers = kb.search_customers('USA', 'region')

# 获取最佳关键词
best_keywords = kb.get_best_keywords(10)
```

---

### 7. 智能助手 (Intelligent Assistant)

**文件**: `src/monitoring/knowledge_base.py`

**功能**:
- 建议关键词
- 建议邮件模板
- 建议下一步行动
- 分析客户模式

**使用示例**:
```python
from monitoring.knowledge_base import IntelligentAssistant

assistant = IntelligentAssistant()

# 建议关键词
keywords = assistant.suggest_keywords()

# 建议邮件模板
template = assistant.suggest_email_template(customer)

# 建议下一步行动
action = assistant.suggest_next_action(customer)
```

---

## 🚀 完整的自动化运维周期

**文件**: `src/intelligent_auto_ops.py`

**运行周期**:
1. **健康检查** - 检查工作流和系统状态
2. **自动优化** - 优化关键词和邮件模板
3. **智能分析** - 分析客户和数据
4. **持续改进** - 执行A/B测试和改进

**运行频率**:
- 每天 UTC 3:00（北京时间 11:00）自动运行
- 也可以手动触发

**使用示例**:
```bash
# 手动运行完整周期
cd src
python intelligent_auto_ops.py
```

---

## 📅 自动化时间表

| 时间（北京时间） | 任务 | 说明 |
|----------------|------|------|
| 上午 9:00 | 运行工作流 | 搜索客户、发送邮件 |
| 上午 11:00 | 自动化运维 | 监控、优化、分析 |

---

## 📊 运维报告

### 报告类型

1. **运维报告** (`ops_report_*.json`)
   - 系统健康状态
   - 优化结果
   - 问题诊断

2. **分析报告** (`analysis_report_*.json`)
   - 客户洞察
   - 关键词分析
   - 推荐建议

3. **工作流日志** (`workflow-logs-*.zip`)
   - 详细运行日志
   - 发送记录
   - 错误日志

### 查看报告

**在 GitHub Actions 中**:
1. 进入 Actions 页面
2. 点击运行记录
3. 下载附件

**本地查看**:
```bash
# 查看最新运维报告
ls -lt logs/ops_*.json | head -1
cat logs/ops_report_*.json

# 查看最新分析报告
ls -lt logs/analysis_*.json | head -1
cat logs/analysis_report_*.json
```

---

## 💡 使用建议

### 1. 定期查看报告

**每天**:
- 查看工作流运行状态
- 查看发送邮件数量
- 查看邮件回复情况

**每周**:
- 查看运维报告
- 分析关键词性能
- 检查系统健康状态

**每月**:
- 总结成功案例
- 记录经验教训
- 优化策略

### 2. 持续优化

**关键词优化**:
- 定期分析关键词性能
- 淘汰低回复率的关键词
- 测试新的关键词

**邮件优化**:
- A/B测试不同邮件模板
- 优化邮件内容
- 提高回复率

**客户管理**:
- 更新客户状态
- 记录客户反馈
- 跟进有兴趣的客户

### 3. 故障处理

**工作流失败**:
- 查看错误日志
- 使用自动修复功能
- 记录问题并修复

**性能下降**:
- 检查关键词性能
- 检查邮件模板
- 执行优化周期

---

## 🔧 配置和维护

### GitHub Secrets 配置

**需要的 Secrets**:
- `SNOVIO_API_KEY` - Snov.io API Key
- `RESEND_API_KEY` - Resend API Key
- `GITHUB_TOKEN` - GitHub Token（自动提供）

### 定期维护

**清理日志文件**:
```bash
# 清理30天前的日志
find logs/ -name "*.json" -mtime +30 -delete
find logs/ -name "*.log" -mtime +30 -delete
```

**备份数据**:
```bash
# 备份知识库
cp logs/knowledge_base.json logs/backup/knowledge_base_$(date +%Y%m%d).json

# 备份发送记录
cp logs/sent_emails.json logs/backup/sent_emails_$(date +%Y%m%d).json
```

---

## 🎯 进阶使用

### 自定义A/B测试

```python
from monitoring.ab_testing import ABTestManager

ab_manager = ABTestManager()

# 创建测试
test_id = ab_manager.create_keyword_test(
    "欧洲市场测试",
    ["crystal candle holders UK", "luxury crystal Germany"]
)

# 分析结果
analysis = ab_manager.analyze_test(test_id)
print(f"最佳变体: {analysis['best_variant']}")
```

### 扩展知识库

```python
from monitoring.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# 添加成功案例
kb.add_success_story({
    'title': '成功案例：德国客户',
    'description': '使用德语邮件模板，获得良好回复',
    'lessons': ['使用客户母语','提供本地化服务']
})

# 添加经验教训
kb.add_lesson_learned({
    'title': '避免周末发送',
    'description': '周末发送的邮件回复率较低',
    'recommendation': '在工作日发送'
})
```

---

## 📞 故障排查

### 问题：工作流失败

**检查**:
1. 查看错误日志
2. 检查 Secrets 配置
3. 检查 API Key 有效性

**解决**:
- 使用自动修复功能
- 参考错误提示修复
- 记录问题并持续改进

### 问题：回复率低

**检查**:
1. 查看关键词性能
2. 查看邮件模板效果
3. 分析客户反馈

**解决**:
- 优化关键词选择
- A/B测试新邮件模板
- 根据反馈调整策略

---

## 🚀 未来扩展

### 计划中的功能

1. **机器学习优化** - 使用ML自动优化策略
2. **多渠道支持** - 支持更多客户开发渠道
3. **智能预测** - 预测客户转化概率
4. **自动化谈判** - 自动化报价和谈判流程

---

## 📚 相关文档

- [README.md](../README.md) - 项目主文档
- [QUICK_START.md](../QUICK_START.md) - 快速开始
- [SETUP_SUMMARY.md](../SETUP_SUMMARY.md) - 配置总结

---

**🎉 智能自动化运维系统已启用！**

**从今天开始，系统将自动监控、优化、分析和改进！** 🚀
