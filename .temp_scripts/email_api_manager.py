"""
邮箱抓取 API 管理器
支持多个 API Key 轮换使用，突破单账户限制
"""
import random
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EmailAPIKey:
    """邮箱 API Key 数据类"""
    name: str  # API 名称
    key: str   # API Key
    requests_used: int = 0  # 已使用次数
    requests_limit: int = 0  # 限制次数
    last_used: Optional[str] = None  # 最后使用时间


class EmailAPIManager:
    """
    邮箱抓取 API 管理器

    功能：
    1. 支持多个 API Key
    2. 自动轮换使用
    3. 记录使用情况
    4. 处理 API 限流
    """

    def __init__(self):
        self.api_keys: List[EmailAPIKey] = []
        self.current_index = 0

    def add_api_key(self, name: str, key: str, limit: int = 50):
        """
        添加 API Key

        Args:
            name: API 名称（如 "snovio_1", "snovio_2"）
            key: API Key
            limit: 请求限制（免费通常 50/月）
        """
        api_key = EmailAPIKey(
            name=name,
            key=key,
            requests_limit=limit
        )
        self.api_keys.append(api_key)
        logger.info(f"✅ 添加 API Key: {name} (限制: {limit})")

    def get_available_key(self) -> Optional[EmailAPIKey]:
        """
        获取可用的 API Key

        策略：
        1. 轮询选择
        2. 避开已达到限制的 Key
        """
        if not self.api_keys:
            logger.warning("⚠️  没有可用的 API Key")
            return None

        # 尝试找到未达限制的 Key
        available_keys = [
            key for key in self.api_keys
            if key.requests_used < key.requests_limit
        ]

        if not available_keys:
            logger.error("❌ 所有 API Key 都已达到限制")
            return None

        # 轮询选择
        selected_key = available_keys[self.current_index % len(available_keys)]
        self.current_index = (self.current_index + 1) % len(available_keys)

        return selected_key

    def mark_used(self, api_key_name: str):
        """标记 API Key 已使用"""
        for key in self.api_keys:
            if key.name == api_key_name:
                key.requests_used += 1
                from datetime import datetime
                key.last_used = datetime.now().isoformat()
                logger.info(f"📊 {api_key_name}: {key.requests_used}/{key.requests_limit}")
                break

    def get_usage_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        stats = {
            "total_keys": len(self.api_keys),
            "total_used": sum(key.requests_used for key in self.api_keys),
            "total_limit": sum(key.requests_limit for key in self.api_keys),
            "details": []
        }

        for key in self.api_keys:
            stats["details"].append({
                "name": key.name,
                "used": key.requests_used,
                "limit": key.requests_limit,
                "remaining": key.requests_limit - key.requests_used,
                "last_used": key.last_used
            })

        return stats

    def reset_usage(self):
        """重置使用计数（每月初调用）"""
        for key in self.api_keys:
            key.requests_used = 0
            key.last_used = None
        logger.info("🔄 所有 API Key 使用计数已重置")


# 全局实例
email_api_manager = EmailAPIManager()


def setup_email_apis():
    """
    设置邮箱抓取 API

    从环境变量读取多个 API Key
    """
    import os

    # Snov.io 多个 Key
    snovio_keys_str = os.getenv("SNOVIO_API_KEYS", "")
    if snovio_keys_str:
        snovio_keys = [key.strip() for key in snovio_keys_str.split(",")]
        for i, key in enumerate(snovio_keys, 1):
            email_api_manager.add_api_key(f"snovio_{i}", key, limit=50)

    # 如果没有环境变量，使用单个 Key（兼容旧版本）
    single_snovio_key = os.getenv("SNOVIO_API_KEY", "")
    if single_snovio_key and not snovio_keys_str:
        email_api_manager.add_api_key("snovio_default", single_snovio_key, limit=50)

    # Hunter.io Key（如果有）
    hunter_key = os.getenv("HUNTER_API_KEY", "")
    if hunter_key:
        email_api_manager.add_api_key("hunter_io", hunter_key, limit=50)

    # Clearbit Key（如果有）
    clearbit_key = os.getenv("CLEARBIT_API_KEY", "")
    if clearbit_key:
        email_api_manager.add_api_key("clearbit", clearbit_key, limit=50)

    logger.info(f"✅ 已配置 {len(email_api_manager.api_keys)} 个邮箱 API Key")


def get_email_api_key() -> Optional[str]:
    """获取可用的 API Key"""
    api_key = email_api_manager.get_available_key()
    if api_key:
        return api_key.key
    return None


def mark_api_key_used(api_key: str):
    """标记 API Key 已使用"""
    for key in email_api_manager.api_keys:
        if key.key == api_key:
            email_api_manager.mark_used(key.name)
            break


if __name__ == "__main__":
    # 测试代码
    setup_email_apis()

    # 打印统计信息
    stats = email_api_manager.get_usage_stats()
    print("\n📊 邮箱 API 使用统计:")
    print(f"总 Key 数: {stats['total_keys']}")
    print(f"总使用: {stats['total_used']}/{stats['total_limit']}")
    print("\n详情:")
    for detail in stats['details']:
        print(f"  {detail['name']}: {detail['used']}/{detail['limit']} (剩余: {detail['remaining']})")

    # 模拟使用
    print("\n🔄 模拟使用:")
    for i in range(10):
        key = get_email_api_key()
        if key:
            print(f"  第 {i+1} 次使用: {key[:10]}...")
            mark_api_key_used(key)
        else:
            print(f"  第 {i+1} 次: ⚠️  无可用 Key")
            break

    # 再次打印统计
    print("\n📊 使用后统计:")
    stats = email_api_manager.get_usage_stats()
    for detail in stats['details']:
        print(f"  {detail['name']}: {detail['used']}/{detail['limit']}")
