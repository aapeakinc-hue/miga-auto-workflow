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
### API 配置
- **snov.io**:
  - API Token: `fbf98546081c2793e21d6de6540ce2ca`
  - Client ID: `746628993ee9eda28e455e53751030bd`
  
- **resend**:
  - API Key: `re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F`
  - 发件邮箱: `aapeakinc@gmail.com`
  
### 注意事项
⚠️ **resend 域名验证**: 
- 使用 gmail.com 作为发件域名需要在 resend.com 上验证域名
- 如果未验证，邮件发送会失败（返回 403 错误）
- 解决方案：在 https://resend.com/domains 上添加并验证你的域名

## 测试结果
工作流已成功测试，各节点运行正常：
- ✅ 产品信息抓取成功
- ✅ 客户搜索成功（测试搜索到5个相关网站）
- ✅ 邮箱获取成功（部分邮箱为估计值）
- ✅ 邮件生成成功
- ⚠️ 邮件发送失败（因域名未验证，需要配置 resend 域名）
