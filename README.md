# 🚀 MIGA 外贸客户开发系统

## 📋 项目简介

本项目构建了一个完整的**外贸客户开发自动化系统**，实现了从产品信息抓取、客户搜索、邮箱获取、邮件生成到发送的全流程自动化，并配套建立了专业的CRM管理系统，实现科学化客户管理和精细化运营。

### 核心功能
- ✅ 自动化客户开发工作流
- ✅ 智能客户搜索与过滤
- ✅ 个性化邮件生成
- ✅ 批量邮件发送
- ✅ CRM 客户管理系统
- ✅ 自动跟进提醒
- ✅ 数据分析报表

---

## 🎯 产品信息

- **品牌**: MIGA Team
- **官网**: https://miga.cc
- **产品网站**: https://products.miga.cc
- **发件邮箱**: info@miga.cc
- **主营产品**: 水晶烛台、水晶工艺品

---

## 🏗️ 项目结构

```
├── src/                           # 源代码
│   ├── graphs/                    # 工作流编排
│   │   ├── state.py              # 状态定义
│   │   ├── graph.py              # 主图编排
│   │   └── nodes/                # 节点实现
│   │       ├── product_fetch_node.py
│   │       ├── customer_search_node.py
│   │       ├── email_fetch_node.py
│   │       ├── email_generate_node.py
│   │       └── email_send_node.py
│   ├── tools/                     # 工具定义
│   │   └── email_fetch_tool.py
│   ├── agents/                    # Agent 代码
│   ├── storage/                   # 存储
│   ├── tests/                     # 测试
│   └── main.py                    # 运行入口
├── config/                        # 配置文件
│   └── email_generate_llm_cfg.json
├── scripts/                       # 脚本
├── assets/                        # 资源文件
├── docs/                          # 文档
│
├── crm_system.py                 # CRM 核心系统
├── crm_tools.py                  # CRM 工具集
├── import_workflow_results.py    # 工作流集成
│
├── AGENTS.md                     # 工作流详细文档
├── CRM_README.md                # CRM 使用指南
├── ANNUAL_PLAN.md               # 年度开发计划
├── client_development_report.md # 客户开发报告
├── QUICK_REFERENCE.md           # 快速参考指南
├── PROJECT_SUMMARY.md           # 项目总结
│
└── README.md                    # 本文件
```

---

## 🚀 快速开始

### 1. 运行工作流

```bash
# 运行完整工作流
bash scripts/local_run.sh -m flow

# 运行单个节点
bash scripts/local_run.sh -m node -n node_name

# 启动 HTTP 服务
bash scripts/http_run.sh -m http -p 5000
```

### 2. 初始化 CRM 系统

```bash
# 创建 CRM 数据库
python crm_system.py

# 导入工作流结果
python import_workflow_results.py

# 使用 CRM 工具
python crm_tools.py
```

### 3. 查看文档

- **[AGENTS.md](AGENTS.md)** - 工作流详细文档
- **[CRM_README.md](CRM_README.md)** - CRM 使用指南
- **[ANNUAL_PLAN.md](ANNUAL_PLAN.md)** - 年度开发计划
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 快速参考指南
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目总结

---

## 🔧 配置说明

### API 配置

#### Snov.io API
- **API Token**: `fbf98546081c2793e21d6de6540ce2ca`
- **Client ID**: `746628993ee9eda28e455e53751030bd`

#### Resend API
- **API Key**: `re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F`
- **发件邮箱**: `info@miga.cc`
- **域名状态**: ✅ 已验证

### 域名配置
- **产品网站**: https://products.miga.cc
- **配置方式**: Cloudflare Pages + 阿里云 DNS

---

## 📊 工作流节点

| 节点 | 功能 | 类型 | 状态 |
|------|------|------|------|
| `product_fetch` | 产品信息抓取 | task | ✅ 完成 |
| `customer_search` | 客户搜索（智能过滤） | task | ✅ 完成 |
| `email_fetch` | 邮箱获取（snov.io API） | task | ✅ 完成 |
| `email_generate` | 邮件生成（大模型） | agent | ✅ 完成 |
| `email_send` | 邮件发送（resend API） | task | ✅ 完成 |

---

## 💼 CRM 客户分类

| 分类 | 定义 | 跟进频率 | 管理策略 |
|------|------|----------|----------|
| **A 类** | 已成交，单笔订单>$10,000 | 每周1次 | 专属客户经理，优先发货 |
| **B 类** | 已回复，有意向 | 每3天1次 | 主动跟进，提供产品目录 |
| **C 类** | 已发送邮件，未回复 | 每2周1次 | 定期发送产品更新 |
| **D 类** | 邮箱无效、明确拒绝 | 不跟进 | 标记为无效，定期清理 |

---

## 📈 测试结果

### 首轮开发成果（美国市场）
- **开发领域**: 5个细分领域
- **发送邮件**: 25封
- **成功发送**: 19封（76%成功率）
- **完成时间**: 2026年3月22日

### 已验证功能
- ✅ 产品信息抓取（products.miga.cc）
- ✅ 客户搜索（智能过滤B2B平台）
- ✅ 邮箱获取（snov.io API）
- ✅ 邮件生成（大模型个性化）
- ✅ 邮件发送（resend API）

---

## 🎯 年度计划

### Q2 2026（4-6月）：建立客户数据库
- 🌍 北美市场（美国、加拿大）
- 🎯 500+潜在客户

### Q3 2026（7-9月）：快速扩张
- 🌍 欧洲市场（英国、德国、法国）
- 🎯 100+意向客户，10+成交客户

### Q4 2026（10-12月）：旺季冲刺
- 🌍 中东市场（阿联酋、沙特）
- 🎯 200+意向客户，50+成交客户

### Q1 2027（1-3月）：亚太市场
- 🌍 亚太市场（日本、韩国、澳大利亚）
- 🎯 100+意向客户，20+成交客户

---

## 🔑 快速参考

### 常用命令

```bash
# 初始化 CRM
python crm_system.py

# 导入工作流结果
python import_workflow_results.py

# 使用 CRM 工具
python crm_tools.py

# 查询 CRM 数据
python -c "from crm_system import CRMDatabase; crm = CRMDatabase('miga_crm.db'); print(crm.get_all_customers())"
```

### 关键指标
- 邮件发送成功率: 76%+
- 客户回复率: 待统计
- 意向客户转化率: 待统计
- 成交转化率: 待统计

---

## 📞 联系方式

- **品牌**: MIGA Team
- **邮箱**: info@miga.cc
- **官网**: https://miga.cc

---

## 📚 技术栈

- **工作流**: LangGraph 1.0
- **语言**: Python 3.8+
- **数据库**: SQLite
- **大模型**: LLM（邮件生成）
- **API**: snov.io, resend

---

## 🎊 项目总结

本项目成功构建了一个完整的**外贸客户开发自动化系统**，实现了从客户开发到科学化管理的全流程闭环，大幅提升客户开发效率和质量。

**核心价值**:
- ✅ 效率提升：工作流自动化，节省90%人工时间
- ✅ 质量提升：智能过滤，精准定位潜在客户
- ✅ 转化提升：个性化邮件，提升回复率和成交率
- ✅ 管理提升：CRM系统，科学化客户管理

---

**MIGA 外贸客户开发系统 - 让外贸更简单！** 🚀

