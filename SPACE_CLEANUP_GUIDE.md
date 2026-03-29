# 空间清理指南

## 当前空间使用情况
- **已使用**: 702MB
- **总容量**: 1.0GB
- **使用率**: 70%

---

## 可以安全清理的文件（不影响工作流）

### 1. Python缓存目录 ⭐ 强烈推荐
**路径**: `__pycache__/`
**大小**: ~152KB
**影响**: 无，会自动重新生成
**清理命令**:
```bash
rm -rf __pycache__
```
**释放空间**: ~152KB

### 2. 临时脚本目录 ⭐ 强烈推荐
**路径**: `.temp_scripts/`
**大小**: ~500KB
**影响**: 无，这些都是已移除的旧版本文件
**清理命令**:
```bash
rm -rf .temp_scripts
```
**释放空间**: ~500KB

### 3. 临时图片和文件夹 ⭐ 推荐
**路径**:
- `assets/temp-images/` (~34MB)
- `assets/新增資料夾/` (~21MB)
- `assets/新增資料夶 (2)/` (~21MB)

**大小**: ~76MB
**影响**: 无，这些都是临时文件
**清理命令**:
```bash
rm -rf assets/temp-images
rm -rf "assets/新增資料夾"
rm -rf "assets/新增資料夶 (2)"
```
**释放空间**: ~76MB

### 4. 临时压缩包 ⭐ 推荐
**路径**:
- `assets/新增資料夾.zip` (~19MB)
- `assets/新增資料夶 (2).zip` (~18MB)

**大小**: ~37MB
**影响**: 无，临时压缩包
**清理命令**:
```bash
rm -f "assets/新增資料夾.zip"
rm -f "assets/新增資料夶 (2).zip"
```
**释放空间**: ~37MB

### 5. 旧的网站压缩包 ⭐ 推荐
**路径**: `miga-website.tar.gz`
**大小**: ~140MB
**影响**: 无，这是旧的备份文件
**清理命令**:
```bash
rm -f miga-website.tar.gz
```
**释放空间**: ~140MB

### 6. Cloudflare部署旧压缩包 ⭐ 可选
**路径**: `cloudflare-deploy/miga-website-final.tar.gz`
**大小**: ~5.8MB
**影响**: 无，如果网站已部署，可以删除
**清理命令**:
```bash
rm -f cloudflare-deploy/miga-website-final.tar.gz
```
**释放空间**: ~5.8MB

---

## 可选择性清理的文件（根据需要）

### 7. Cloudflare部署资源 ⚠️ 谨慎
**路径**:
- `cloudflare-deploy/images/` (~43MB)
- `cloudflare-deploy/videos/` (~7.8MB)

**大小**: ~50.8MB
**影响**: 如果需要重新部署网站，这些文件会用到
**清理命令**:
```bash
# 仅在确认不需要重新部署时清理
rm -rf cloudflare-deploy/images
rm -rf cloudflare-deploy/videos
```
**释放空间**: ~50.8MB

### 8. 日志文件 ⚠️ 谨慎
**路径**: `logs/`
**大小**: ~24KB
**影响**: 会丢失历史日志，建议保留最近的
**清理命令**:
```bash
# 只清理7天前的日志
find logs/ -name "*.txt" -mtime +7 -delete
find logs/ -name "*.json" -mtime +7 -delete
```
**释放空间**: 几KB

---

## 必须保留的文件（影响工作流）

### 🚫 不能删除的目录和文件

| 路径 | 大小 | 说明 |
|------|------|------|
| `src/` | ~552KB | 工作流核心代码 |
| `config/` | ~24KB | 配置文件 |
| `requirements.txt` | ~几KB | 依赖包列表 |
| `.github/` | ~几KB | GitHub Actions配置 |
| `AGENTS.md` | ~24KB | 项目文档 |
| `README.md` | ~16KB | 项目说明 |
| `docs/` | ~120KB | 文档目录 |

---

## 推荐清理方案

### 方案一：安全清理（推荐）⭐
**清理内容**:
1. `__pycache__/`
2. `.temp_scripts/`
3. `assets/temp-images/`
4. `assets/新增資料夶/`
5. `assets/新增資料夶 (2)/`
6. `assets/新增資料夶.zip`
7. `assets/新增資料夶 (2).zip`
8. `miga-website.tar.gz`

**清理命令**:
```bash
# 一键清理（安全版）
rm -rf __pycache__
rm -rf .temp_scripts
rm -rf assets/temp-images
rm -rf "assets/新增資料夶"
rm -rf "assets/新增資料夶 (2)"
rm -f "assets/新增資料夶.zip"
rm -f "assets/新增資料夶 (2).zip"
rm -f miga-website.tar.gz
```

**释放空间**: ~254MB
**影响**: 无
**清理后空间**: ~448MB / 1.0GB (44.8%)

---

### 方案二：深度清理（谨慎）
**清理内容**: 方案一的所有内容 + cloudflare-deploy资源

**清理命令**:
```bash
# 执行方案一的所有清理
rm -rf __pycache__
rm -rf .temp_scripts
rm -rf assets/temp-images
rm -rf "assets/新增資料夶"
rm -rf "assets/新增資料夶 (2)"
rm -f "assets/新增資料夶.zip"
rm -f "assets/新增資料夶 (2).zip"
rm -f miga-website.tar.gz
rm -f cloudflare-deploy/miga-website-final.tar.gz

# 清理cloudflare资源（仅确认不需要重新部署时）
rm -rf cloudflare-deploy/images
rm -rf cloudflare-deploy/videos
```

**释放空间**: ~305MB
**影响**: 如果需要重新部署网站，需要重新准备资源
**清理后空间**: ~397MB / 1.0GB (39.7%)

---

## 清理前检查清单

### ✅ 清理前确认
- [ ] 工作流代码已备份（如需要）
- [ ] 确认不再需要临时文件
- [ ] 确认网站已成功部署（如果要删除cloudflare资源）
- [ ] 了解每个删除文件的作用

### ✅ 清理后验证
- [ ] 检查工作流是否能正常运行
- [ ] 检查配置文件是否完整
- [ ] 测试关键功能是否正常

---

## 快速清理命令

### 一键安全清理脚本
```bash
#!/bin/bash
# 安全清理脚本 - 释放约254MB空间

echo "开始清理..."

# 删除Python缓存
echo "删除Python缓存..."
rm -rf __pycache__

# 删除临时脚本
echo "删除临时脚本..."
rm -rf .temp_scripts

# 删除临时图片
echo "删除临时图片..."
rm -rf assets/temp-images

# 删除临时文件夹
echo "删除临时文件夹..."
rm -rf "assets/新增資料夶"
rm -rf "assets/新增資料夶 (2)"

# 删除临时压缩包
echo "删除临时压缩包..."
rm -f "assets/新增資料夶.zip"
rm -f "assets/新增資料夶 (2).zip"

# 删除旧网站压缩包
echo "删除旧网站压缩包..."
rm -f miga-website.tar.gz

echo "清理完成！"
echo "释放空间: ~254MB"
```

### 使用方法
```bash
# 创建清理脚本
cat > clean_space.sh << 'EOF'
#!/bin/bash
echo "开始清理..."
rm -rf __pycache__
rm -rf .temp_scripts
rm -rf assets/temp-images
rm -rf "assets/新增資料夶"
rm -rf "assets/新增資料夶 (2)"
rm -f "assets/新增資料夶.zip"
rm -f "assets/新增資料夶 (2).zip"
rm -f miga-website.tar.gz
echo "清理完成！释放空间: ~254MB"
EOF

# 添加执行权限
chmod +x clean_space.sh

# 执行清理
./clean_space.sh
```

---

## 清理后空间对比

| 方案 | 清理前 | 清理后 | 释放空间 | 使用率 |
|------|--------|--------|----------|--------|
| 方案一（安全） | 702MB | ~448MB | ~254MB | 44.8% |
| 方案二（深度） | 702MB | ~397MB | ~305MB | 39.7% |

---

## 常见问题

### Q1: 清理后会影响工作流运行吗？
**A**: 方案一完全不会影响工作流，方案二需要在确认不需要重新部署网站时执行。

### Q2: 删除后能恢复吗？
**A**: 不能直接恢复。如果不确定某个文件是否需要，建议先移动到临时目录而不是直接删除。

### Q3: 如何判断某个文件是否可以删除？
**A**: 参考本指南的分类，优先清理标记为"强烈推荐"和"推荐"的文件。

### Q4: 清理频率建议多久一次？
**A**: 建议每周清理一次临时文件，每月清理一次日志文件。

### Q5: 清理后空间还会增长吗？
**A**: 会。工作流运行会产生日志文件，Python会生成新的缓存。建议定期清理。

---

## 总结

### 推荐操作
✅ **执行方案一（安全清理）**
- 释放空间：~254MB
- 影响：无
- 风险：低

### 清理后维护
1. 定期清理日志文件（每周）
2. 定期清理临时文件（每周）
3. 监控空间使用情况（每天）

### 注意事项
⚠️ 删除前确认文件是否真的不需要
⚠️ 重要文件先备份再删除
⚠️ 清理后测试工作流是否正常

---

**文档生成时间**: 2026年3月29日
**版本**: v1.0
