# 📋 MIGA 外贸客户开发系统 - 部署清单

## 🚀 部署前检查

### ✅ 环境要求
- [ ] Python 3.8+ 已安装
- [ ] pip 或 uv 包管理器已安装
- [ ] 网络连接正常（访问外部API）

### ✅ 依赖安装
```bash
# 检查 Python 版本
python --version

# 安装依赖
pip install -r requirements.txt

# 或使用 uv
uv pip install -r requirements.txt
```

### ✅ 配置文件检查
- [ ] `config/email_generate_llm_cfg.json` 存在且有效
- [ ] API Key 已正确配置
- [ ] 发件邮箱已验证

---

## 🔑 API 配置检查

### Snov.io API
- [ ] API Token 已设置: `fbf98546081c2793e21d6de6540ce2ca`
- [ ] Client ID 已设置: `746628993ee9eda28e455e53751030bd`
- [ ] 测试 API 连接正常

### Resend API
- [ ] API Key 已设置: `re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F`
- [ ] 发件邮箱 `info@miga.cc` 已验证
- [ ] 域名 `miga.cc` DNS 配置正确
- [ ] 测试邮件发送正常

---

## 🌐 域名配置检查

### Cloudflare Pages
- [ ] 自定义域名 `products.miga.cc` 已激活
- [ ] SSL 证书已启用
- [ ] 页面可正常访问: https://products.miga.cc

### 阿里云 DNS
- [ ] CNAME 记录已配置: `products → migac-website.pages.dev`
- [ ] DNS 生效时间已过（通常 10-30 分钟）
- [ ] 域名解析正常

---

## 📊 CRM 系统部署

### 数据库初始化
```bash
# 运行 CRM 系统初始化
python crm_system.py
```

检查项:
- [ ] `miga_crm.db` 数据库文件已创建
- [ ] 所有表结构已创建（customers, interactions, orders）
- [ ] 无错误信息

### 数据导入
```bash
# 导入工作流结果（如果有）
python import_workflow_results.py
```

检查项:
- [ ] 数据导入成功
- [ ] 客户数据完整
- [ ] 互动记录已创建

---

## 🧪 功能测试

### 1. 工作流测试
```bash
# 运行完整工作流
bash scripts/local_run.sh -m flow
```

检查项:
- [ ] 产品信息抓取成功
- [ ] 客户搜索成功
- [ ] 邮箱获取成功
- [ ] 邮件生成成功
- [ ] 邮件发送成功
- [ ] 整体流程无错误

### 2. CRM 工具测试
```bash
# 运行 CRM 工具
python crm_tools.py
```

检查项:
- [ ] 自动跟进提醒正常
- [ ] 客户分类摘要正确
- [ ] 邮件模板可用

### 3. 邮件发送测试
```bash
# 发送测试邮件（可选）
python -c "from src.graphs.nodes.email_send_node import *; send_test_email()"
```

检查项:
- [ ] 测试邮件发送成功
- [ ] 邮件内容正确
- [ ] 收件人收到邮件

---

## 📚 文档检查

### 核心文档
- [ ] `README.md` - 项目概览（已更新）
- [ ] `AGENTS.md` - 工作流详细文档
- [ ] `CRM_README.md` - CRM 使用指南
- [ ] `ANNUAL_PLAN.md` - 年度开发计划
- [ ] `QUICK_REFERENCE.md` - 快速参考指南
- [ ] `PROJECT_SUMMARY.md` - 项目总结
- [ ] `DEPLOYMENT_CHECKLIST.md` - 部署清单（本文件）

### 文档内容检查
- [ ] 所有链接有效
- [ ] 代码示例正确
- [ ] 配置信息准确
- [ ] 步骤描述清晰

---

## 🔍 常见问题排查

### 问题1: Python 版本不兼容
**症状**: ImportError 或语法错误
**解决**: 升级 Python 到 3.8+

```bash
python --version  # 检查版本
```

### 问题2: 依赖包缺失
**症状**: ModuleNotFoundError
**解决**: 安装缺失的依赖包

```bash
pip install langgraph langchain requests pydantic jinja2
```

### 问题3: API Key 无效
**症状**: 403 或 401 错误
**解决**: 检查 API Key 配置

```bash
# 检查配置文件
cat config/email_generate_llm_cfg.json
```

### 问题4: 邮箱未验证
**症状**: 邮件发送失败（403 错误）
**解决**: 在 Resend 控制台验证域名

1. 登录 Resend 控制台
2. 进入域名设置
3. 验证 `info@miga.cc`
4. 等待验证完成

### 问题5: DNS 解析失败
**症状**: 无法访问 products.miga.cc
**解决**: 检查 DNS 配置

1. 登录阿里云 DNS 控制台
2. 检查 CNAME 记录
3. 确认记录生效

---

## 📊 性能优化

### 工作流优化
- [ ] 优化搜索关键词
- [ ] 调整过滤规则
- [ ] 优化邮件模板

### CRM 优化
- [ ] 定期清理无效客户
- [ ] 优化查询索引
- [ ] 定期备份数据

### 邮件优化
- [ ] 测试最佳发送时间
- [ ] 优化邮件主题
- [ ] 个性化邮件内容

---

## 🔒 安全检查

### API 安全
- [ ] API Key 不在代码中硬编码
- [ ] 使用环境变量存储敏感信息
- [ ] 定期更新 API Key

### 数据安全
- [ ] 定期备份数据库
- [ ] 导出数据到云端
- [ ] 保护客户隐私

### 访问控制
- [ ] 限制数据库访问权限
- [ ] 使用强密码
- [ ] 定期审计访问日志

---

## 📅 定期维护

### 每周维护
- [ ] 检查邮件发送成功率
- [ ] 查看客户回复
- [ ] 更新跟进任务

### 每月维护
- [ ] 分析数据报表
- [ ] 清理无效客户
- [ ] 优化工作流

### 每季度维护
- [ ] 复盘市场开发效果
- [ ] 调整年度计划
- [ ] 更新技术栈

---

## 🎯 部署后验证

### 功能验证
- [ ] 工作流运行正常
- [ ] 邮件发送成功
- [ ] CRM 数据完整
- [ ] 跟进提醒准确

### 性能验证
- [ ] 响应时间正常
- [ ] 内存使用合理
- [ ] 无内存泄漏

### 稳定性验证
- [ ] 连续运行 24 小时无崩溃
- [ ] 错误处理完善
- [ ] 日志记录完整

---

## ✅ 部署完成检查

### 核心功能
- [ ] 工作流正常运行
- [ ] 邮件发送成功
- [ ] CRM 系统可用
- [ ] 文档完整

### 配置正确
- [ ] API Key 有效
- [ ] 域名解析正常
- [ ] 邮箱已验证
- [ ] 数据库已初始化

### 文档齐全
- [ ] 使用文档完整
- [ ] 故障排查文档可用
- [ ] 联系方式清晰

---

## 📞 技术支持

如有问题或需要帮助，请联系：
- **邮箱**: info@miga.cc
- **官网**: https://miga.cc

---

**部署检查清单完成！** 🎉

如所有检查项都已完成，系统已准备就绪，可以开始使用！
