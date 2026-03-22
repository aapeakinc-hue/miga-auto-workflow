# 📊 MIGA 数据驱动外贸客户开发系统

## 🎯 系统概述

本系统是一个完整的数据驱动外贸客户开发解决方案，以海关数据、市场规模和大数据为支撑，实现智能目标设定、每日工作计划、自动化报告生成和目标持续调整。

### 核心特性

- 📈 **市场数据分析** - 基于海关数据和市场规模进行潜力评估
- 🎯 **智能目标设定** - 根据市场数据自动生成年度和月度目标
- 📋 **每日计划管理** - 自动化每日工作计划和次日计划
- 📊 **多维度报告** - 日、周、月、年度总结报告
- 📧 **邮件自动发送** - 所有报告自动发送到 info@miga.cc
- 🔄 **目标智能调整** - 基于达成度自动调整下月目标

---

## 🏗️ 系统架构

### 核心模块

```
数据驱动外贸客户开发系统
│
├── 📊 市场研究模块 (market_research.py)
│   ├── 海关数据管理
│   ├── 市场规模分析
│   ├── 市场潜力评估
│   └── 竞争格局分析
│
├── 🎯 目标设定模块 (goal_setting.py)
│   ├── 年度目标设定
│   ├── 月度目标分解
│   ├── 目标达成追踪
│   └── 基于市场的目标生成
│
├── 📋 每日计划模块 (daily_planner.py)
│   ├── 每日工作计划
│   ├── 执行记录
│   ├── 次日计划
│   └── 每日总结生成
│
├── 📊 报告生成模块 (report_generator.py)
│   ├── 每日报告
│   ├── 周度报告
│   ├── 月度报告
│   └── 年度报告
│
├── 📧 邮件发送模块 (summary_sender.py)
│   ├── 每日总结邮件
│   ├── 周度总结邮件
│   ├── 月度总结邮件
│   ├── 年度总结邮件
│   └── 目标调整通知
│
├── 🔄 目标调整模块 (goal_adjuster.py)
│   ├── 绩效分析
│   ├── 调整因子计算
│   ├── 目标自动调整
│   └── 调整报告生成
│
└── 🎭 工作流编排器 (workflow_orchestrator.py)
    ├── 系统初始化
    ├── 每日工作流
    ├── 周度工作流
    ├── 月度工作流
    └── 年度工作流
```

---

## 🚀 快速开始

### 1. 系统初始化

```bash
# 初始化所有模块
python workflow_orchestrator.py
```

这将自动执行：
- ✅ 创建所有数据库
- ✅ 导入示例市场数据
- ✅ 初始化示例目标
- ✅ 创建示例每日计划
- ✅ 运行完整工作流

### 2. 运行每日工作流

```bash
# 运行每日工作流（默认今天，美国市场）
python run_daily_workflow.py

# 指定日期和市场
python run_daily_workflow.py --date 2026-03-22 --market USA
```

### 3. 运行周度工作流

```bash
# 运行周度工作流（默认本周，美国市场）
python run_weekly_workflow.py

# 指定周开始日期和市场
python run_weekly_workflow.py --start-date 2026-03-17 --market USA
```

### 4. 运行月度工作流

```bash
# 运行月度工作流（默认本月，美国市场）
python run_monthly_workflow.py

# 指定年份、月份和市场
python run_monthly_workflow.py --year 2026 --month 3 --market USA
```

### 5. 运行年度工作流

```bash
# 运行年度工作流（默认今年）
python run_annual_workflow.py

# 指定年份
python run_annual_workflow.py --year 2026
```

---

## 📊 数据驱动目标设定

### 市场数据支撑

系统基于以下数据源设定目标：

#### 1. 海关数据
- 各国水晶产品进口数据
- 月度/年度进口量
- 进口金额

#### 2. 市场规模数据
- 各国水晶产品市场规模
- 市场增长率
- 行业趋势

#### 3. 竞争格局数据
- 主要竞争对手
- 市场份额
- 竞争对手收入

### 目标设定流程

```
市场数据收集
    ↓
市场潜力分析
    ↓
市场规模估算
    ↓
目标市场份额设定
    ↓
年度目标生成
    ↓
月度目标分解
    ↓
每日任务分配
```

### 目标达成追踪

系统自动追踪以下指标：

| 指标 | 定义 | 目标 |
|------|------|------|
| 客户开发目标 | 每月开发的潜在客户数量 | 基于市场份额 |
| 意向客户目标 | 每月获得的意向客户数量 | 基于转化率 |
| 成交客户目标 | 每月成交的客户数量 | 基于订单量 |
| 收入目标 | 每月的收入目标 | 基于市场规模 |

---

## 📋 每日工作流程

### 1. 每日计划（自动化）

系统自动生成每日工作计划，包括：

- 🎯 客户搜索工作流执行
- 📧 开发邮件发送（20封/天）
- 📩 邮箱回复检查与跟进
- 📊 CRM系统更新
- 📈 当日数据分析

### 2. 执行记录（自动化/人工）

系统自动记录：
- ✅ 已完成任务
- ⏳ 未完成任务
- 📊 关键指标（邮件发送数、新增客户数、回复数）
- ⚠️ 遇到的挑战
- 💡 经验教训

### 3. 次日计划（自动化）

系统自动创建次日计划，基于：
- 今日未完成任务
- 明日优先级设置
- 预期结果

### 4. 每日总结（自动化）

系统自动生成每日总结，包括：
- 📊 关键指标
- 🎯 亮点成就
- ⚠️ 存在问题
- 📋 行动计划
- 📧 自动发送到 info@miga.cc

---

## 📈 报告体系

### 每日报告

**发送时间**: 每天晚上 22:00

**内容**:
- 今日数据（任务完成率、邮件发送数、新增客户数）
- 今日亮点
- 存在问题
- 行动计划

**接收邮箱**: info@miga.cc

### 周度报告

**发送时间**: 每周日 22:00

**内容**:
- 本周数据汇总
- 周度目标达成情况
- 本周亮点
- 存在问题
- 改进建议

**接收邮箱**: info@miga.cc

### 月度报告

**发送时间**: 每月最后一天 22:00

**内容**:
- 本月数据汇总
- 月度目标达成情况
- 趋势分析
- 本月亮点
- 存在问题
- 改进建议
- 目标调整建议

**接收邮箱**: info@miga.cc

### 年度报告

**发送时间**: 每年12月31日 22:00

**内容**:
- 年度目标达成情况
- 各市场表现对比
- 年度亮点
- 存在问题
- 改进建议
- 下年度规划建议

**接收邮箱**: info@miga.cc

---

## 🔄 目标调整机制

### 调整触发条件

系统在以下情况下自动调整目标：

#### 1. 每月调整

**触发时机**: 月末

**调整依据**:
- 月度目标达成率
- 平均达成率 > 120%: 提高 15%
- 平均达成率 80%-100%: 保持不变
- 平均达成率 60%-80%: 降低 10%
- 平均达成率 < 60%: 降低 20%

**调整对象**: 下月目标

#### 2. 季度调整

**触发时机**: 季末

**调整依据**:
- 季度平均达成率
- 综合考虑各月表现

**调整对象**: 下季度目标

### 调整流程

```
月末/季末
    ↓
分析绩效数据
    ↓
计算达成率
    ↓
确定调整策略
    ↓
应用调整因子
    ↓
更新目标
    ↓
发送调整通知
    ↓
执行新目标
```

### 调整通知

系统会自动发送调整通知到 info@miga.cc，包括：
- 📊 目标达成情况
- 🔄 调整建议
- 💡 综合建议

---

## 📞 使用场景

### 场景1: 首次部署

```bash
# 1. 初始化系统
python workflow_orchestrator.py

# 2. 运行每日工作流
python run_daily_workflow.py

# 3. 检查邮件
# 查看 info@miga.cc 收到的每日总结
```

### 场景2: 定期执行

```bash
# 每天执行（建议使用 cron 定时任务）
0 22 * * * cd /path/to/project && python run_daily_workflow.py

# 每周日执行周度工作流
0 22 * * 0 cd /path/to/project && python run_weekly_workflow.py

# 每月最后一天执行月度工作流
0 22 28-31 * * cd /path/to/project && python run_monthly_workflow.py
```

### 场景3: 手动调整目标

```python
from goal_setting import GoalSetting
from market_research import MarketResearch

# 初始化
market = MarketResearch()
goal_system = GoalSetting()

# 生成市场报告
market_report = market.generate_market_report("USA")

# 基于市场数据生成目标
goals = goal_system.generate_goals_based_on_market_data(
    market_report,
    target_market_share=0.05
)

# 设定年度目标
goal_system.set_annual_goal(
    year=2026,
    market="USA",
    customer_development_goal=goals["annual_goals"]["customer_development_goal"],
    intention_customer_goal=goals["annual_goals"]["intention_customer_goal"],
    deal_customer_goal=goals["annual_goals"]["deal_customer_goal"],
    revenue_goal=goals["annual_goals"]["revenue_goal"]
)
```

---

## 📊 数据库说明

### market_data.db - 市场数据数据库

**表结构**:
- `market_data` - 海关数据
- `market_size` - 市场规模数据
- `competitors` - 竞争对手数据

### goals.db - 目标数据库

**表结构**:
- `annual_goals` - 年度目标
- `monthly_goals` - 月度目标
- `goal_achievement` - 目标达成记录
- `adjustment_records` - 调整记录

### daily_planner.db - 每日计划数据库

**表结构**:
- `daily_plans` - 每日计划
- `daily_execution` - 每日执行记录
- `next_day_plan` - 次日计划

---

## 🔧 配置说明

### API 配置

#### Resend API（邮件发送）
- **API Key**: `re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F`
- **发件邮箱**: `info@miga.cc`
- **接收邮箱**: `info@miga.cc`

### 数据库配置

所有数据库自动创建，无需配置。

### 日志配置

日志文件位置: `/app/work/logs/bypass/app.log`

---

## 💡 最佳实践

### 1. 数据驱动决策
- 依赖系统生成的数据分析
- 基于市场数据设定目标
- 避免凭感觉调整目标

### 2. 持续优化
- 定期查看月度报告
- 分析目标达成情况
- 根据系统建议调整目标

### 3. 及时响应
- 每日查看总结邮件
- 及时处理客户回复
- 快速跟进意向客户

### 4. 数据质量
- 确保每日执行记录完整
- 及时更新CRM系统
- 保持数据准确性

---

## 📞 技术支持

如有问题或需要帮助，请联系：
- **邮箱**: info@miga.cc
- **官网**: https://miga.cc

---

## 📝 更新日志

### v2.0.0 (2026-03-22)
- ✅ 新增市场研究模块
- ✅ 新增目标设定模块
- ✅ 新增每日计划模块
- ✅ 新增报告生成模块
- ✅ 新增邮件发送模块
- ✅ 新增目标调整模块
- ✅ 新增工作流编排器
- ✅ 实现数据驱动的目标设定
- ✅ 实现自动化的报告发送
- ✅ 实现智能的目标调整

---

**MIGA 数据驱动外贸客户开发系统 - 让数据驱动决策！** 🚀
