# ⚡ WinSCP快速操作卡片

## 📥 下载文件（2分钟）

### 1. 连接WinSCP
```
主机: 您的服务器IP
端口: 22
用户: root
密码: 您的密码
```

### 2. 下载文件
- 右侧窗口: `/workspace/projects/miga-website-deploy.tar.gz`
- 左侧窗口: 选择保存位置
- 拖拽文件到左侧

---

## 📦 解压文件（10秒）

### Windows操作
1. 右键点击 `miga-website-deploy.tar.gz`
2. 选择"解压到当前文件夹"
3. 得到 `cloudflare-deploy` 文件夹

---

## 📤 上传到Cloudflare（3分钟）

### 步骤
1. 打开: https://dash.cloudflare.com/
2. 登录
3. Workers & Pages → 您的项目
4. Upload assets → 拖拽 `cloudflare-deploy` 文件夹
5. Deploy

---

## 🌐 配置域名（1分钟）

1. Custom domains → Set up a custom domain
2. 输入: `miga.cc`
3. Continue → Activate domain

---

## ✅ 验证（1分钟）

访问:
- https://miga.cc
- https://miga.cc/products.html

---

## 🎯 总时间: 5-10分钟

**详细指南**: 查看 `WINSCP_GUIDE.md`
