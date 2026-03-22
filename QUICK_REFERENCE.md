# 🚀 MIGA 外贸客户开发 - 快速参考指南

## 📋 项目信息

**项目名称**: 外贸客户开发自动化工作流
**品牌信息**: MIGA Team
**官网**: https://miga.cc
**产品网站**: https://products.miga.cc
**发件邮箱**: info@miga.cc

---

## 🛠️ 常用命令

### 工作流相关

#### 1. 运行完整工作流
```bash
# 使用 test_run 工具测试工作流
# 在项目根目录执行

# 构建和运行
python src/main.py
```

#### 2. 查看工作流状态
```bash
# 查看项目结构
ls -la

# 查看节点文件
ls -la src/graphs/nodes/

# 查看配置文件
ls -la config/
```

### CRM 系统相关

#### 1. 初始化 CRM 系统
```bash
python crm_system.py
```
输出:
- ✅ 数据库初始化完成
- ✅ 创建了所有必要的表

#### 2. 导入工作流结果到 CRM
```bash
python import_workflow_results.py
```
输出:
- 📊 批次导入统计
- ✅ 成功导入客户数量
- 📈 CRM 当前统计

#### 3. 使用 CRM 工具
```bash
python crm_tools.py
```
输出:
- 📅 自动跟进提醒（未来7天）
- 📊 客户分类摘要
- 📧 邮件模板预览

#### 4. 查询 CRM 数据
```python
from crm_system import CRMDatabase

crm = CRMDatabase("miga_crm.db")

# 查询所有客户
customers = crm.get_all_customers()

# 查询待跟进客户
pending = crm.get_pending_followups(7)

# 获取统计数据
stats = crm.get_statistics()
```

---

## 🎯 工作流核心节点

### 1. 产品信息抓取
- **节点名**: `product_fetch`
- **功能**: 从网站抓取产品信息
- **输入**: 产品URL
- **输出**: 产品名称、描述、图片等

### 2. 客户搜索
- **节点名**: `customer_search`
- **功能**: 基于关键词搜索潜在客户
- **输入**: 产品信息、搜索关键词
- **输出**: 客户列表（公司名、网站）

### 3. 邮箱获取
- **节点名**: `email_fetch`
- **功能**: 使用 snov.io API 获取客户邮箱
- **输入**: 客户网站/域名
- **输出**: 邮箱地址列表

### 4. 邮件生成
- **节点名**: `email_generate`
- **功能**: 使用大模型生成个性化邮件
- **输入**: 产品信息、客户信息
- **输出**: 个性化邮件内容

### 5. 邮件发送
- **节点名**: `email_send`
- **功能**: 使用 resend API 批量发送邮件
- **输入**: 邮件内容、客户邮箱列表
- **输出**: 发送结果（成功/失败统计）

---

## 🔑 API 配置

### Snov.io API
- **API Token**: `fbf98546081c2793e21d6de6540ce2ca`
- **Client ID**: `746628993ee9eda28e455e53751030bd`
- **功能**: 根据域名获取邮箱地址

### Resend API
- **API Key**: `re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F`
- **发件邮箱**: `info@miga.cc`
- **域名状态**: ✅ 已验证
- **功能**: 批量发送邮件

---

## 📊 CRM 客户分类

### A 类客户（VIP）
- **定义**: 已成交，单笔订单 > $10,000
- **跟进频率**: 每周1次
- **管理策略**:
  - 专属客户经理
  - 优先发货
  - 专属折扣
  - 定期回访

### B 类客户（重点）
- **定义**: 已回复，有意向
- **跟进频率**: 每3天1次
- **管理策略**:
  - 主动跟进
  - 提供产品目录
  - 寄送样品
  - 有限折扣（10%）

### C 类客户（潜在）
- **定义**: 已发送邮件，未回复
- **跟进频率**: 每2周1次
- **管理策略**:
  - 定期发送产品更新
  - 节日问候
  - 自动化邮件序列

### D 类客户（无效）
- **定义**: 邮箱无效、明确拒绝、无需求
- **跟进频率**: 不跟进
- **管理策略**: 标记为无效，定期清理

---

## 📅 年度开发计划

### Q2 2026（4-6月）：建立客户数据库
- **目标**: 建立500+潜在客户数据库
- **市场**: 北美市场（美国、加拿大）
- **重点**: 收集客户信息，建立CRM系统

### Q3 2026（7-9月）：快速扩张
- **目标**: 获取100+意向客户，转化10+成交客户
- **市场**: 欧洲市场（英国、德国、法国）
- **重点**: 优化邮件模板，提升转化率

### Q4 2026（10-12月）：旺季冲刺
- **目标**: 获取200+意向客户，转化50+成交客户
- **市场**: 中东市场（阿联酋、沙特）
- **重点**: 旺季促销，提升订单量

### Q1 2027（1-3月）：亚太市场
- **目标**: 获取100+意向客户，转化20+成交客户
- **市场**: 亚太市场（日本、韩国、澳大利亚）
- **重点**: 新市场开拓

---

## 📧 邮件发送最佳实践

### 1. 邮件主题优化
- ✅ 使用简洁明了的主题
- ✅ 包含客户公司名称
- ✅ 突出产品优势

### 2. 邮件内容优化
- ✅ 个性化开头（提及客户公司）
- ✅ 清晰的产品介绍
- ✅ 明确的Call to Action
- ✅ 专业的署名信息

### 3. 发送时间优化
- ✅ 工作日早上9-11点
- ✅ 避免周末和节假日
- ✅ 考虑客户时区

### 4. 跟进策略
- ✅ 3天后第一次跟进
- ✅ 7天后第二次跟进
- ✅ 14天后第三次跟进

---

## 🔍 搜索关键词推荐

### 美国市场
- "wholesale crystal candle holders USA"
- "crystal decor distributors"
- "wedding supplies wholesale"
- "luxury home decor importers"
- "event planners crystal decor"

### 欧洲市场
- "crystal candle holders wholesale UK"
- "wedding decorations Germany"
- "crystal decor importers France"
- "luxury home decor distributors"

### 中东市场
- "crystal candle holders Dubai"
- "wedding supplies wholesale UAE"
- "luxury home decor Saudi Arabia"
- "event planners crystal decor Middle East"

---

## 📞 常见问题

### Q1: 如何提高邮件发送成功率？
**A**:
1. 确保邮箱地址正确
2. 使用已验证的发件域名
3. 避免被标记为垃圾邮件
4. 定期检查邮件发送质量

### Q2: 如何提升客户回复率？
**A**:
1. 个性化邮件内容
2. 清晰的价值主张
3. 明确的Call to Action
4. 专业的邮件格式

### Q3: 如何管理大量客户数据？
**A**:
1. 使用CRM系统
2. 客户分类管理
3. 自动化跟进
4. 定期数据清理

### Q4: 如何处理无效客户？
**A**:
1. 标记为D类客户
2. 定期清理（6个月）
3. 分析失败原因
4. 优化筛选策略

---

## 📈 关键指标追踪

### 获客指标
- 每月开发客户数量
- 邮件发送成功率
- 邮件打开率
- 邮件回复率

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

## 📚 相关文档

- **AGENTS.md**: 工作流详细文档
- **CRM_README.md**: CRM系统使用指南
- **ANNUAL_PLAN.md**: 年度开发计划
- **client_development_report.md**: 客户开发报告

---

## 🆘 技术支持

如有问题或需要帮助，请联系：
- **邮箱**: info@miga.cc
- **网站**: https://miga.cc

---

**MIGA 外贸客户开发 - 让客户开发更高效！** 🚀
