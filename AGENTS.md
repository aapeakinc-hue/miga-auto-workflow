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

## 📊 数据驱动系统（新增）

### 系统概述
基于海关数据、市场规模和大数据的外贸客户开发自动化系统，实现智能目标设定、每日工作计划、自动化报告生成和目标持续调整。

### 核心模块
| 模块名 | 文件位置 | 功能描述 |
|-------|---------|---------|
| 市场研究 | `market_research.py` | 海关数据分析、市场规模评估、竞争格局分析 |
| 目标设定 | `goal_setting.py` | 年度/月度目标设定、目标分解、达成追踪 |
| 每日计划 | `daily_planner.py` | 每日工作计划、执行记录、次日计划 |
| 报告生成 | `report_generator.py` | 日/周/月/年度报告生成 |
| 邮件发送 | `summary_sender.py` | 报告邮件发送到 info@miga.cc |
| 目标调整 | `goal_adjuster.py` | 基于达成度的目标智能调整 |
| 工作流编排 | `workflow_orchestrator.py` | 整合所有模块，自动化执行 |

### 功能特性
- ✅ **数据驱动目标设定** - 基于海关数据和市场规模自动生成目标
- ✅ **每日自动化计划** - 自动生成每日工作计划和次日计划
- ✅ **多维度报告** - 日、周、月、年度总结报告
- ✅ **邮件自动发送** - 所有报告自动发送到 info@miga.cc
- ✅ **智能目标调整** - 基于达成率自动调整下月目标
- ✅ **绩效追踪** - 实时追踪各项指标达成情况

### 使用方法
```bash
# 初始化系统
python main_data_driven.py --init

# 运行每日工作流
python main_data_driven.py --daily

# 运行周度工作流
python main_data_driven.py --weekly

# 运行月度工作流
python main_data_driven.py --monthly

# 运行年度工作流
python main_data_driven.py --annual

# 运行完整工作流
python main_data_driven.py --full

# 查看系统状态
python main_data_driven.py --status
```

### 目标设定流程
```
市场数据收集（海关数据、市场规模）
    ↓
市场潜力分析
    ↓
市场规模估算
    ↓
目标市场份额设定
    ↓
年度目标生成
    ↓
月度目标分解（考虑季节性）
    ↓
每日任务分配
```

### 目标调整机制
- **调整触发**: 每月月末自动触发
- **调整依据**: 月度目标达成率
  - 达成率 > 120%: 提高 15%
  - 达成率 80%-100%: 保持不变
  - 达成率 60%-80%: 降低 10%
  - 达成率 < 60%: 降低 20%
- **调整对象**: 下月目标
- **调整通知**: 自动发送到 info@miga.cc

### 报告发送时间
- **每日报告**: 每天 22:00
- **周度报告**: 每周日 22:00
- **月度报告**: 每月最后一天 22:00
- **年度报告**: 每年12月31日 22:00
- **目标调整通知**: 月末（需要调整时）

### 数据库文件
- `market_data.db` - 市场数据（海关数据、市场规模、竞争对手）
- `goals.db` - 目标数据（年度目标、月度目标、达成记录、调整记录）
- `daily_planner.db` - 每日计划（每日计划、执行记录、次日计划）
- `miga_crm.db` - CRM数据（客户、互动、订单）

### 文档
- `DATA_DRIVEN_SYSTEM_README.md` - 数据驱动系统详细文档

### 目标示例（2026年美国市场）
- **年度目标**:
  - 客户开发: 500个
  - 意向客户: 50个
  - 成交客户: 10个
  - 收入目标: $20,000

- **月度目标**（基于季节性权重调整）:
  - 1月: 40个（权重8%）
  - 10月: 50个（权重10% - 旺季）
  - 11月: 55个（权重11% - 旺季高峰）

---

## ☁️ 云端部署系统（新增）

### 系统概述
将整个外贸客户开发系统部署到云服务器，实现7x24小时全自动运行，无需人工干预。

### 部署目标
- ✅ 每日自动执行市场研究、客户开发、邮件发送
- ✅ 自动生成并发送日报、周报、月报、年报
- ✅ 基于数据自动调整月度目标
- ✅ 系统全自动运行，稳定可靠

### 部署文档
- **CLOUD_DEPLOYMENT_GUIDE.md** - 完整部署指南（包含详细步骤、故障排查、安全建议）
- **QUICK_START_CLOUD.md** - 5分钟快速开始（适合新手）
- **CLOUD_DEPLOYMENT_README.md** - 部署文档包说明

### 部署工具脚本
- **deploy_on_server.sh** - 一键部署脚本
  - 自动安装系统依赖
  - 创建Python虚拟环境
  - 安装所有Python包
  - 生成配置文件模板
  - 创建备份脚本
  - 生成定时任务模板

- **system_status.sh** - 系统状态监控脚本
  - 检查系统基本信息
  - 检查Python环境
  - 检查数据库文件
  - 检查定时任务
  - 检查最近日志
  - 检查系统资源
  - 检查网络连接

### 服务器要求
- **操作系统**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **配置建议**: 2核4GB、40GB硬盘、1Mbps网络
- **推荐云服务商**: 腾讯云、阿里云、华为云、AWS、DigitalOcean

### 部署后的目录结构
```
/opt/miga-crm/
├── venv/                    # Python虚拟环境
├── data/                    # 数据库文件
│   ├── market_data.db
│   ├── goals.db
│   ├── daily_planner.db
│   └── miga_crm.db
├── logs/                    # 日志文件
│   ├── daily_workflow.log
│   ├── weekly_report.log
│   ├── monthly_adjustment.log
│   └── backup.log
├── reports/                 # 报告文件
├── backups/                 # 数据备份
├── assets/                  # 资源文件
├── main_data_driven.py      # 主程序
├── .env                     # 环境变量配置
├── backup.sh                # 备份脚本
└── deploy_on_server.sh      # 部署脚本
```

### 定时任务配置
```bash
# 每天早上8:00执行每日工作流
0 8 * * * cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily

# 每月1号凌晨1:00调整目标
0 1 1 * * cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --adjust_goals

# 每周日凌晨2:00生成周报
0 2 * * 0 cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --weekly

# 每天凌晨4:00备份数据
0 4 * * * /opt/miga-crm/backup.sh

# 每天凌晨3:00清理7天前的日志
0 3 * * * find /opt/miga-crm/logs -name "*.log" -mtime +7 -delete
```

### 监控和维护
```bash
# 查看系统状态
bash /opt/miga-crm/system_status.sh

# 查看实时日志
tail -f /opt/miga-crm/logs/daily_workflow.log

# 查看定时任务
crontab -l

# 手动执行每日工作流
cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily

# 手动备份数据
bash /opt/miga-crm/backup.sh
```

### 部署检查清单
- [ ] 云服务器已购买并可以SSH连接
- [ ] Python 3.8+ 已安装
- [ ] 项目文件已上传到 `/opt/miga-crm/`
- [ ] 虚拟环境已创建
- [ ] 所有依赖包已安装
- [ ] 环境变量文件 `.env` 已配置
- [ ] 系统初始化成功（4个数据库文件已创建）
- [ ] 定时任务已配置（crontab -l 可见）
- [ ] 手动执行每日工作流成功
- [ ] 测试邮件成功发送到 info@miga.cc
- [ ] 日志目录有正常输出

### 部署优势
1. **7x24小时运行**: 云服务器24小时在线，无需人工干预
2. **自动化执行**: 每日工作流、周报、月报全自动生成
3. **数据安全**: 定期自动备份，数据永不丢失
4. **稳定可靠**: 专业云服务商，99.9%可用性
5. **扩展性强**: 可根据业务需求随时升级配置
6. **远程管理**: 随时随地通过SSH管理

### 常见问题解决

#### 问题1: 定时任务没有执行
```bash
# 检查Cron服务状态
service cron status

# 查看Cron日志
sudo grep CRON /var/log/syslog | tail -20

# 手动测试命令
cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily
```

#### 问题2: 邮件发送失败
```bash
# 检查环境变量配置
cat /opt/miga-crm/.env

# 查看错误日志
tail -n 50 /opt/miga-crm/logs/daily_workflow.log
```

#### 问题3: 数据库文件损坏
```bash
# 使用备份恢复
cp /opt/miga-crm/backups/backup_xxx/data/*.db /opt/miga-crm/data/

# 或重新初始化
cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --init
```

### 快速部署步骤
1. 购买云服务器（推荐：腾讯云、阿里云、华为云）
2. SSH连接到服务器
3. 上传项目文件到 `/opt/miga-crm/`
4. 运行部署脚本：`sudo bash deploy_on_server.sh`
5. 配置环境变量：`nano /opt/miga-crm/.env`
6. 初始化系统：`python main_data_driven.py --init`
7. 测试运行：`python main_data_driven.py --daily`
8. 配置定时任务：`crontab -e`
9. 完成！

### 部署完成标志
当以下条件全部满足时，说明部署成功：
1. ✅ 可以SSH连接到服务器
2. ✅ 项目文件在 `/opt/miga-crm/` 目录
3. ✅ 运行 `bash system_status.sh` 显示全部绿色 ✅
4. ✅ 定时任务已配置（crontab -l 可见）
5. ✅ 手动执行工作流成功
6. ✅ 测试邮件成功发送
7. ✅ 次日早上8:00自动执行并收到邮件

### 相关文档
- 详细部署指南: [CLOUD_DEPLOYMENT_GUIDE.md](./CLOUD_DEPLOYMENT_GUIDE.md)
- 快速开始指南: [QUICK_START_CLOUD.md](./QUICK_START_CLOUD.md)
- 部署文档包说明: [CLOUD_DEPLOYMENT_README.md](./CLOUD_DEPLOYMENT_README.md)
