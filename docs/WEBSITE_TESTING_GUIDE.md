# 网站测试指南 - MIGAC

本文档提供详细的网站测试步骤和检查清单。

## 📋 测试概览

### 测试范围
- ✅ HTML语法验证
- ✅ 响应式布局测试
- ✅ 功能测试
- ✅ 性能测试
- ✅ SEO检查
- ✅ 跨浏览器兼容性

---

## 🖥️ 本地测试步骤

### 步骤1: 在浏览器中打开页面

#### 方法A: 直接打开文件
```bash
# 在浏览器中打开
# Windows/Mac: 双击 HTML 文件
# 或使用命令行
open assets/contact-optimized.html  # Mac
start assets/contact-optimized.html  # Windows
xdg-open assets/contact-optimized.html  # Linux
```

#### 方法B: 使用本地服务器（推荐）
```bash
# Python 3
cd assets
python3 -m http.server 8000

# 然后在浏览器访问:
# http://localhost:8000/contact-optimized.html
# http://localhost:8000/products.html
```

### 步骤2: 响应式布局测试

#### 使用浏览器开发者工具

1. **打开开发者工具**
   - Chrome/Edge: `F12` 或 `Ctrl+Shift+I` (Windows) / `Cmd+Shift+I` (Mac)
   - Firefox: `F12`

2. **切换到移动设备视图**
   - 点击设备图标（或按 `Ctrl+Shift+M`）
   - 选择不同设备尺寸

3. **测试的屏幕尺寸**

| 设备 | 分辨率 | 测试重点 |
|------|--------|---------|
| 手机 (小) | 375x667 | 导航菜单、表单布局 |
| 手机 (大) | 414x896 | 产品卡片、按钮大小 |
| 平板 | 768x1024 | 网格布局、图片显示 |
| 笔记本 | 1366x768 | 整体布局、字体大小 |
| 桌面 | 1920x1080 | 完整视图、间距 |

4. **测试清单**
   - [ ] 头部导航在移动端显示正常
   - [ ] 产品卡片在不同尺寸下布局正确
   - [ ] 表单字段在移动端易于输入
   - [ ] 按钮大小适合触摸操作
   - [ ] 图片在所有尺寸下清晰
   - [ ] WhatsApp按钮位置合适

### 步骤3: 功能测试

#### 联系页面功能测试

**1. 导航功能**
- [ ] 点击"获取免费报价"按钮，滚动到联系表单
- [ ] 点击"浏览产品目录"按钮，滚动到产品展示区
- [ ] 点击页脚链接，正确跳转
- [ ] 点击WhatsApp按钮，打开WhatsApp（或显示提示）

**2. 表单功能**
- [ ] 所有必填字段验证正常
- [ ] 提交空表单，显示验证错误
- [ ] 填写完整表单，提交成功
- [ ] 提交后显示成功消息
- [ ] 表单自动清空
- [ ] 页面滚动到成功消息

**3. 产品展示功能**
- [ ] 产品卡片悬停效果正常
- [ ] 所有产品图片显示（占位图片）
- [ ] 点击产品卡片（如有点击事件）

**4. WhatsApp按钮**
- [ ] 按钮固定在右下角
- [ ] 点击打开WhatsApp应用或网页版
- [ ] 预填充消息正确

#### 产品页面功能测试

**1. 筛选功能**
- [ ] 点击"全部产品"，显示所有产品
- [ ] 点击"水晶烛台"，只显示对应产品
- [ ] 点击"吊灯烛台"，只显示对应产品
- [ ] 点击"茶烛灯"，只显示对应产品
- [ ] 点击"装饰摆件"，只显示对应产品
- [ ] 点击"吊灯"，只显示对应产品
- [ ] 切换筛选器时过渡平滑

**2. 导航功能**
- [ ] 点击"首页"，跳转到联系页面
- [ ] 点击"产品目录"，当前页面高亮
- [ ] 点击"联系我们"，跳转到联系页面
- [ ] 点击"立即询盘"，跳转到联系页面

**3. 产品卡片**
- [ ] 所有8个产品卡片显示
- [ ] 产品标签（热销、新品、定制款）显示正确
- [ ] 产品信息完整
- [ ] 产品特性标签显示
- [ ] 起订量信息正确

**4. CTA区域**
- [ ] 点击"立即咨询定制"，跳转到联系页面
- [ ] 点击"下载完整产品目录"，打开邮件客户端

### 步骤4: 性能测试

#### 使用 Chrome DevTools Performance

1. **打开性能标签页**
2. **点击录制**
3. **刷新页面**
4. **停止录制**
5. **查看性能指标**

#### 关键性能指标

| 指标 | 目标值 | 当前状态 |
|------|--------|---------|
| 首次内容绘制 (FCP) | < 1.8s | ⏳ 需测试 |
| 最大内容绘制 (LCP) | < 2.5s | ⏳ 需测试 |
| 首次输入延迟 (FID) | < 100ms | ⏳ 需测试 |
| 累积布局偏移 (CLS) | < 0.1 | ⏳ 需测试 |

#### 使用 PageSpeed Insights

1. 访问 [PageSpeed Insights](https://pagespeed.web.dev/)
2. 输入网站URL（部署后）
3. 查看性能评分和建议

### 步骤5: SEO检查

#### 1. 检查 Meta 标签

在浏览器中按 `Ctrl+U` (Windows) 或 `Cmd+Option+U` (Mac) 查看源代码

检查项：
- [ ] `<title>` 标签存在且内容正确
- [ ] `<meta name="description">` 存在
- [ ] `<meta name="keywords">` 存在
- [ ] `<meta name="robots">` 存在
- [ ] Open Graph 标签完整
- [ ] Twitter Card 标签完整
- [ ] 规范链接 (canonical) 正确

#### 2. 使用 SEO 工具

**Chrome 扩展推荐**:
- SEO Minion
- MozBar
- Ahrefs SEO Toolbar

**在线工具**:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Screaming Frog SEO Spider](https://www.screamingfrog.com/seo-spider/)

### 步骤6: 跨浏览器测试

#### 测试的浏览器

| 浏览器 | 版本 | 测试项 |
|--------|------|--------|
| Chrome | 最新版本 | 全部功能 |
| Firefox | 最新版本 | 全部功能 |
| Safari | 最新版本 | 全部功能 |
| Edge | 最新版本 | 全部功能 |
| Safari (iOS) | 最新版本 | 移动端 |
| Chrome (Android) | 最新版本 | 移动端 |

#### 检查项
- [ ] 布局一致
- [ ] 功能正常
- [ ] 样式正确
- [ ] 没有JavaScript错误

### 步骤7: 表单提交测试

#### 测试 Formspree 集成

1. **打开控制台** (`F12` → Console)
2. **填写并提交表单**
3. **检查控制台是否有错误**

#### 测试场景

| 场景 | 预期结果 | 状态 |
|------|---------|------|
| 提交空表单 | 显示验证错误 | ⏳ |
| 只填写必填字段 | 提交成功 | ⏳ |
| 填写所有字段 | 提交成功 | ⏳ |
| 邮箱格式错误 | 显示验证错误 | ⏳ |
| 提交后 | 显示成功消息 | ⏳ |
| 提交后 | 表单清空 | ⏳ |

---

## 🌐 在线测试（部署后）

### 步骤1: 部署到生产环境

参考 `WEBSITE_OPTIMIZATION_GUIDE.md` 的"部署步骤"

### 步骤2: 在线功能测试

**测试 URL**:
- 联系页面: `https://miga.cc/contact-optimized.html`
- 产品页面: `https://miga.cc/products.html`

**测试清单**:
- [ ] 页面可以正常访问
- [ ] 所有链接正常工作
- [ ] 图片正常加载（替换真实图片后）
- [ ] 表单可以正常提交
- [ ] WhatsApp链接正常
- [ ] 页面加载速度可接受

### 步骤3: 使用在线测试工具

#### 1. Google PageSpeed Insights
```
URL: https://pagespeed.web.dev/
输入网址，获取性能评分
```

#### 2. GTmetrix
```
URL: https://gtmetrix.com/
输入网址，获取详细性能报告
```

#### 3. WebPageTest
```
URL: https://www.webpagetest.org/
输入网址，获取多地区测试结果
```

#### 4. SEO Checkers
- [Siteliner](https://www.siteliner.com/) - 内容检查
- [WooRank](https://www.woorank.com/) - 综合SEO检查
- [SEOptimer](https://www.seoptimer.com/) - 免费SEO审计

### 步骤4: 移动设备测试

#### 使用真实设备

**iOS 设备**:
1. 在 Safari 中打开网站
2. 测试所有功能
3. 检查显示效果

**Android 设备**:
1. 在 Chrome 中打开网站
2. 测试所有功能
3. 检查显示效果

#### 使用在线工具

- [BrowserStack](https://www.browserstack.com/) - 多设备测试
- [Responsinator](http://www.responsinator.com/) - 响应式测试
- [LambdaTest](https://www.lambdatest.com/) - 跨浏览器测试

---

## 🐛 常见问题排查

### 问题1: 页面样式混乱

**可能原因**:
- CSS文件未加载
- 浏览器缓存问题
- CSS语法错误

**解决方案**:
```bash
# 1. 检查HTML结构
grep -n "<style>" assets/contact-optimized.html

# 2. 清除浏览器缓存
# Chrome: Ctrl+Shift+Delete

# 3. 强制刷新
# Windows: Ctrl+F5
# Mac: Cmd+Shift+R
```

### 问题2: 图片不显示

**可能原因**:
- 图片URL错误
- 图片文件不存在
- 图片格式不支持

**解决方案**:
```bash
# 1. 检查图片URL
grep "img src" assets/contact-optimized.html

# 2. 测试图片URL
curl -I https://your-bucket.com/images/products/xxx.jpg

# 3. 检查图片文件
ls -lh assets/images/products/
```

### 问题3: 表单提交失败

**可能原因**:
- Formspree配置错误
- 网络问题
- JavaScript错误

**解决方案**:
```javascript
// 1. 打开浏览器控制台 (F12)
// 查看Console标签页的错误信息

// 2. 检查Network标签页
// 查看表单提交请求的状态

// 3. 验证Formspree表单ID
// mpqyvjee
```

### 问题4: 移动端布局问题

**可能原因**:
- 媒体查询错误
- viewport设置问题
- CSS兼容性问题

**解决方案**:
```css
/* 1. 检查viewport meta标签 */
<meta name="viewport" content="width=device-width, initial-scale=1.0">

/* 2. 测试媒体查询 */
@media (max-width: 768px) {
  /* 移动端样式 */
}
```

### 问题5: WhatsApp按钮不工作

**可能原因**:
- URL格式错误
- 手机号错误
- 链接被阻止

**解决方案**:
```html
<!-- 正确的WhatsApp链接格式 -->
<a href="https://wa.me/8619879476613?text=你好，我想咨询水晶烛台产品">
```

---

## ✅ 最终测试清单

### 部署前检查

- [ ] 所有HTML文件语法正确
- [ ] 所有CSS样式正确
- [ ] 所有JavaScript无错误
- [ ] 所有链接正确
- [ ] 所有占位图片标记清晰
- [ ] Formspree配置正确
- [ ] WhatsApp链接正确
- [ ] SEO元标签完整
- [ ] 响应式布局正常

### 部署后检查

- [ ] 网站可以正常访问
- [ ] 所有页面加载正常
- [ ] 所有图片正常显示
- [ ] 表单可以正常提交
- [ ] WhatsApp功能正常
- [ ] 移动端显示正常
- [ ] 性能评分可接受
- [ ] SEO检查通过

---

## 📊 测试报告模板

### 测试日期: ___________
### 测试人员: ___________
### 测试环境: ___________

#### 功能测试结果

| 功能 | 测试结果 | 备注 |
|------|---------|------|
| 页面加载 | ✅/❌ | |
| 导航功能 | ✅/❌ | |
| 表单提交 | ✅/❌ | |
| 产品筛选 | ✅/❌ | |
| WhatsApp链接 | ✅/❌ | |

#### 响应式测试结果

| 设备尺寸 | 测试结果 | 备注 |
|---------|---------|------|
| 手机 (375px) | ✅/❌ | |
| 平板 (768px) | ✅/❌ | |
| 桌面 (1920px) | ✅/❌ | |

#### 性能测试结果

| 指标 | 目标值 | 实际值 | 状态 |
|------|--------|--------|------|
| FCP | < 1.8s | ___s | ✅/❌ |
| LCP | < 2.5s | ___s | ✅/❌ |

#### 发现的问题

1. ___________________________
2. ___________________________
3. ___________________________

#### 修复建议

1. ___________________________
2. ___________________________
3. ___________________________

---

## 📞 需要帮助？

如遇到技术问题，请联系：

- **邮箱**: info@miga.cc
- **WhatsApp**: +86-19879476613
- **电话**: +86-19879476613

---

**文档版本**: 1.0
**更新日期**: 2024-01-01

---

## 🚀 开始测试

现在您已经准备好测试网站了！

**快速测试步骤**:
1. 在浏览器中打开 `assets/contact-optimized.html`
2. 在浏览器中打开 `assets/products.html`
3. 使用上述测试清单逐项检查
4. 记录发现的问题
5. 修复问题并重新测试

祝您测试顺利！✅
