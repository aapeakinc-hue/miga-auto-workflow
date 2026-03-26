# 📧 邮箱抓取 API 配置指南

## 📊 免费邮箱抓取 API 对比

| API 名称 | 免费配额 | 限制 | 优势 | 难度 |
|---------|---------|------|------|------|
| **Snov.io** | 50次/月 | 每月50次搜索 | 准确率高，数据丰富 | ⭐⭐ |
| **Hunter.io** | 25次/月 | 每天10次 | 简单易用 | ⭐ |
| **Clearbit** | 50次/月 | 每月50次 | 数据质量高 | ⭐⭐⭐ |
| **Voila Norbert** | 50次/月 | 每月50次 | 批量搜索 | ⭐⭐⭐ |

---

## 🚀 推荐方案

### 方案 1：多账户 Snov.io（最推荐）✨

**优势**：
- ✅ API 统一，代码兼容性好
- ✅ 准确率高，数据丰富
- ✅ 支持批量搜索

**配置步骤**：

#### 1. 注册多个 Snov.io 账户

注册 **3-5 个** Snov.io 免费账户：
- 账户 1：邮箱1@gmail.com
- 账户 2：邮箱2@gmail.com
- 账户 3：邮箱3@gmail.com
- ...

#### 2. 获取每个账户的 API Key

每个账户登录后：
```
1. 访问：https://snov.io/api-access-token
2. 点击 "Generate API Token"
3. 复制 API Key
```

#### 3. 配置 GitHub Secrets

在 GitHub 仓库设置中添加多个 Secrets：

```
SNOVIO_API_KEYS=snovio_key1,snovio_key2,snovio_key3
```

**配额计算**：
```
3 个账户 × 50次/月 = 150次/月
5 个账户 × 50次/月 = 250次/月
```

---

### 方案 2：多 API 混合使用

**优势**：
- ✅ 总配额更高
- ✅ 降低单一 API 依赖
- ✅ 数据来源多样化

**配置步骤**：

#### 1. 注册多个 API

**Snov.io**（50次/月）:
```
1. 访问：https://snov.io
2. 注册免费账户
3. 获取 API Key
```

**Hunter.io**（25次/月）:
```
1. 访问：https://hunter.io
2. 注册免费账户
3. 获取 API Key
```

**Clearbit**（50次/月）:
```
1. 访问：https://clearbit.com
2. 注册免费账户
3. 获取 API Key
```

#### 2. 配置 GitHub Secrets

在 GitHub 仓库设置中添加：

```
SNOVIO_API_KEYS=snovio_key1,snovio_key2
HUNTER_API_KEY=hunter_key
CLEARBIT_API_KEY=clearbit_key
```

**配额计算**：
```
Snov.io (2个账户): 100次/月
Hunter.io: 25次/月
Clearbit: 50次/月
-------------------
总计: 175次/月
```

---

### 方案 3：纯估算（零成本）

**优势**：
- ✅ 完全免费
- ✅ 无需注册
- ✅ 无配额限制

**缺点**：
- ❌ 准确率低
- ❌ 可能无效
- ❌ 需要手动验证

**适用场景**：
- 测试阶段
- 低需求场景
- 后期手动验证

---

## 🔧 配置步骤

### 步骤 1：获取 API Keys

#### Snov.io
```
1. 访问：https://snov.io
2. 注册账户（使用不同邮箱）
3. 访问：https://snov.io/api-access-token
4. 点击 "Generate API Token"
5. 复制 API Key
```

#### Hunter.io
```
1. 访问：https://hunter.io
2. 注册账户
3. 访问：https://hunter.io/api_keys
4. 复制 API Key
```

#### Clearbit
```
1. 访问：https://clearbit.com
2. 注册账户
3. 访问：https://clearbit.com/developers
4. 复制 API Key
```

---

### 步骤 2：配置 GitHub Secrets

#### 方式 1：单个 Key（兼容旧版本）

```
SNOVIO_API_KEY=your_snovio_key_here
```

#### 方式 2：多个 Snov.io Keys（推荐）

```
SNOVIO_API_KEYS=key1,key2,key3,key4,key5
```

**注意**：
- 使用逗号分隔
- 不要有空格
- 至少 3-5 个 Key

#### 方式 3：多 API 混合

```
SNOVIO_API_KEYS=key1,key2
HUNTER_API_KEY=hunter_key_here
CLEARBIT_API_KEY=clearbit_key_here
```

---

### 步骤 3：添加到 GitHub

1. 访问你的 GitHub 仓库
2. 点击 **Settings**
3. 点击左侧 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 添加以下 Secrets：

```
Name: SNOVIO_API_KEYS
Value: key1,key2,key3,key4,key5

Name: HUNTER_API_KEY
Value: your_hunter_key

Name: CLEARBIT_API_KEY
Value: your_clearbit_key
```

---

## 📊 配额计算

### 场景 1：3 个 Snov.io 账户

```
账户 1: 50次/月
账户 2: 50次/月
账户 3: 50次/月
-------------------
总计: 150次/月
每天: 150/30 = 5次/天
```

### 场景 2：5 个 Snov.io 账户

```
5 个账户 × 50次/月 = 250次/月
每天: 250/30 = 8次/天
```

### 场景 3：混合方案

```
Snov.io (2个): 100次/月
Hunter.io: 25次/月
Clearbit: 50次/月
-------------------
总计: 175次/月
每天: 175/30 = 6次/天
```

---

## 🔄 自动轮换机制

系统会自动：
1. ✅ 轮换使用不同的 API Key
2. ✅ 记录每个 Key 的使用次数
3. ✅ 避开已达到限制的 Key
4. ✅ 优先使用剩余配额多的 Key

**示例**：
```
第1次搜索: 使用 Snovio 账户1 (1/50)
第2次搜索: 使用 Snovio 账户2 (1/50)
第3次搜索: 使用 Hunter.io (1/25)
第4次搜索: 使用 Snovio 账户3 (1/50)
...
```

---

## 📈 监控和管理

### 查看使用统计

运行工作流后，查看日志中的统计信息：

```
📊 邮箱 API 使用统计:
总 Key 数: 5
总使用: 15/250

详情:
  snovio_1: 5/50 (剩余: 45)
  snovio_2: 3/50 (剩余: 47)
  snovio_3: 4/50 (剩余: 46)
  snovio_4: 2/50 (剩余: 48)
  snovio_5: 1/50 (剩余: 49)
```

### 月初自动重置

系统会在每月初自动重置计数：
```
🔄 所有 API Key 使用计数已重置
```

---

## 💡 最佳实践

### 1. 建议配置

```
✅ 推荐配置：
- 3-5 个 Snov.io 账户
- 或 2 个 Snov.io + 1 个 Hunter.io + 1 个 Clearbit
```

### 2. 定期检查

```
✅ 每周检查使用情况
✅ 每月初查看配额是否重置
✅ 发现异常及时处理
```

### 3. 备份方案

```
✅ 保留纯估算模式作为备选
✅ API 用尽时自动切换
✅ 不影响工作流运行
```

---

## ❓ 常见问题

### Q1: Snov.io API 限流怎么办？

**A**：
1. 添加更多的 API Key
2. 系统会自动轮换使用
3. 使用混合方案（Hunter.io + Clearbit）

---

### Q2: 如何查看剩余配额？

**A**：
1. 查看工作流日志
2. 访问 API 提供商后台
3. 使用我们的统计工具

---

### Q3: 免费配额用完了怎么办？

**A**：
1. 等待下个月自动重置
2. 注册更多免费账户
3. 升级到付费版（可选）

---

### Q4: 如何添加新的 API Key？

**A**：
1. 获取新的 API Key
2. 在 GitHub Secrets 中添加
3. 格式：`SNOVIO_API_KEYS=key1,key2,key3`

---

### Q5: API Key 会过期吗？

**A**：
- ✅ 不会过期（永久有效）
- ⚠️  每月配额会重置
- ⚠️  长时间不用可能失效

---

## 🎉 总结

### 推荐配置

**方案 1：多账户 Snov.io**（最简单）
```
3-5 个 Snov.io 账户
配额: 150-250次/月
成本: 免费
```

**方案 2：混合方案**（配额更高）
```
2 个 Snov.io + 1 个 Hunter.io + 1 个 Clearbit
配额: 175次/月
成本: 免费
```

### 快速开始

1. ✅ 注册 3-5 个 Snov.io 账户
2. ✅ 获取每个账户的 API Key
3. ✅ 在 GitHub Secrets 中配置
4. ✅ 系统自动轮换使用

---

## 📞 需要帮助？

如果遇到问题，请：
1. 检查 API Key 是否正确
2. 查看工作流日志
3. 联系技术支持

---

**祝使用愉快！🎉**
