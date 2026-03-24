"""
A/B测试系统
用于测试不同关键词、邮件模板的效果
"""
import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ABTestManager:
    """A/B测试管理器"""

    def __init__(self, test_file: str = "logs/ab_tests.json"):
        self.test_file = test_file
        self.load_tests()

    def load_tests(self):
        """加载测试配置"""
        try:
            if os.path.exists(self.test_file):
                with open(self.test_file, 'r', encoding='utf-8') as f:
                    self.tests = json.load(f)
            else:
                self.tests = {
                    'keyword_tests': {},
                    'email_template_tests': {},
                    'active_tests': []
                }
        except Exception as e:
            logger.error(f"加载测试配置失败: {e}")
            self.tests = {}

    def save_tests(self):
        """保存测试配置"""
        try:
            os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
            with open(self.test_file, 'w', encoding='utf-8') as f:
                json.dump(self.tests, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存测试配置失败: {e}")

    def create_keyword_test(self, test_name: str, variants: List[str]) -> str:
        """创建关键词A/B测试"""
        test_id = f"kw_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.tests['keyword_tests'][test_id] = {
            'name': test_name,
            'variants': variants,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'results': {variant: [] for variant in variants}
        }

        self.tests['active_tests'].append(test_id)
        self.save_tests()

        logger.info(f"✅ 创建关键词测试: {test_name}")
        return test_id

    def create_email_template_test(self, test_name: str, templates: List[Dict]) -> str:
        """创建邮件模板A/B测试"""
        test_id = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.tests['email_template_tests'][test_id] = {
            'name': test_name,
            'templates': templates,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'results': {i: [] for i in range(len(templates))}
        }

        self.tests['active_tests'].append(test_id)
        self.save_tests()

        logger.info(f"✅ 创建邮件模板测试: {test_name}")
        return test_id

    def assign_variant(self, test_id: str) -> str:
        """为当前运行分配测试变体（随机分配）"""
        # 检查是否是关键词测试
        if test_id in self.tests.get('keyword_tests', {}):
            test = self.tests['keyword_tests'][test_id]
            variants = test['variants']
            selected = random.choice(variants)
            logger.info(f"🎲 关键词测试 {test_id} 选择变体: {selected}")
            return selected

        # 检查是否是邮件模板测试
        if test_id in self.tests.get('email_template_tests', {}):
            test = self.tests['email_template_tests'][test_id]
            templates = test['templates']
            selected_idx = random.randint(0, len(templates) - 1)
            logger.info(f"🎲 邮件模板测试 {test_id} 选择变体: {selected_idx}")
            return str(selected_idx)

        logger.warning(f"⚠️ 未找到测试: {test_id}")
        return None

    def record_result(self, test_id: str, variant: str, result: Dict[str, Any]):
        """记录测试结果"""
        # 检查是否是关键词测试
        if test_id in self.tests.get('keyword_tests', {}):
            if variant in self.tests['keyword_tests'][test_id]['results']:
                self.tests['keyword_tests'][test_id]['results'][variant].append({
                    'timestamp': datetime.now().isoformat(),
                    **result
                })
                self.save_tests()

        # 检查是否是邮件模板测试
        if test_id in self.tests.get('email_template_tests', {}):
            variant_idx = int(variant)
            if variant_idx in self.tests['email_template_tests'][test_id]['results']:
                self.tests['email_template_tests'][test_id]['results'][variant_idx].append({
                    'timestamp': datetime.now().isoformat(),
                    **result
                })
                self.save_tests()

    def analyze_test(self, test_id: str) -> Dict[str, Any]:
        """分析测试结果"""
        # 分析关键词测试
        if test_id in self.tests.get('keyword_tests', {}):
            test = self.tests['keyword_tests'][test_id]
            results = test['results']

            variant_stats = []
            for variant, result_list in results.items():
                if not result_list:
                    continue

                total_emails = len(result_list)
                responses = sum(1 for r in result_list if r.get('response_received', False))
                response_rate = (responses / total_emails * 100) if total_emails > 0 else 0

                variant_stats.append({
                    'variant': variant,
                    'total_emails': total_emails,
                    'responses': responses,
                    'response_rate': response_rate
                })

            # 找出最佳变体
            best_variant = max(variant_stats, key=lambda x: x['response_rate']) if variant_stats else None

            return {
                'test_id': test_id,
                'test_name': test['name'],
                'type': 'keyword',
                'variant_stats': variant_stats,
                'best_variant': best_variant,
                'created_at': test['created_at'],
                'status': test['status']
            }

        # 分析邮件模板测试
        if test_id in self.tests.get('email_template_tests', {}):
            test = self.tests['email_template_tests'][test_id]
            results = test['results']

            variant_stats = []
            for idx, result_list in results.items():
                if not result_list:
                    continue

                total_emails = len(result_list)
                responses = sum(1 for r in result_list if r.get('response_received', False))
                response_rate = (responses / total_emails * 100) if total_emails > 0 else 0

                variant_stats.append({
                    'variant': idx,
                    'template_name': test['templates'][idx].get('name', f'Template {idx}'),
                    'total_emails': total_emails,
                    'responses': responses,
                    'response_rate': response_rate
                })

            best_variant = max(variant_stats, key=lambda x: x['response_rate']) if variant_stats else None

            return {
                'test_id': test_id,
                'test_name': test['name'],
                'type': 'email_template',
                'variant_stats': variant_stats,
                'best_variant': best_variant,
                'created_at': test['created_at'],
                'status': test['status']
            }

        return {}


class OptimizationEngine:
    """优化引擎 - 基于数据自动优化"""

    def __init__(self):
        self.ab_manager = ABTestManager()

    def optimize_keywords(self, top_keywords: int = 10) -> List[str]:
        """优化关键词选择"""
        # 从性能数据中找出最佳关键词
        top_keywords_data = self.ab_manager.tests.get('keyword_performance', {})

        if not top_keywords_data:
            # 如果没有数据，使用默认关键词
            return [
                "crystal candle holders wholesale USA",
                "crystal candelabra importers Europe",
                "luxury crystal decor buyers",
                "home decor crystal suppliers",
                "gift shops crystal wholesalers"
            ]

        # 按回复率排序
        sorted_keywords = sorted(
            top_keywords_data.items(),
            key=lambda x: x[1].get('response_rate', 0),
            reverse=True
        )

        return [kw[0] for kw in sorted_keywords[:top_keywords]]

    def suggest_new_keywords(self, existing_keywords: List[str], count: int = 5) -> List[str]:
        """建议新的关键词"""
        # 基于现有关键词生成新的变体
        base_keywords = [
            "crystal candle holders",
            "crystal candelabra",
            "luxury crystal decor",
            "home decor crystal",
            "gift shops crystal"
        ]

        markets = [
            "wholesale USA",
            "importers Europe",
            "buyers UK",
            "distributors Germany",
            "suppliers France",
            "wholesalers Canada"
        ]

        new_keywords = []
        for base in base_keywords:
            for market in markets:
                new_keyword = f"{base} {market}"
                if new_keyword not in existing_keywords:
                    new_keywords.append(new_keyword)
                    if len(new_keywords) >= count:
                        return new_keywords

        return new_keywords

    def optimize_email_template(self, template_type: str = "sales") -> Dict[str, Any]:
        """优化邮件模板"""
        # 这里可以根据回复率分析哪个模板效果最好
        # 然后生成新的模板变体

        templates = {
            "sales": [
                {
                    "name": "标准销售模板",
                    "subject": "Crystal Candle Holders Wholesale Opportunity",
                    "body": "Dear {{company}},\n\nI hope this email finds you well..."
                },
                {
                    "name": "简洁模板",
                    "subject": "Quick Inquiry: Crystal Products",
                    "body": "Hi {{company}},\n\nWe're manufacturers of..."
                },
                {
                    "name": "价值导向模板",
                    "subject": "Premium Quality Crystal - Best Prices",
                    "body": "Hello {{company}},\n\nLooking for premium crystal products?..."
                }
            ]
        }

        return templates.get(template_type, templates["sales"])

    def generate_optimization_plan(self) -> Dict[str, Any]:
        """生成优化计划"""
        plan = {
            'timestamp': datetime.now().isoformat(),
            'keyword_optimization': {},
            'email_template_optimization': {},
            'action_items': []
        }

        # 关键词优化
        top_keywords = self.optimize_keywords()
        new_keywords = self.suggest_new_keywords(top_keywords)

        plan['keyword_optimization'] = {
            'current_top_keywords': top_keywords,
            'suggested_new_keywords': new_keywords,
            'recommendation': f"建议测试 {len(new_keywords)} 个新关键词"
        }

        # 邮件模板优化
        templates = self.optimize_email_template()
        plan['email_template_optimization'] = {
            'available_templates': [t['name'] for t in templates],
            'recommendation': '建议创建A/B测试，比较不同邮件模板的效果'
        }

        # 行动项
        plan['action_items'] = [
            {
                'priority': 'high',
                'action': '创建关键词A/B测试',
                'description': f'测试 {len(new_keywords)} 个新关键词的效果'
            },
            {
                'priority': 'medium',
                'action': '创建邮件模板A/B测试',
                'description': '比较不同邮件模板的回复率'
            },
            {
                'priority': 'low',
                'action': '分析客户细分',
                'description': '按地区、公司类型等维度分析客户响应'
            }
        ]

        return plan


if __name__ == "__main__":
    logger.info("🧪 启动A/B测试系统")

    # 创建A/B测试管理器
    ab_manager = ABTestManager()

    # 示例：创建关键词测试
    test_id = ab_manager.create_keyword_test(
        "美国市场关键词测试",
        [
            "crystal candle holders wholesale USA",
            "luxury crystal decor wholesalers America",
            "crystal home decor buyers USA"
        ]
    )

    # 示例：创建邮件模板测试
    template_test_id = ab_manager.create_email_template_test(
        "邮件模板测试",
        [
            {"name": "模板A", "subject": "Opportunity", "body": "..."},
            {"name": "模板B", "subject": "Inquiry", "body": "..."}
        ]
    )

    logger.info(f"✅ 关键词测试ID: {test_id}")
    logger.info(f"✅ 邮件模板测试ID: {template_test_id}")

    # 生成优化计划
    optimizer = OptimizationEngine()
    plan = optimizer.generate_optimization_plan()
    logger.info(f"📋 优化计划: {json.dumps(plan, indent=2, ensure_ascii=False)}")

    logger.info("✅ A/B测试系统已启动")
