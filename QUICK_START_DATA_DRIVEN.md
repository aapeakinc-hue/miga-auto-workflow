# 🚀 快速开始指南 - MIGA 数据驱动外贸客户开发系统

## 📋 前置要求

- Python 3.8+
- pip 或 uv 包管理器
- 网络连接（访问外部API）

## 🎯 5分钟快速部署

### 步骤1: 安装依赖

```bash
pip install langgraph langchain requests pydantic jinja2
```

### 步骤2: 初始化系统

```bash
python main_data_driven.py --init
```

这将自动完成：
- ✅ 创建所有数据库
- ✅ 导入示例市场数据
- ✅ 初始化示例目标
- ✅ 创建示例每日计划

### 步骤3: 运行每日工作流

```bash
python main_data_driven.py --daily
```

这将自动完成：
- ✅ 执行客户搜索工作流
- ✅ 发送开发邮件
- ✅ 生成每日总结
- ✅ 发送报告到 info@miga.cc
- ✅ 创建次日计划

### 步骤4: 查看结果

检查你的邮箱 `info@miga.cc`，你将收到：
- 📊 每日工作总结报告
- 📋 今日关键指标
- 🎯 亮点和问题
- 📧 次日计划

---

## 📚 核心概念

### 1. 数据驱动目标设定

系统基于以下数据源设定目标：
- 📊 海关数据 - 各国水晶产品进口数据
- 📈 市场规模 - 各国水晶产品市场规模
- 🏆 竞争格局 - 主要竞争对手信息

### 2. 每日自动化流程

```
每日计划（自动生成）
    ↓
执行任务（自动 + 人工）
    ↓
记录结果（自动记录）
    ↓
生成总结（自动生成）
    ↓
发送邮件（自动发送）
    ↓
次日计划（自动创建）
```

### 3. 目标智能调整

系统在月末自动分析绩效，根据达成率调整下月目标：
- 超额完成（>120%）：提高15%
- 基本达成（80-100%）：保持不变
- 未达标（60-80%）：降低10%
- 严重未达标（<60%）：降低20%

---

## 🎓 常用命令

### 系统管理

```bash
# 初始化系统
python main_data_driven.py --init

# 查看系统状态
python main_data_driven.py --status
```

### 工作流执行

```bash
# 每日工作流
python main_data_driven.py --daily

# 周度工作流
python main_data_driven.py --weekly

# 月度工作流
python main_data_driven.py --monthly

# 年度工作流
python main_data_driven.py --annual

# 完整工作流（执行所有适用的）
python main_data_driven.py --full
```

### 高级选项

```bash
# 指定日期和市场
python main_data_driven.py --daily --date 2026-03-22 --market UK

# 指定年份和月份
python main_data_driven.py --monthly --year 2026 --month 3

# 指定市场（所有工作流支持）
python main_data_driven.py --daily --market Germany
```

---

## ⏰ 定时任务设置

### Linux/macOS (cron)

```bash
# 编辑 crontab
crontab -e

# 添加以下任务
# 每天晚上10点执行每日工作流
0 22 * * * cd /path/to/project && python main_data_driven.py --daily >> /app/work/logs/bypass/app.log 2>&1

# 每周日晚10点执行周度工作流
0 22 * * 0 cd /path/to/project && python main_data_driven.py --weekly >> /app/work/logs/bypass/app.log 2>&1

# 每月最后一天晚10点执行月度工作流
0 22 28-31 * * cd /path/to/project && python main_data_driven.py --monthly >> /app/work/logs/bypass/app.log 2>&1
```

### Windows (Task Scheduler)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天、每周、每月）
4. 设置操作（运行程序）
5. 程序: `python`
6. 参数: `main_data_driven.py --daily`
7. 起始于: 项目目录路径

---

## 📊 理解数据

### 市场数据示例

```python
from market_research import MarketResearch

market = MarketResearch()

# 生成市场分析报告
report = market.generate_market_report("USA")

print(f"市场潜力: {report['market_potential']['potential']}")
print(f"市场增长率: {report['growth_rate']}%")
print(f"预估市场规模: ${report['estimated_market_size']:,.0f}")
```

### 目标数据示例

```python
from goal_setting import GoalSetting

goal_system = GoalSetting()

# 获取年度目标
annual_goal = goal_system.get_annual_goal(2026, "USA")

print(f"客户开发目标: {annual_goal['customer_development_goal']}")
print(f"意向客户目标: {annual_goal['intention_customer_goal']}")
print(f"成交客户目标: {annual_goal['deal_customer_goal']}")
print(f"收入目标: ${annual_goal['revenue_goal']:,.0f}")
```

### 每日数据示例

```python
from daily_planner import DailyPlanner

planner = DailyPlanner()
today = date.today()

# 获取每日计划
daily_plan = planner.get_daily_plan(today, "USA")

print(f"今日任务数: {len(daily_plan['tasks'])}")
for task in daily_plan['tasks']:
    print(f"  - {task['description']}")
```

---

## 🎯 工作流程示例

### 完整的一天

```bash
# 早上9点 - 开始工作
# 1. 查看今日计划
python main_data_driven.py --status

# 2. 执行客户开发工作流
bash scripts/local_run.sh -m flow

# 3. 检查邮箱回复并跟进
# （人工操作）

# 中午12点 - 午休

# 下午2点 - 继续工作
# 1. 更新CRM系统
python import_workflow_results.py

# 2. 跟进意向客户
# （人工操作）

# 晚上9点 - 准备收工
# 1. 记录今日完成情况
# （系统自动记录）

# 晚上10点 - 系统自动执行
# （cron定时任务自动执行）
python main_data_driven.py --daily

# 晚上10:30 - 查看每日总结
# （检查 info@miga.cc 邮箱）
```

### 完整的一周

```bash
# 周一至周六
# 每天执行每日工作流
python main_data_driven.py --daily

# 周日
# 执行周度工作流（自动包含每日工作流）
python main_data_driven.py --weekly
```

### 完整的一月

```bash
# 每天执行每日工作流
python main_data_driven.py --daily

# 每周执行周度工作流
python main_data_driven.py --weekly

# 月末执行月度工作流
python main_data_driven.py --monthly
```

---

## 💡 实用技巧

### 1. 快速检查系统状态

```bash
python main_data_driven.py --status
```

### 2. 重新生成今日计划

```bash
# 删除今日计划数据后重新初始化
python main_data_driven.py --init
```

### 3. 查看日志

```bash
# 查看最新日志
tail -n 50 /app/work/logs/bypass/app.log

# 搜索错误
grep -n "Error\|Exception" /app/work/logs/bypass/app.log
```

### 4. 备份数据

```bash
# 备份所有数据库
cp *.db backup_$(date +%Y%m%d).tar.gz
```

---

## 🔧 故障排查

### 问题1: 数据库不存在

**症状**: 提示找不到数据库文件

**解决**:
```bash
python main_data_driven.py --init
```

### 问题2: 邮件发送失败

**症状**: 邮件未发送到 info@miga.cc

**解决**:
1. 检查 API Key 配置
2. 检查网络连接
3. 查看日志: `tail -n 20 /app/work/logs/bypass/app.log`

### 问题3: 目标未生成

**症状**: 查看状态时没有目标数据

**解决**:
```bash
# 重新初始化系统
python main_data_driven.py --init
```

### 问题4: 报告格式错误

**症状**: 邮件内容显示异常

**解决**:
1. 检查数据库数据完整性
2. 查看日志获取详细错误信息

---

## 📞 获取帮助

### 查看帮助信息

```bash
python main_data_driven.py --help
```

### 查看详细文档

- 📖 [数据驱动系统文档](DATA_DRIVEN_SYSTEM_README.md)
- 📖 [工作流文档](AGENTS.md)
- 📖 [CRM使用指南](CRM_README.md)
- 📖 [快速参考](QUICK_REFERENCE.md)

### 技术支持

- **邮箱**: info@miga.cc
- **官网**: https://miga.cc

---

## 🎊 你已经准备好了！

现在你可以：

1. ✅ 初始化系统: `python main_data_driven.py --init`
2. ✅ 运行每日工作流: `python main_data_driven.py --daily`
3. ✅ 查看系统状态: `python main_data_driven.py --status`
4. ✅ 接收报告邮件: 查看 info@miga.cc
5. ✅ 跟进客户回复: 在 CRM 系统中管理

**开始你的数据驱动外贸客户开发之旅吧！** 🚀
