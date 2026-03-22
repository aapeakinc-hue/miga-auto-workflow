# 📊 MIGA CRM 系统使用指南

## 🎯 系统概述

MIGA CRM 系统是一个专为外贸客户开发设计的管理系统，帮助你科学管理客户、追踪跟进、分析数据。

### 核心功能
- ✅ 客户信息管理
- ✅ 互动记录追踪
- ✅ 订单管理
- ✅ 自动跟进提醒
- ✅ 客户分类管理
- ✅ 数据分析报表
- ✅ 与工作流集成

---

## 🚀 快速开始

### 1. 初始化CRM系统

```bash
python crm_system.py
```

这会创建一个SQLite数据库文件 `miga_crm.db`，包含所有必要的表结构。

### 2. 导入工作流结果

```bash
python import_workflow_results.py
```

这将自动把工作流发送的邮件结果导入到CRM系统。

### 3. 使用CRM工具

```bash
python crm_tools.py
```

提供批量导入、自动跟进、客户分类等功能。

---

## 📁 系统架构

### 核心模块

#### 1. `crm_system.py` - 核心CRM系统
**主要类**:
- `CRMDatabase`: 数据库操作类
- `CRMAnalyzer`: 数据分析类
- `Customer`, `Interaction`, `Order`: 数据模型

**主要功能**:
- 添加/查询客户
- 记录客户互动
- 追踪订单
- 生成统计报告

#### 2. `crm_tools.py` - 工具集
**主要类**:
- `CRMImporter`: 批量导入工具
- `CRMAutoFollowup`: 自动跟进工具
- `CRMSegmentManager`: 客户分类管理

**主要功能**:
- 从JSON/CSV导入客户
- 生成跟进任务
- 客户分类升级建议
- 邮件模板管理

#### 3. `import_workflow_results.py` - 工作流集成
**主要类**:
- `WorkflowToCRM`: 工作流结果解析

**主要功能**:
- 解析工作流发送结果
- 自动导入客户到CRM
- 创建初始互动记录

---

## 💡 使用场景

### 场景1: 新客户开发

**步骤**:
1. 运行工作流发送邮件
2. 获取发送结果
3. 导入到CRM系统
4. 设置自动跟进提醒

**代码示例**:
```python
from crm_system import CRMDatabase
from import_workflow_results import WorkflowToCRM

# 初始化CRM
crm = CRMDatabase("miga_crm.db")

# 导入工作流结果
results = WorkflowToCRM.process_workflow_file(crm, "workflow_results.json")
print(f"导入客户: {results['imported_customers']}")
```

### 场景2: 客户跟进管理

**步骤**:
1. 查看待跟进客户列表
2. 使用邮件模板发送跟进邮件
3. 记录互动结果
4. 更新客户分类

**代码示例**:
```python
from crm_tools import CRMAutoFollowup, CRMSegmentManager

# 获取待跟进客户
tasks = CRMAutoFollowup.generate_followup_tasks(crm, days_ahead=7)

for task in tasks:
    # 获取邮件模板
    template = CRMAutoFollowup.get_followup_template(
        task['customer_type'],
        "followup"
    )

    # 发送跟进邮件
    send_followup_email(task['email'], template)

    # 更新客户分类
    CRMSegmentManager.classify_customer(crm, task['customer_id'], new_type)
```

### 场景3: 数据分析

**步骤**:
1. 获取统计数据
2. 分析转化漏斗
3. 生成月度报告
4. 导出数据报表

**代码示例**:
```python
from crm_system import CRMAnalyzer

# 获取统计
stats = crm.get_statistics()
print(f"总客户数: {stats['total_customers']}")

# 分析转化漏斗
funnel = CRMAnalyzer.analyze_conversion_funnel(crm)
print(f"转化率: {funnel['conversion_rate']}%")

# 生成月度报告
report = CRMAnalyzer.generate_monthly_report(crm, 2026, 4)
print(report)
```

---

## 📊 客户分类体系

### A类客户（VIP客户）
**定义**: 已成交，单笔订单>$10,000
**管理策略**:
- 专属客户经理
- 优先发货
- 专属折扣
- 定期回访（每月1次）
- 赠送样品

### B类客户（重点客户）
**定义**: 已回复，有意向
**管理策略**:
- 主动跟进
- 提供产品目录
- 寄送样品
- 有限折扣（10%）

### C类客户（潜在客户）
**定义**: 已发送邮件，未回复
**管理策略**:
- 定期发送产品更新
- 节日问候
- 自动化邮件序列

### D类客户（无效客户）
**定义**: 邮箱无效、明确拒绝、无需求
**管理策略**:
- 标记为无效
- 定期清理（6个月）

---

## 🔄 跟进策略

### 跟进频率

| 客户类型 | 跟进频率 | 跟进方式 |
|----------|----------|----------|
| A类 | 每周1次 | 电话/邮件 |
| B类 | 每3天1次 | 邮件/视频会议 |
| C类 | 每2周1次 | 自动化邮件 |
| D类 | 不跟进 | - |

### 跟进模板

系统内置了不同类型客户的跟进邮件模板：
- 初始联系邮件
- 第一次跟进（3天后）
- 第二次跟进（7天后）
- 提供折扣优惠
- 节日问候

---

## 📈 数据分析指标

### 获客指标
- 每月开发客户数量
- 邮件打开率
- 邮件回复率
- 客户获取成本（CAC）

### 转化指标
- 潜在客户 → 意向客户转化率
- 意向客户 → 成交转化率
- 平均成交周期
- 平均订单价值（AOV）

### 留存指标
- 客户续单率
- 客户流失率
- 客户生命周期价值（CLV）

---

## 🛠️ 高级功能

### 1. 批量导入

从JSON或CSV文件批量导入客户：

```python
from crm_tools import CRMImporter

# 从JSON导入
results = CRMImporter.import_from_json(crm, "customers.json")

# 从CSV导入
results = CRMImporter.import_from_csv(crm, "customers.csv")
```

### 2. 客户分类升级建议

```python
from crm_tools import CRMSegmentManager

# 获取升级建议
suggestion = CRMSegmentManager.suggest_customer_upgrade(crm, customer_id)
print(f"建议升级为: {suggestion['suggested_type']}")
print(f"原因: {suggestion['reason']}")
```

### 3. 自动跟进提醒

```python
from crm_tools import CRMAutoFollowup

# 生成未来7天的跟进任务
tasks = CRMAutoFollowup.generate_followup_tasks(crm, days_ahead=7)

for task in tasks:
    if task['priority'] == 'high':
        print(f"紧急跟进: {task['company_name']}")
```

### 4. 数据导出

```python
# 导出为JSON
crm.export_to_json("crm_backup.json")

# 导出统计数据
stats = crm.get_statistics()
with open("stats.json", "w") as f:
    json.dump(stats, f)
```

---

## 📅 与年度计划集成

### 每月执行流程

1. **月初**: 执行工作流开发新客户
2. **月中**: 导入结果到CRM，设置跟进
3. **月末**: 分析数据，生成报告
4. **持续**: 跟进重点客户

### 季度复盘

1. **Q1（4-6月）**: 建立客户数据库
2. **Q2（7-9月）**: 快速扩张，优化流程
3. **Q3（10-12月）**: 旺季冲刺，提升转化
4. **Q4（1-3月）**: 年终总结，规划来年

---

## 🎯 最佳实践

### 1. 客户信息完整度
- 确保邮箱正确
- 收集联系人姓名
- 记录客户行业
- 标记客户国家

### 2. 互动记录规范
- 每次互动都要记录
- 记录互动内容
- 设置下次跟进日期
- 更新客户状态

### 3. 分类管理
- 定期检查客户分类
- 及时升级客户等级
- 淘汰无效客户
- 保持数据库清洁

### 4. 数据安全
- 定期备份数据库
- 导出数据到云端
- 保护客户隐私
- 访问权限控制

---

## 📞 技术支持

如有问题或需要帮助，请联系：
- 邮箱: info@miga.cc
- 网站: https://miga.cc

---

## 📝 更新日志

### v1.0.0 (2026-03-22)
- ✅ 初始版本发布
- ✅ 客户管理功能
- ✅ 互动记录功能
- ✅ 订单管理功能
- ✅ 自动跟进功能
- ✅ 数据分析功能
- ✅ 工作流集成

---

**MIGA CRM 系统 - 让客户管理更科学！** 🚀
