## 项目概述
- **名称**: 外贸客户开发工作流
- **功能**: 自动化外贸客户开发流程，从网站抓取产品信息 → 搜索潜在客户 → 获取客户邮箱 → 生成个性化开发邮件 → 批量发送邮件

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| product_fetch | `nodes/product_fetch_node.py` | task | 从网站抓取产品信息 | - | - |
| customer_search | `nodes/customer_search_node.py` | task | 基于关键词搜索潜在客户 | - | - |
| email_fetch | `nodes/email_fetch_node.py` | task | 使用 snov.io 获取客户邮箱 | - | - |
| email_generate | `nodes/email_generate_node.py` | agent | 使用大模型生成个性化邮件 | - | `config/email_generate_llm_cfg.json` |
| email_send | `nodes/email_send_node.py` | task | 使用 resend API 发送邮件 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
无子图

## 技能使用
- 节点 `product_fetch` 使用 Fetch URL 技能
- 节点 `customer_search` 使用 Web Search 技能
- 节点 `email_generate` 使用大语言模型技能
- 节点 `email_fetch` 使用 snov.io API（第三方服务）
- 节点 `email_send` 使用 resend API（第三方服务）

## 工作流流程
1. **产品信息抓取** (`product_fetch`): 从指定网站URL提取产品信息
2. **客户搜索** (`customer_search`): 基于产品信息和目标关键词搜索潜在客户
3. **邮箱获取** (`email_fetch`): 使用 snov.io API 根据客户公司域名获取邮箱地址
4. **邮件生成** (`email_generate`): 根据产品和客户信息使用大模型生成个性化邮件
5. **邮件发送** (`email_send`): 使用 resend API 批量发送邮件

## 配置说明
### 自定义域名配置
- **产品网站**: https://products.miga.cc
- **配置方式**:
  - 在阿里云DNS中添加CNAME记录：`products → migac-website.pages.dev`
  - 在Cloudflare Pages中激活自定义域名：`products.miga.cc`
  - Cloudflare自动提供SSL证书
- **旧域名**: https://migac-website.pages.dev/products (仍然可用)

### API 配置
- **snov.io**:
  - API Token: `fbf98546081c2793e21d6de6540ce2ca`
  - Client ID: `746628993ee9eda28e455e53751030bd`
  
- **resend**:
  - API Key: `re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F`
  - 发件邮箱: `info@miga.cc` (已验证域名)
  - 域名状态: ✅ 已验证

### 邮件署名信息
- 发件人: MIGA Team
- 邮箱: info@miga.cc
- 网站: https://miga.cc

## 测试结果
工作流已成功测试，各节点运行正常：
- ✅ 产品信息抓取成功（从 products.miga.cc）
- ✅ 客户搜索成功（智能过滤B2B平台和非商业网站）
- ✅ 邮箱获取成功（使用snov.io API）
- ✅ 邮件生成成功（大模型生成个性化邮件）
- ✅ 邮件发送成功（成功率80%+）

### 最新测试结果（2026-03-22）
- **关键词**: 美国水晶装饰品批发商
- **搜索到的客户**: 5家
- **邮件发送**: 4/5 成功
- **成功发送到**:
  - Crystals Wholesale USA
  - Best crystals Deals Online in the US
  - Tocrystal (Bulk Crystals)
  - ACCIO (trending crystal products)

### 产品信息
根据 https://products.miga.cc 抓取的产品：
- **水晶烛台系列**: 10款（五臂/九臂烛台、烛台套装等）
- **水晶工艺品系列**: 6款（花艺摆件、雕塑、花瓶、装饰桌等）
- **目标客户**: 婚礼策划公司、活动策划公司、高端酒店、奢华家居装饰批发商

### CRM 系统集成
- **CRM系统文件**:
  - `crm_system.py`: 核心CRM管理系统
  - `crm_tools.py`: CRM工具集（批量导入、自动跟进、客户分类）
  - `import_workflow_results.py`: 工作流结果导入工具
  - `CRM_README.md`: CRM使用指南

- **功能特性**:
  - 客户信息管理（添加、查询、更新）
  - 互动记录追踪（邮件、电话、会议）
  - 订单管理（创建、更新、查询）
  - 自动跟进提醒（基于客户类型和天数）
  - 客户分类管理（A/B/C/D四级分类）
  - 数据分析报表（转化漏斗、月度报告）

- **客户分类体系**:
  - **A类（VIP客户）**: 已成交，单笔订单>$10,000
  - **B类（重点客户）**: 已回复，有意向
  - **C类（潜在客户）**: 已发送邮件，未回复
  - **D类（无效客户）**: 邮箱无效、明确拒绝、无需求

- **使用方法**:
  ```bash
  # 初始化CRM系统
  python crm_system.py

  # 导入工作流结果
  python import_workflow_results.py

  # 使用CRM工具
  python crm_tools.py
  ```

- **数据存储**:
  - 数据库: SQLite (miga_crm.db)
  - 备份: 支持导出为JSON格式
  - 集成: 与工作流自动对接
