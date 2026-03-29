"""
快速设置自动化工作流
"""
import os
import sys

def setup_automation():
    """设置自动化环境"""
    print("🚀 外贸客户开发工作流 - 自动化设置向导")
    print("=" * 50)

    # 1. 创建日志目录
    print("\n📁 创建日志目录...")
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"✅ 创建目录: {logs_dir}")
    else:
        print(f"✅ 目录已存在: {logs_dir}")

    # 2. 检查自动化脚本
    auto_script = "src/auto_workflow.py"
    if os.path.exists(auto_script):
        print(f"✅ 自动化脚本已存在: {auto_script}")
    else:
        print(f"❌ 自动化脚本不存在: {auto_script}")
        return False

    # 3. 初始化发送历史
    sent_emails_file = "logs/sent_emails.json"
    if not os.path.exists(sent_emails_file):
        import json
        with open(sent_emails_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f"✅ 初始化发送历史: {sent_emails_file}")
    else:
        print(f"✅ 发送历史已存在: {sent_emails_file}")

    # 4. 显示配置选项
    print("\n" + "=" * 50)
    print("🔧 自动化配置选项：")
    print("=" * 50)

    print("\n1️⃣  Cron 定时任务（推荐）")
    print("   适用于：有服务器（Linux/Mac/Windows）")
    print("   优点：灵活、免费、完全可控")

    print("\n2️⃣  Cloudflare Cron")
    print("   适用于：使用 Cloudflare")
    print("   优点：免费、云端运行")

    print("\n3️⃣  GitHub Actions")
    print("   适用于：代码托管在 GitHub")
    print("   优点：免费、云端运行")

    print("\n4️⃣  手动运行（测试）")
    print("   适用于：临时测试")

    # 5. 生成 Cron 命令
    print("\n" + "=" * 50)
    print("📋 Cron 命令示例：")
    print("=" * 50)

    project_path = os.getcwd()

    print(f"\n项目路径: {project_path}")
    print(f"\n每天上午 9 点运行：")
    print(f"0 9 * * * cd {project_path} && python src/auto_workflow.py >> logs/cron.log 2>&1")

    print(f"\n每天上午 9 点和下午 3 点运行：")
    print(f"0 9,15 * * * cd {project_path} && python src/auto_workflow.py >> logs/cron.log 2>&1")

    # 6. 测试运行
    print("\n" + "=" * 50)
    print("🧪 是否现在测试运行自动化脚本？")
    print("=" * 50)

    choice = input("是否测试？(y/n): ").strip().lower()

    if choice == 'y':
        print("\n⏳ 正在测试运行...")
        os.system("python src/auto_workflow.py")
    else:
        print("\n⏭️  跳过测试")

    # 7. 显示下一步
    print("\n" + "=" * 50)
    print("📖 下一步：")
    print("=" * 50)

    print("\n1. 查看 AUTOMATION_GUIDE.md 了解详细配置")
    print("2. 选择自动化方案并配置")
    print("3. 定期查看日志目录：logs/")
    print("4. 监控 Resend 发送记录")

    print("\n" + "=" * 50)
    print("✅ 自动化设置完成！")
    print("=" * 50)

    return True

if __name__ == "__main__":
    success = setup_automation()
    sys.exit(0 if success else 1)
