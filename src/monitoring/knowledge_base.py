"""
智能知识库系统
记录客户信息、邮件模板、关键词等，支持智能搜索和推荐
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeBase:
    """知识库系统"""

    def __init__(self, kb_file: str = "logs/knowledge_base.json"):
        self.kb_file = kb_file
        self.load_knowledge()

    def load_knowledge(self):
        """加载知识库"""
        try:
            if os.path.exists(self.kb_file):
                with open(self.kb_file, 'r', encoding='utf-8') as f:
                    self.knowledge = json.load(f)
            else:
                self.knowledge = {
                    'customers': [],
                    'keywords': [],
                    'email_templates': [],
                    'success_stories': [],
                    'lessons_learned': []
                }
        except Exception as e:
            logger.error(f"加载知识库失败: {e}")
            self.knowledge = {}

    def save_knowledge(self):
        """保存知识库"""
        try:
            os.makedirs(os.path.dirname(self.kb_file), exist_ok=True)
            with open(self.kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存知识库失败: {e}")

    def add_customer(self, customer: Dict[str, Any]):
        """添加客户信息"""
        # 检查客户是否已存在
        existing = next(
            (c for c in self.knowledge['customers'] if c.get('email') == customer.get('email')),
            None
        )

        if existing:
            # 更新现有客户信息
            existing.update({
                'last_contact': datetime.now().isoformat(),
                **customer
            })
            logger.info(f"📝 更新客户信息: {customer.get('email')}")
        else:
            # 添加新客户
            customer['created_at'] = datetime.now().isoformat()
            customer['last_contact'] = datetime.now().isoformat()
            self.knowledge['customers'].append(customer)
            logger.info(f"✅ 添加新客户: {customer.get('email')}")

        self.save_knowledge()

    def update_customer_status(self, email: str, status: str, notes: str = ""):
        """更新客户状态"""
        customer = next(
            (c for c in self.knowledge['customers'] if c.get('email') == email),
            None
        )

        if customer:
            customer['status'] = status
            customer['last_contact'] = datetime.now().isoformat()
            if notes:
                customer['notes'] = customer.get('notes', '') + "\n" + notes
            self.save_knowledge()
            logger.info(f"📝 更新客户状态: {email} -> {status}")
            return True
        else:
            logger.warning(f"⚠️ 未找到客户: {email}")
            return False

    def add_keyword(self, keyword: str, category: str = "general"):
        """添加关键词"""
        existing = next(
            (k for k in self.knowledge['keywords'] if k.get('keyword') == keyword),
            None
        )

        if not existing:
            keyword_data = {
                'keyword': keyword,
                'category': category,
                'created_at': datetime.now().isoformat(),
                'usage_count': 0,
                'success_count': 0
            }
            self.knowledge['keywords'].append(keyword_data)
            logger.info(f"✅ 添加关键词: {keyword}")
            self.save_knowledge()

    def record_keyword_result(self, keyword: str, success: bool):
        """记录关键词使用结果"""
        keyword_data = next(
            (k for k in self.knowledge['keywords'] if k.get('keyword') == keyword),
            None
        )

        if keyword_data:
            keyword_data['usage_count'] += 1
            if success:
                keyword_data['success_count'] += 1
            keyword_data['last_used'] = datetime.now().isoformat()
            self.save_knowledge()

    def add_email_template(self, template: Dict[str, Any]):
        """添加邮件模板"""
        template['created_at'] = datetime.now().isoformat()
        template['usage_count'] = 0
        template['success_count'] = 0
        self.knowledge['email_templates'].append(template)
        logger.info(f"✅ 添加邮件模板: {template.get('name')}")
        self.save_knowledge()

    def record_template_result(self, template_name: str, success: bool):
        """记录邮件模板使用结果"""
        template = next(
            (t for t in self.knowledge['email_templates'] if t.get('name') == template_name),
            None
        )

        if template:
            template['usage_count'] += 1
            if success:
                template['success_count'] += 1
            template['last_used'] = datetime.now().isoformat()
            self.save_knowledge()

    def add_success_story(self, story: Dict[str, Any]):
        """添加成功案例"""
        story['created_at'] = datetime.now().isoformat()
        self.knowledge['success_stories'].append(story)
        logger.info(f"✅ 添加成功案例: {story.get('title')}")
        self.save_knowledge()

    def add_lesson_learned(self, lesson: Dict[str, Any]):
        """添加经验教训"""
        lesson['created_at'] = datetime.now().isoformat()
        self.knowledge['lessons_learned'].append(lesson)
        logger.info(f"✅ 添加经验教训: {lesson.get('title')}")
        self.save_knowledge()

    def search_customers(self, query: str, field: str = None) -> List[Dict[str, Any]]:
        """搜索客户"""
        query = query.lower()
        results = []

        for customer in self.knowledge['customers']:
            # 全字段搜索
            if field is None:
                for key, value in customer.items():
                    if isinstance(value, str) and query in value.lower():
                        results.append(customer)
                        break
            # 指定字段搜索
            else:
                if field in customer and isinstance(customer[field], str):
                    if query in customer[field].lower():
                        results.append(customer)

        return results

    def search_keywords(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """搜索关键词"""
        query = query.lower()
        results = []

        for keyword in self.knowledge['keywords']:
            if query in keyword.get('keyword', '').lower():
                if category is None or keyword.get('category') == category:
                    results.append(keyword)

        return results

    def get_best_keywords(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """获取最佳关键词（按成功率排序）"""
        keywords_with_rate = []

        for kw in self.knowledge['keywords']:
            if kw.get('usage_count', 0) > 0:
                success_rate = (kw.get('success_count', 0) / kw['usage_count'] * 100)
                keywords_with_rate.append({
                    **kw,
                    'success_rate': success_rate
                })

        # 按成功率排序
        keywords_with_rate.sort(key=lambda x: x.get('success_rate', 0), reverse=True)
        return keywords_with_rate[:top_n]

    def get_best_email_templates(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """获取最佳邮件模板（按成功率排序）"""
        templates_with_rate = []

        for template in self.knowledge['email_templates']:
            if template.get('usage_count', 0) > 0:
                success_rate = (template.get('success_count', 0) / template['usage_count'] * 100)
                templates_with_rate.append({
                    **template,
                    'success_rate': success_rate
                })

        templates_with_rate.sort(key=lambda x: x.get('success_rate', 0), reverse=True)
        return templates_with_rate[:top_n]

    def generate_customer_insights(self) -> Dict[str, Any]:
        """生成客户洞察"""
        total_customers = len(self.knowledge['customers'])

        # 按状态统计
        status_counts = {}
        for customer in self.knowledge['customers']:
            status = customer.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        # 按地区统计
        region_counts = {}
        for customer in self.knowledge['customers']:
            region = customer.get('region', 'unknown')
            region_counts[region] = region_counts.get(region, 0) + 1

        # 按行业统计
        industry_counts = {}
        for customer in self.knowledge['customers']:
            industry = customer.get('industry', 'unknown')
            industry_counts[industry] = industry_counts.get(industry, 0) + 1

        return {
            'total_customers': total_customers,
            'status_distribution': status_counts,
            'region_distribution': region_counts,
            'industry_distribution': industry_counts,
            'generated_at': datetime.now().isoformat()
        }

    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """生成推荐建议"""
        recommendations = []

        # 基于成功案例生成推荐
        for story in self.knowledge['success_stories']:
            recommendations.append({
                'type': 'success_pattern',
                'title': f"复刻成功案例: {story.get('title')}",
                'description': story.get('description', ''),
                'priority': 'high'
            })

        # 基于经验教训生成推荐
        for lesson in self.knowledge['lessons_learned']:
            recommendations.append({
                'type': 'avoid_mistake',
                'title': f"避免问题: {lesson.get('title')}",
                'description': lesson.get('description', ''),
                'priority': 'medium'
            })

        return recommendations


class IntelligentAssistant:
    """智能助手 - 基于知识库提供智能建议"""

    def __init__(self):
        self.kb = KnowledgeBase()

    def suggest_keywords(self, context: Dict[str, Any] = None) -> List[str]:
        """建议关键词"""
        # 获取最佳关键词
        best_keywords = self.kb.get_best_keywords(5)

        if best_keywords:
            return [kw['keyword'] for kw in best_keywords]
        else:
            # 如果没有数据，返回默认建议
            return [
                "crystal candle holders wholesale USA",
                "luxury crystal decor buyers",
                "home decor crystal suppliers"
            ]

    def suggest_email_template(self, customer: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """建议邮件模板"""
        # 根据客户特征选择最佳模板
        best_templates = self.kb.get_best_email_templates(3)

        if best_templates:
            return best_templates[0]
        else:
            return None

    def suggest_next_action(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """建议下一步行动"""
        status = customer.get('status', 'unknown')

        action_map = {
            'new': {
                'action': 'send_initial_email',
                'description': '发送初始开发邮件',
                'priority': 'high'
            },
            'contacted': {
                'action': 'follow_up',
                'description': '跟进客户（等待回复）',
                'priority': 'medium'
            },
            'interested': {
                'action': 'send_samples',
                'description': '发送样品和详细报价',
                'priority': 'high'
            },
            'negotiating': {
                'action': 'finalize_deal',
                'description': '谈判和成交',
                'priority': 'high'
            }
        }

        return action_map.get(status, {
            'action': 'review',
            'description': '审查客户状态',
            'priority': 'low'
        })

    def analyze_customer_pattern(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """分析客户模式"""
        # 基于知识库中的类似客户生成分析
        similar_customers = self.kb.search_customers(
            customer.get('region', ''),
            'region'
        )

        if similar_customers:
            # 分析类似客户的成功模式
            success_customers = [
                c for c in similar_customers
                if c.get('status') in ['interested', 'negotating', 'won']
            ]

            return {
                'similar_customers': len(similar_customers),
                'success_rate': len(success_customers) / len(similar_customers) * 100,
                'recommendation': '这是一个有潜力的市场' if success_customers else '需要调整策略'
            }
        else:
            return {
                'similar_customers': 0,
                'success_rate': 0,
                'recommendation': '这是新市场，谨慎测试'
            }


if __name__ == "__main__":
    logger.info("🧠 启动智能知识库系统")

    # 创建知识库
    kb = KnowledgeBase()

    # 示例：添加客户
    kb.add_customer({
        'email': 'contact@example.com',
        'company': 'Example Corp',
        'region': 'USA',
        'industry': 'Home Decor',
        'status': 'new'
    })

    # 示例：添加关键词
    kb.add_keyword("crystal candle holders wholesale USA", "USA market")

    # 示例：生成客户洞察
    insights = kb.generate_customer_insights()
    logger.info(f"📊 客户洞察: {json.dumps(insights, indent=2, ensure_ascii=False)}")

    # 示例：智能助手建议
    assistant = IntelligentAssistant()
    keywords = assistant.suggest_keywords()
    logger.info(f"💡 建议关键词: {keywords}")

    logger.info("✅ 智能知识库系统已启动")
