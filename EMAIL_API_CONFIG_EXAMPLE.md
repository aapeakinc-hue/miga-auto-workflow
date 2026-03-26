# 📧 邮箱 API 配置示例

## GitHub Secrets 配置

### 方式 1：单个 Snov.io Key（兼容旧版本）
```
SNOVIO_API_KEY=snovio_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 方式 2：多个 Snov.io Keys（推荐）✨
```
SNOVIO_API_KEYS=snovio_key1,snovio_key2,snovio_key3,snovio_key4,snovio_key5
```

### 方式 3：多 API 混合
```
SNOVIO_API_KEYS=snovio_key1,snovio_key2
HUNTER_API_KEY=hunter_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLEARBIT_API_KEY=clearbit_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 如何获取 API Keys

### 1. Snov.io API Keys（推荐）

**步骤**：
1. 访问：https://snov.io
2. 注册 3-5 个免费账户（使用不同邮箱）
3. 每个账户登录后访问：https://snov.io/api-access-token
4. 点击 "Generate API Token"
5. 复制 API Key

**示例 Keys**：
```
snovio_key1 = "snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
snovio_key2 = "snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o7p"
snovio_key3 = "snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o8p"
snovio_key4 = "snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o9p"
snovio_key5 = "snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o0p"
```

**配置到 GitHub Secrets**：
```
SNOVIO_API_KEYS=snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p,snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o7p,snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o8p,snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o9p,snovio_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o0p
```

**配额**：
```
5 个账户 × 50次/月 = 250次/月
每天: 250/30 ≈ 8次/天
```

---

### 2. Hunter.io API Key

**步骤**：
1. 访问：https://hunter.io
2. 注册免费账户
3. 访问：https://hunter.io/api_keys
4. 复制 API Key

**示例 Key**：
```
hunter_key = "hunter_1a2b3c4d5e6f7g8h9i0j"
```

**配置到 GitHub Secrets**：
```
HUNTER_API_KEY=hunter_1a2b3c4d5e6f7g8h9i0j
```

**配额**：
```
25次/月
每天: 25/30 ≈ 1次/天
```

---

### 3. Clearbit API Key

**步骤**：
1. 访问：https://clearbit.com
2. 注册免费账户
3. 访问：https://clearbit.com/developers
4. 复制 API Key

**示例 Key**：
```
clearbit_key = "sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**配置到 GitHub Secrets**：
```
CLEARBIT_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**配额**：
```
50次/月
每天: 50/30 ≈ 2次/天
```

---

## 配额对比

### 单账户 Snov.io
```
50次/月
每天: 1-2次
```

### 多账户 Snov.io（3个账户）
```
150次/月
每天: 5次
```

### 多账户 Snov.io（5个账户）
```
250次/月
每天: 8次
```

### 混合方案
```
Snov.io (2个): 100次/月
Hunter.io: 25次/月
Clearbit: 50次/月
-------------------
总计: 175次/月
每天: 6次
```

---

## 推荐配置

### 最低配置
```
3 个 Snov.io 账户
配额: 150次/月
每天: 5次
```

### 推荐配置 ✨
```
5 个 Snov.io 账户
配额: 250次/月
每天: 8次
```

### 高级配置
```
3 个 Snov.io + 1 个 Hunter.io + 1 个 Clearbit
配额: 175次/月
每天: 6次
```

---

## 如何添加到 GitHub

### 步骤 1：访问 GitHub Secrets
```
1. 访问你的 GitHub 仓库
2. 点击 Settings
3. 点击 Secrets and variables → Actions
4. 点击 New repository secret
```

### 步骤 2：添加 Snov.io Keys
```
Name: SNOVIO_API_KEYS
Value: snovio_key1,snovio_key2,snovio_key3,snovio_key4,snovio_key5

注意：
- 使用逗号分隔
- 不要有空格
- 至少 3-5 个 Key
```

### 步骤 3：添加 Hunter.io Key（可选）
```
Name: HUNTER_API_KEY
Value: hunter_1a2b3c4d5e6f7g8h9i0j
```

### 步骤 4：添加 Clearbit Key（可选）
```
Name: CLEARBIT_API_KEY
Value: sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 测试配置

### 测试脚本
```python
from src.email_api_manager import setup_email_apis, email_api_manager
from src.tools.email_fetch_multi_api import fetch_emails_from_domain

# 设置 APIs
setup_email_apis()

# 打印统计
stats = email_api_manager.get_usage_stats()
print(f"✅ 已配置 {stats['total_keys']} 个 API Key")

# 测试获取邮箱
emails = fetch_emails_from_domain("miga.cc", max_results=5)
print(f"✅ 找到 {len(emails)} 个邮箱")
```

---

## 故障排查

### 问题 1：没有可用的 API Key

**原因**：所有 API Key 都已达到限制

**解决**：
1. 等待下个月自动重置
2. 添加更多 API Key
3. 使用估算邮箱作为备选

---

### 问题 2：API 调用失败

**原因**：
- API Key 错误
- 网络问题
- API 服务异常

**解决**：
1. 检查 API Key 是否正确
2. 查看工作流日志
3. 联系技术支持

---

### 问题 3：配额不足

**原因**：使用的次数超过了免费配额

**解决**：
1. 添加更多 API Key
2. 升级到付费版
3. 等待下月重置

---

## 常见问题

### Q1: API Key 会过期吗？

**A**：
- ✅ 不会过期（永久有效）
- ⚠️  每月配额会重置
- ⚠️  长时间不用可能失效

---

### Q2: 如何查看剩余配额？

**A**：
1. 查看工作流日志
2. 访问 API 提供商后台
3. 使用统计工具

---

### Q3: 可以混合使用不同的 API 吗？

**A**：
- ✅ 可以！系统会自动轮换
- ✅ 优先使用配额多的 API
- ✅ 失败时自动切换

---

### Q4: 如何添加新的 API Key？

**A**：
1. 获取新的 API Key
2. 在 GitHub Secrets 中添加
3. 格式：`SNOVIO_API_KEYS=key1,key2,key3`

---

### Q5: 免费配额用完了怎么办？

**A**：
1. 等待下个月自动重置
2. 注册更多免费账户
3. 升级到付费版（可选）

---

## 📞 需要帮助？

如果遇到问题，请：
1. 检查 API Key 是否正确
2. 查看工作流日志
3. 查看 EMAIL_API_SETUP_GUIDE.md

---

**祝配置顺利！🎉**
