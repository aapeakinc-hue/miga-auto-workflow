#!/usr/bin/env python3
"""
市场研究与数据分析系统
功能：基于海关数据和市场规模进行数据分析
"""
import json
from typing import Dict, List
from datetime import datetime
import sqlite3

class MarketResearch:
    """市场研究与分析"""

    def __init__(self, db_path: str = "market_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化市场数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建市场数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                product_category TEXT NOT NULL,
                import_volume REAL,
                import_value REAL,
                year INTEGER,
                month INTEGER,
                data_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建市场规模表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_size (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                product_category TEXT NOT NULL,
                market_size REAL,
                growth_rate REAL,
                year INTEGER,
                data_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建竞争对手表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                country TEXT NOT NULL,
                market_share REAL,
                revenue REAL,
                product_focus TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def import_customs_data(self, data: List[Dict]) -> int:
        """导入海关数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        inserted_count = 0

        for item in data:
            cursor.execute("""
                INSERT INTO market_data
                (country, product_category, import_volume, import_value, year, month, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("country"),
                item.get("product_category"),
                item.get("import_volume"),
                item.get("import_value"),
                item.get("year"),
                item.get("month"),
                item.get("data_source", "海关数据")
            ))
            inserted_count += 1

        conn.commit()
        conn.close()

        return inserted_count

    def import_market_size_data(self, data: List[Dict]) -> int:
        """导入市场规模数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        inserted_count = 0

        for item in data:
            cursor.execute("""
                INSERT INTO market_size
                (country, product_category, market_size, growth_rate, year, data_source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item.get("country"),
                item.get("product_category"),
                item.get("market_size"),
                item.get("growth_rate"),
                item.get("year"),
                item.get("data_source", "市场调研")
            ))
            inserted_count += 1

        conn.commit()
        conn.close()

        return inserted_count

    def get_market_potential(self, country: str, year: int = None) -> Dict:
        """获取市场潜力分析"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if year:
            cursor.execute("""
                SELECT country, product_category,
                       SUM(import_value) as total_value,
                       AVG(import_value) as avg_value,
                       COUNT(*) as data_points
                FROM market_data
                WHERE country = ? AND year = ?
                GROUP BY country, product_category
            """, (country, year))
        else:
            cursor.execute("""
                SELECT country, product_category,
                       SUM(import_value) as total_value,
                       AVG(import_value) as avg_value,
                       COUNT(*) as data_points,
                       MAX(year) as latest_year
                FROM market_data
                WHERE country = ?
                GROUP BY country, product_category
            """, (country,))

        results = cursor.fetchall()
        conn.close()

        if not results:
            return {
                "country": country,
                "potential": "low",
                "total_import": 0,
                "avg_monthly": 0,
                "recommendation": "数据不足，建议进一步调研"
            }

        total_import = sum([r[2] for r in results])
        avg_monthly = sum([r[3] for r in results]) / len(results)

        # 市场潜力评估
        if total_import > 10000000:  # 1000万美元以上
            potential = "high"
            recommendation = "高潜力市场，优先开发"
        elif total_import > 5000000:  # 500万美元以上
            potential = "medium"
            recommendation = "中等潜力市场，重点跟进"
        else:
            potential = "low"
            recommendation = "低潜力市场，观察为主"

        return {
            "country": country,
            "potential": potential,
            "total_import": total_import,
            "avg_monthly": avg_monthly,
            "recommendation": recommendation,
            "details": [
                {
                    "product_category": r[1],
                    "total_value": r[2],
                    "avg_value": r[3]
                }
                for r in results
            ]
        }

    def get_market_growth_rate(self, country: str) -> float:
        """获取市场增长率"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT year, SUM(import_value) as total_value
            FROM market_data
            WHERE country = ?
            GROUP BY year
            ORDER BY year DESC
            LIMIT 3
        """, (country,))

        results = cursor.fetchall()
        conn.close()

        if len(results) < 2:
            return 0.0

        # 计算年增长率
        current_year_value = results[0][1]
        previous_year_value = results[1][1]

        if previous_year_value == 0:
            return 0.0

        growth_rate = ((current_year_value - previous_year_value) / previous_year_value) * 100

        return round(growth_rate, 2)

    def get_competitive_landscape(self, country: str) -> List[Dict]:
        """获取竞争格局"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT company_name, country, market_share, revenue, product_focus
            FROM competitors
            WHERE country = ?
            ORDER BY market_share DESC
        """, (country,))

        results = cursor.fetchall()
        conn.close()

        return [
            {
                "company_name": r[0],
                "country": r[1],
                "market_share": r[2],
                "revenue": r[3],
                "product_focus": r[4]
            }
            for r in results
        ]

    def generate_market_report(self, country: str) -> Dict:
        """生成市场分析报告"""
        market_potential = self.get_market_potential(country)
        growth_rate = self.get_market_growth_rate(country)
        competitors = self.get_competitive_landscape(country)

        # 市场规模估算
        estimated_market_size = market_potential.get("total_import", 0) * 2  # 假设市场规模是进口额的2倍

        # 市场机会评估
        if growth_rate > 10:
            opportunity_level = "high"
            opportunity_desc = "高增长市场，机会巨大"
        elif growth_rate > 5:
            opportunity_level = "medium"
            opportunity_desc = "稳定增长市场，机会良好"
        elif growth_rate > 0:
            opportunity_level = "low"
            opportunity_desc = "缓慢增长市场，机会有限"
        else:
            opportunity_level = "negative"
            opportunity_desc = "市场萎缩，谨慎进入"

        return {
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "country": country,
            "market_potential": market_potential,
            "growth_rate": growth_rate,
            "estimated_market_size": estimated_market_size,
            "opportunity_level": opportunity_level,
            "opportunity_description": opportunity_desc,
            "competitors": competitors,
            "recommendations": self._generate_recommendations(market_potential, growth_rate)
        }

    def _generate_recommendations(self, market_potential: Dict, growth_rate: float) -> List[str]:
        """生成市场建议"""
        recommendations = []

        potential = market_potential.get("potential", "low")

        # 基于市场潜力的建议
        if potential == "high":
            recommendations.append("该市场潜力巨大，建议优先投入资源开发")
            recommendations.append("考虑设立本地办事处或寻找本地合作伙伴")
            recommendations.append("提供有竞争力的定价和付款条件")
        elif potential == "medium":
            recommendations.append("该市场有一定潜力，建议稳步开发")
            recommendations.append("重点关注产品质量和服务")
            recommendations.append("建立品牌知名度")
        else:
            recommendations.append("该市场潜力较低，建议谨慎进入")
            recommendations.append("可以尝试小规模试销")
            recommendations.append("持续观察市场动态")

        # 基于增长率的建议
        if growth_rate > 10:
            recommendations.append(f"市场年增长率{growth_rate}%，处于高速增长期，抓住机会")
        elif growth_rate > 5:
            recommendations.append(f"市场年增长率{growth_rate}%，增长稳定，适合长期布局")
        elif growth_rate > 0:
            recommendations.append(f"市场年增长率{growth_rate}%，增长缓慢，需差异化竞争")
        else:
            recommendations.append(f"市场年增长率{growth_rate}%，市场萎缩，需谨慎评估")

        return recommendations

def load_sample_market_data():
    """加载示例市场数据"""
    # 模拟海关数据
    customs_data = [
        {
            "country": "USA",
            "product_category": "水晶烛台",
            "import_volume": 50000,
            "import_value": 5000000,
            "year": 2025,
            "month": 1,
            "data_source": "海关数据"
        },
        {
            "country": "USA",
            "product_category": "水晶工艺品",
            "import_volume": 30000,
            "import_value": 3000000,
            "year": 2025,
            "month": 1,
            "data_source": "海关数据"
        },
        {
            "country": "UK",
            "product_category": "水晶烛台",
            "import_volume": 20000,
            "import_value": 2000000,
            "year": 2025,
            "month": 1,
            "data_source": "海关数据"
        },
        {
            "country": "Germany",
            "product_category": "水晶工艺品",
            "import_volume": 15000,
            "import_value": 1500000,
            "year": 2025,
            "month": 1,
            "data_source": "海关数据"
        },
        {
            "country": "UAE",
            "product_category": "水晶烛台",
            "import_volume": 10000,
            "import_value": 1000000,
            "year": 2025,
            "month": 1,
            "data_source": "海关数据"
        }
    ]

    # 模拟市场规模数据
    market_size_data = [
        {
            "country": "USA",
            "product_category": "水晶烛台",
            "market_size": 50000000,
            "growth_rate": 8.5,
            "year": 2025,
            "data_source": "市场调研"
        },
        {
            "country": "UK",
            "product_category": "水晶烛台",
            "market_size": 15000000,
            "growth_rate": 6.2,
            "year": 2025,
            "data_source": "市场调研"
        },
        {
            "country": "Germany",
            "product_category": "水晶工艺品",
            "market_size": 20000000,
            "growth_rate": 4.5,
            "year": 2025,
            "data_source": "市场调研"
        },
        {
            "country": "UAE",
            "product_category": "水晶烛台",
            "market_size": 8000000,
            "growth_rate": 12.0,
            "year": 2025,
            "data_source": "市场调研"
        },
        {
            "country": "Japan",
            "product_category": "水晶工艺品",
            "market_size": 12000000,
            "growth_rate": 3.8,
            "year": 2025,
            "data_source": "市场调研"
        }
    ]

    return customs_data, market_size_data

if __name__ == "__main__":
    # 初始化市场研究系统
    market = MarketResearch()

    # 加载示例数据
    customs_data, market_size_data = load_sample_market_data()

    # 导入数据
    market.import_customs_data(customs_data)
    market.import_market_size_data(market_size_data)

    # 生成市场报告
    countries = ["USA", "UK", "Germany", "UAE", "Japan"]

    print("=" * 80)
    print("市场分析报告")
    print("=" * 80)

    for country in countries:
        report = market.generate_market_report(country)

        print(f"\n--- {country} 市场分析 ---")
        print(f"市场潜力: {report['market_potential']['potential']}")
        print(f"市场增长率: {report['growth_rate']}%")
        print(f"预估市场规模: ${report['estimated_market_size']:,.0f}")
        print(f"机会等级: {report['opportunity_level']}")
        print(f"机会描述: {report['opportunity_description']}")
        print(f"\n建议:")
        for rec in report['recommendations']:
            print(f"  • {rec}")

    print("\n" + "=" * 80)
