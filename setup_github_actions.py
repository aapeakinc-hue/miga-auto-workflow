"""
GitHub Actions 快速配置向导
帮助用户快速完成 GitHub Actions 配置
"""
import os
import json
import subprocess
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_step(step, text):
    """打印步骤"""
    print(f"📌 步骤 {step}: {text}")

def print_success(text):
    """打印成功信息"""
    print(f"✅ {text}")

def print_error(text):
    """打印错误信息"""
    print(f"❌ {text}")

def print_info(text):
    """打印信息"""
    print(f"ℹ️  {text}")

def check_git_repository():
    """检查是否为 Git 仓库"""
    print_step(1, "检查 Git 仓库状态")

    git_dir = Path(".git")
    if git_dir.exists():
        print_success("这是一个 Git 仓库")

        # 检查是否有远程仓库
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stdout.strip():
                print_info(f"远程仓库: {result.stdout.strip()}")
                return True, True  # 是 Git 仓库，有远程仓库
            else:
                print_info("本地 Git 仓库，尚未配置远程仓库")
                return True, False  # 是 Git 仓库，无远程仓库
        except Exception as e:
            print_info(f"无法检查远程仓库: {e}")
            return True, False
    else:
        print_info("当前目录不是 Git 仓库")
        return False, False  # 不是 Git 仓库

def check_github_actions_config():
    """检查 GitHub Actions 配置文件"""
    print_step(2, "检查 GitHub Actions 配置")

    config_file = Path(".github/workflows/auto-workflow.yml")

    if config_file.exists():
        print_success(f"配置文件已存在: {config_file}")
        return True
    else:
        print_error(f"配置文件不存在: {config_file}")
        print_info("需要创建配置文件")
        return False

def check_required_secrets():
    """检查需要的 API Keys"""
    print_step(3, "检查 API Keys 配置")

    secrets = {
        "SNOVIO_API_KEY": "Snov.io API Key",
        "RESEND_API_KEY": "Resend API Key"
    }

    print_info("需要在 GitHub 中配置以下 Secrets:")
    for name, desc in secrets.items():
        print(f"   - {name} ({desc})")

    return secrets.keys()

def generate_quick_start_guide():
    """生成快速启动指南"""
    print_header("📋 GitHub Actions 配置检查结果")

    # 检查 Git 仓库
    is_git_repo, has_remote = check_git_repository()

    # 检查配置文件
    has_config = check_github_actions_config()

    # 检查 Secrets
    required_secrets = check_required_secrets()

    # 生成下一步操作指南
    print_header("🚀 下一步操作指南")

    if not is_git_repo:
        print_info("请先创建 Git 仓库并上传代码到 GitHub")
        print("\n操作步骤：")
        print("1. 访问 https://github.com 创建新仓库")
        print("2. 执行以下命令初始化并上传：")
        print("\n   git init")
        print("   git add .")
        print("   git commit -m '初始提交'")
        print("   git remote add origin https://github.com/YOUR_USERNAME/miga-auto-workflow.git")
        print("   git branch -M main")
        print("   git push -u origin main\n")

    elif is_git_repo and not has_remote:
        print_info("请添加远程仓库并推送代码")
        print("\n操作步骤：")
        print("1. 访问 https://github.com 创建新仓库")
        print("2. 执行以下命令添加远程仓库并推送：")
        print("\n   git remote add origin https://github.com/YOUR_USERNAME/miga-auto-workflow.git")
        print("   git branch -M main")
        print("   git push -u origin main\n")

    elif is_git_repo and has_remote:
        print_success("代码已上传到 GitHub")

        if has_config:
            print_success("GitHub Actions 配置文件已就绪")
            print("\n下一步：配置 GitHub Secrets")
            print("\n操作步骤：")
            print("1. 进入 GitHub 仓库页面")
            print("2. 点击 Settings → Secrets and variables → Actions")
            print("3. 点击 New repository secret")
            print("4. 添加以下 Secrets：")
            for secret in required_secrets:
                print(f"   - {secret}")
            print("\n5. 配置完成后，手动测试运行一次：")
            print("   - 进入 Actions 页面")
            print("   - 点击 'Run workflow'")
            print("   - 等待运行完成并查看日志\n")
        else:
            print_error("GitHub Actions 配置文件缺失")
            print_info("请确保 .github/workflows/auto-workflow.yml 文件存在\n")

    print_header("📖 详细文档")

    print_info("查看完整配置指南：GITHUB_ACTIONS_GUIDE.md")

    print("\n" + "=" * 60)
    print("💡 温馨提示")
    print("=" * 60)
    print("• 配置完成后，工作流将在每天北京时间上午 9 点自动运行")
    print("• 你可以随时手动触发运行（Actions → Run workflow）")
    print("• 完全免费，无需服务器，无需电脑开机")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    generate_quick_start_guide()
