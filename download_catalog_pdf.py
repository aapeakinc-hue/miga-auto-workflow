"""
读取MIGAC产品目录PDF
"""
import requests
import os

# 下载PDF文件
url = "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2FMIGAC+CATALOGUE.pdf&nonce=d5474b14-aa3e-41c5-9301-7ba2b8ca1f5c&project_id=7620116912135094306&sign=53e059a3a1aa0d70f593754fcb1008c0c2bd7080f7d0a1ceca1f5cbfeb83adb6"

print("正在下载PDF文件...")
response = requests.get(url)

if response.status_code == 200:
    with open("assets/MIGAC_CATALOGUE.pdf", "wb") as f:
        f.write(response.content)
    print(f"✅ PDF文件下载成功！大小: {len(response.content)} bytes")
else:
    print(f"❌ 下载失败: {response.status_code}")
