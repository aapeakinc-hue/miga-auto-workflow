# 外贸客户开发自动化工作流

> 🚀 **自动化外贸客户开发系统** - 每天自动搜索潜在客户、发送开发邮件，无需人工干预

---

## 🎯 项目简介

这是一个完整的外贸客户开发自动化系统，实现从产品信息获取、客户搜索、邮箱获取、邮件生成到发送的全流程自动化。

### 核心功能

- ✅ **自动搜索潜在客户** - 基于关键词搜索全球客户
- ✅ **自动获取邮箱** - 使用 Snov.io API 获取客户邮箱
- ✅ **自动生成邮件** - 使用 AI 生成个性化开发邮件
- ✅ **自动发送邮件** - 使用 Resend API 发送邮件
- ✅ **自动记录历史** - 避免重复发送同一客户
- ✅ **自动生成报告** - 每日统计发送结果

---

## 🚀 快速开始

### 1️⃣ 配置 GitHub Actions 自动化（推荐）

**为什么选择 GitHub Actions？**

- ✅ 完全免费（每月 2000 分钟）
- ✅ 无需服务器
- ✅ 无需电脑开机
- ✅ 配置简单（5 分钟搞定）

**详细配置步骤**：查看 [SETUP_SUMMARY.md](SETUP_SUMMARY.md)

**快速配置**：
```bash
# 运行配置向导
python setup_github_actions.py

# 按照向导指引完成配置
```

---

### 2️⃣ 手动运行工作流

```bash
cd src
python auto_workflow.py
```

**输入示例**：
```json
{
  "target_keywords": "crystal candle holders wholesale USA",
  "website_url": "https://miga.cc"
}
```

---

## 📊 自动化方案对比

| 方案 | 成本 | 难度 | 可靠性 | 推荐度 |
|------|------|------|--------|--------|
| **GitHub Actions** | 免费 | 简单 | ⭐⭐⭐⭐⭐ | ✅✅✅ |
| Cloudflare Workers | 免费 | 中等 | ⭐⭐⭐⭐⭐ | ✅✅ |
| 本地 Cron | 免费 | 简单 | ⭐⭐⭐ | ❌ |
| 云服务器 | 付费 | 中等 | ⭐⭐⭐⭐⭐ | ✅ |

---

## 📁 项目结构

```
├── src/                          # 源代码
│   ├── graphs/                   # 工作流代码
│   │   ├── graph.py             # 主图编排
│   │   ├── state.py             # 状态定义
│   │   └── nodes/               # 节点实现
│   │       ├── product_fetch_node.py
│   │       ├── customer_search_node.py
│   │       ├── email_fetch_node.py
│   │       ├── email_generate_node.py
│   │       └── email_send_node.py
│   ├── auto_workflow.py         # 自动化脚本
│   └── test_single_customer.py  # 测试脚本
├── config/                       # 配置文件
│   ├── email_generate_llm_cfg.json
│   └── optimized_search_keywords.py
├── .github/workflows/            # GitHub Actions
│   └── auto-workflow.yml        # 自动化配置
├── cloudflare/                   # Cloudflare Workers（备选）
├── logs/                         # 日志文件
├── AGENTS.md                     # 项目索引
├── GITHUB_ACTIONS_GUIDE.md       # GitHub Actions 详细指南
├── SETUP_SUMMARY.md              # 快速配置总结
└── README.md                     # 本文件
```

---

## 🔑 API 密钥配置

### GitHub Secrets（GitHub Actions 方案）

在 GitHub 仓库 Settings → Secrets and variables → Actions 中配置：

- `SNOVIO_API_KEY` - Snov.io API Key
- `RESEND_API_KEY` - Resend API Key

### 本地环境变量

```bash
export SNOVIO_API_KEY="your-snovio-api-key"
export RESEND_API_KEY="your-resend-api-key"
```

---

## 📈 工作流程

```
1. 产品信息获取 (product_fetch)
   ↓
2. 客户搜索 (customer_search)
   ↓
3. 邮箱获取 (email_fetch)
   ↓
4. 邮件生成 (email_generate)
   ↓
5. 邮件发送 (email_send)
   ↓
完成
```

---

## 🎯 日常工作

### 自动化后

**每天 9 点自动完成**：
- 🔍 搜索 3-5 个潜在客户
- 📧 发送 3-5 封开发邮件
- 📊 记录发送历史
- 📋 生成每日报告

**你只需要**：
- 📧 检查邮箱回复（info@miga.cc）
- 💬 回复有兴趣的客户
- 📝 跟进潜在客户
- 💰 成交！

---

## 📚 文档

### 核心文档

- [AGENTS.md](AGENTS.md) - 项目索引和技术细节
- [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - GitHub Actions 快速配置
- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - GitHub Actions 详细指南

### 其他文档

- [cloudflare/DEPLOYMENT_GUIDE.md](cloudflare/DEPLOYMENT_GUIDE.md) - Cloudflare Workers 部署指南
- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) - 自动化配置指南

---

## 🛠️ 技术栈

- **Python 3.12** - 主要开发语言
- **LangGraph** - 工作流编排框架
- **Snov.io API** - 客户搜索和邮箱验证
- **Resend API** - 邮件发送和追踪
- **GitHub Actions** - 自动化定时任务
- **Cloudflare Workers** - 备选自动化方案

---

## 🧪 测试

### 测试单个客户

```bash
cd src
python test_single_customer.py
```

### 测试自动化流程

```bash
cd src
python auto_workflow.py
```

### 测试 GitHub Actions

在 GitHub 仓库 → Actions → Run workflow

---

## 📊 发送记录

### 查看本地发送记录

```bash
cat logs/sent_emails.json
```

### 查看每日报告

```bash
cat logs/daily_report_*.txt
```

### 查看 Resend 发送记录

访问 https://resend.com

---

## 🔧 常见问题

### Q: 如何修改运行时间？

**A**: 编辑 `.github/workflows/auto-workflow.yml` 中的 cron 表达式。

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # UTC 时间
```

### Q: Actions 运行失败怎么办？

**A**:
1. 查看 Actions 日志
2. 检查 GitHub Secrets 配置
3. 确认 API Keys 有效

### Q: 如何查看发送记录？

**A**:
1. 在 GitHub Actions 运行记录中下载日志附件
2. 查看 `logs/sent_emails.json`
3. 访问 Resend 控制台

### Q: 会收费吗？

**A**:
- GitHub Actions: 免费（每月 2000 分钟）
- Cloudflare Workers: 免费（每天 100,000 次请求）
- 本地 Cron: 免费

---

## 💡 优化建议

### 搜索关键词优化

1. 使用英文关键词提高搜索准确性
2. 针对目标市场定制关键词
3. 定期测试和优化关键词效果

### 邮件内容优化

1. 个性化邮件内容
2. 突出产品优势
3. 明确行动号召

### 客户筛选优化

1. 过滤无效网站（电商平台、B2B平台）
2. 过滤中文网站（针对海外市场）
3. 优先选择欧美客户

---

## 📞 支持

### 查看文档

- [AGENTS.md](AGENTS.md) - 项目索引和技术细节
- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - GitHub Actions 详细指南
- [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - 快速配置总结

### 外部资源

- LangGraph 文档: https://langchain-ai.github.io/langgraph/
- Snov.io 文档: https://snov.io/api
- Resend 文档: https://resend.com/docs
- GitHub Actions 文档: https://docs.github.com/en/actions

---

## 🎉 开始使用

### 最快开始（推荐）

1. 运行配置向导：`python setup_github_actions.py`
2. 按照 [SETUP_SUMMARY.md](SETUP_SUMMARY.md) 完成配置
3. 等待第二天自动运行

### 手动测试

```bash
cd src
python auto_workflow.py
```

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢以下服务提供的支持：
- LangGraph
- Snov.io
- Resend
- GitHub Actions
- Cloudflare Workers

---

**配置完成后，工作流将每天自动运行！** 🚀
