# MIGAC 产品目录使用指南

## 📚 目录说明

本产品目录包含以下文件：

1. **MIGAC_PRODUCT_CATALOG_V2.json** - 完整的产品目录 JSON 数据
2. **MIGAC_PRODUCT_CATALOG_V2.html** - 可视化产品目录网页
3. **MIGAC_MODEL_SYSTEM_GUIDE.md** - 详细的新型号系统说明文档
4. **MIGAC_QUICK_REFERENCE.md** - 快速参考卡
5. **本文件** - 使用指南

---

## 🚀 快速开始

### 1. 查看 HTML 版本目录

直接在浏览器中打开 `MIGAC_PRODUCT_CATALOG_V2.html` 文件，即可查看完整的可视化产品目录。

**特点**:
- 简洁大方的设计
- 响应式布局，支持移动端
- 产品分类清晰
- Best Seller 和 Featured 标签高亮

### 2. 阅读快速参考卡

打开 `MIGAC_QUICK_REFERENCE.md` 文件，快速了解：
- 型号命名规则
- 产品系列代码
- 颜色代码
- 畅销产品列表

### 3. 深入了解新型号系统

打开 `MIGAC_MODEL_SYSTEM_GUIDE.md` 文件，详细了解：
- 新型号系统的设计理念
- 完整的旧型号到新型号转换表
- 产品统计信息
- 应用场景说明

### 4. 程序化访问产品数据

如果您需要通过编程方式访问产品数据，可以使用 JSON 文件。

---

## 💻 编程访问 JSON 数据

### Python 示例

```python
import json

# 读取 JSON 文件
with open('MIGAC_PRODUCT_CATALOG_V2.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# 访问品牌信息
print(f"品牌: {catalog['brand']['name']}")
print(f"公司: {catalog['brand']['company']}")
print(f"网站: {catalog['brand']['website']}")

# 访问型号系统
model_system = catalog['model_system']
print(f"\n型号规则: {model_system['naming_convention']}")
print(f"示例: {model_system['example']}")

# 遍历所有产品系列
for series in catalog['product_series']:
    print(f"\n{series['icon']} {series['series_name']} ({series['series_code']})")
    print(f"产品数量: {len(series['products'])}")
    
    # 遍历该系列的所有产品
    for product in series['products']:
        print(f"  • {product['new_model']} - {product['name']}")
        if product.get('best_seller'):
            print(f"    🔥 Best Seller")
        if product.get('featured'):
            print(f"    ⭐ Featured")

# 获取所有畅销产品
best_sellers = []
for series in catalog['product_series']:
    for product in series['products']:
        if product.get('best_seller'):
            best_sellers.append(product)

print(f"\n🔥 畅销产品 ({len(best_sellers)} 个):")
for product in best_sellers:
    print(f"  • {product['new_model']} - {product['name']}")

# 按系列筛选产品
def get_products_by_series(series_code):
    for series in catalog['product_series']:
        if series['series_code'] == series_code:
            return series['products']
    return []

# 示例：获取所有水晶烛台产品
candelabra_products = get_products_by_series('CA')
print(f"\n水晶烛台产品 ({len(candelabra_products)} 个):")
for product in candelabra_products:
    print(f"  • {product['new_model']} - {product['name']}")
```

### JavaScript 示例

```javascript
// 读取 JSON 文件
const catalog = require('./MIGAC_PRODUCT_CATALOG_V2.json');

// 访问品牌信息
console.log(`品牌: ${catalog.brand.name}`);
console.log(`公司: ${catalog.brand.company}`);
console.log(`网站: ${catalog.brand.website}`);

// 访问型号系统
console.log(`\n型号规则: ${catalog.model_system.naming_convention}`);
console.log(`示例: ${catalog.model_system.example}`);

// 遍历所有产品系列
catalog.product_series.forEach(series => {
    console.log(`\n${series.icon} ${series.seriesName} (${series.seriesCode})`);
    console.log(`产品数量: ${series.products.length}`);
    
    // 遍历该系列的所有产品
    series.products.forEach(product => {
        console.log(`  • ${product.newModel} - ${product.name}`);
        if (product.bestSeller) {
            console.log(`    🔥 Best Seller`);
        }
        if (product.featured) {
            console.log(`    ⭐ Featured`);
        }
    });
});

// 获取所有畅销产品
const bestSellers = [];
catalog.product_series.forEach(series => {
    series.products.forEach(product => {
        if (product.bestSeller) {
            bestSellers.push(product);
        }
    });
});

console.log(`\n🔥 畅销产品 (${bestSellers.length} 个):`);
bestSellers.forEach(product => {
    console.log(`  • ${product.newModel} - ${product.name}`);
});

// 按系列筛选产品
function getProductsBySeries(seriesCode) {
    const series = catalog.product_series.find(s => s.seriesCode === seriesCode);
    return series ? series.products : [];
}

// 示例：获取所有水晶烛台产品
const candelabraProducts = getProductsBySeries('CA');
console.log(`\n水晶烛台产品 (${candelabraProducts.length} 个):`);
candelabraProducts.forEach(product => {
    console.log(`  • ${product.newModel} - ${product.name}`);
});
```

---

## 🔍 产品查询功能

### 按型号查询

```python
def find_product_by_model(model_number):
    """根据型号查询产品"""
    for series in catalog['product_series']:
        for product in series['products']:
            if product['new_model'] == model_number:
                return product
    return None

# 示例
product = find_product_by_model('MG-CA-001-083-N')
if product:
    print(f"产品名称: {product['name']}")
    print(f"价格范围: {product['price_range']}")
    print(f"MOQ: {product['moq']}")
```

### 按名称搜索

```python
def search_products(keyword):
    """根据关键词搜索产品"""
    results = []
    keyword = keyword.lower()
    
    for series in catalog['product_series']:
        for product in series['products']:
            if (keyword in product['name'].lower() or 
                keyword in product['name_cn'] or 
                keyword in product['new_model'].lower()):
                results.append(product)
    
    return results

# 示例：搜索所有"五臂"产品
results = search_products('5-arm')
print(f"找到 {len(results)} 个相关产品")
for product in results:
    print(f"  • {product['new_model']} - {product['name']}")
```

### 按价格范围筛选

```python
def filter_by_price(min_price, max_price):
    """按价格范围筛选产品"""
    results = []
    
    for series in catalog['product_series']:
        for product in series['products']:
            price_range = product['price_range']
            # 解析价格范围，例如 "$15-25"
            prices = [int(p.replace('$', '')) for p in price_range.split('-')]
            avg_price = sum(prices) / len(prices)
            
            if min_price <= avg_price <= max_price:
                results.append(product)
    
    return results

# 示例：筛选价格在 $20-40 之间的产品
results = filter_by_price(20, 40)
print(f"价格在 $20-40 之间的产品 ({len(results)} 个):")
for product in results:
    print(f"  • {product['new_model']} - {product['name']} ({product['price_range']})")
```

### 按尺寸筛选

```python
def filter_by_height(min_height, max_height):
    """按高度筛选产品（仅适用于烛台、花架等）"""
    results = []
    
    for series in catalog['product_series']:
        for product in series['products']:
            if 'height' in product:
                height = product['height']
                if min_height <= height <= max_height:
                    results.append(product)
    
    return results

# 示例：筛选高度在 80-120cm 之间的产品
results = filter_by_height(80, 120)
print(f"高度在 80-120cm 之间的产品 ({len(results)} 个):")
for product in results:
    print(f"  • {product['new_model']} - {product['name']} ({product['height']}cm)")
```

---

## 📊 数据统计

```python
def get_statistics():
    """获取产品目录统计信息"""
    stats = {
        'total_products': 0,
        'total_series': len(catalog['product_series']),
        'best_sellers': 0,
        'featured': 0,
        'series_breakdown': {}
    }
    
    for series in catalog['product_series']:
        series_stats = {
            'total': len(series['products']),
            'best_sellers': 0,
            'featured': 0
        }
        
        for product in series['products']:
            stats['total_products'] += 1
            if product.get('best_seller'):
                stats['best_sellers'] += 1
                series_stats['best_sellers'] += 1
            if product.get('featured'):
                stats['featured'] += 1
                series_stats['featured'] += 1
        
        stats['series_breakdown'][series['series_code']] = series_stats
    
    return stats

# 获取统计信息
stats = get_statistics()

print("📊 产品目录统计")
print(f"总产品数: {stats['total_products']}")
print(f"总系列数: {stats['total_series']}")
print(f"畅销产品: {stats['best_sellers']}")
print(f"特色产品: {stats['featured']}")
print("\n按系列统计:")
for code, data in stats['series_breakdown'].items():
    print(f"  {code}: {data['total']} 个产品 ({data['best_sellers']} 畅销, {data['featured']} 特色)")
```

---

## 🌐 在网站中使用

### React 组件示例

```jsx
import React, { useState, useEffect } from 'react';
import catalog from './MIGAC_PRODUCT_CATALOG_V2.json';

function ProductCatalog() {
  const [selectedSeries, setSelectedSeries] = useState(null);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    if (selectedSeries) {
      const series = catalog.product_series.find(s => s.seriesCode === selectedSeries);
      setProducts(series ? series.products : []);
    }
  }, [selectedSeries]);

  return (
    <div className="catalog">
      <h1>{catalog.brand.name} Product Catalog</h1>
      
      {/* 系列选择器 */}
      <div className="series-selector">
        {catalog.product_series.map(series => (
          <button 
            key={series.seriesCode}
            onClick={() => setSelectedSeries(series.seriesCode)}
            className={selectedSeries === series.seriesCode ? 'active' : ''}
          >
            {series.icon} {series.seriesName}
          </button>
        ))}
      </div>

      {/* 产品列表 */}
      <div className="product-list">
        {products.map(product => (
          <div key={product.newModel} className="product-card">
            <div className="model-number">{product.newModel}</div>
            <h3>{product.name}</h3>
            <p className="chinese-name">{product.name_cn}</p>
            <div className="badges">
              {product.bestSeller && <span className="badge best-seller">Best Seller</span>}
              {product.featured && <span className="badge featured">Featured</span>}
            </div>
            <div className="price">{product.priceRange}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductCatalog;
```

---

## 📤 导出数据

### 导出为 CSV

```python
import csv

def export_to_csv(filename='products.csv'):
    """导出产品数据为 CSV 文件"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # 写入表头
        writer.writerow([
            'New Model', 'Old Model', 'Name', 'Name CN', 
            'Series', 'Price Range', 'MOQ', 'Lead Time',
            'Best Seller', 'Featured'
        ])
        
        # 写入数据
        for series in catalog['product_series']:
            for product in series['products']:
                writer.writerow([
                    product['new_model'],
                    product.get('old_model', ''),
                    product['name'],
                    product['name_cn'],
                    series['series_code'],
                    product['price_range'],
                    product['moq'],
                    product['lead_time'],
                    'Yes' if product.get('best_seller') else 'No',
                    'Yes' if product.get('featured') else 'No'
                ])
    
    print(f"✅ 已导出到 {filename}")

export_to_csv()
```

### 导出为 Excel

```python
import pandas as pd

def export_to_excel(filename='products.xlsx'):
    """导出产品数据为 Excel 文件"""
    data = []
    
    for series in catalog['product_series']:
        for product in series['products']:
            data.append({
                '型号': product['new_model'],
                '旧型号': product.get('old_model', ''),
                '产品名称': product['name'],
                '中文名称': product['name_cn'],
                '系列': series['series_code'],
                '系列名称': series['series_name'],
                '价格范围': product['price_range'],
                'MOQ': product['moq'],
                '交期': product['lead_time'],
                '畅销款': '是' if product.get('best_seller') else '否',
                '特色款': '是' if product.get('featured') else '否'
            })
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"✅ 已导出到 {filename}")

export_to_excel()
```

---

## 🔧 自定义配置

### 添加新产品

```python
def add_product(series_code, product_data):
    """向指定系列添加新产品"""
    for series in catalog['product_series']:
        if series['series_code'] == series_code:
            series['products'].append(product_data)
            print(f"✅ 已添加产品: {product_data['new_model']}")
            return True
    print(f"❌ 未找到系列: {series_code}")
    return False

# 示例：添加新产品
new_product = {
    "new_model": "MG-CA-016-100-G",
    "old_model": "NEW001",
    "name": "Gold 5-Arm Candelabra",
    "name_cn": "金色五臂烛台",
    "dimensions": "48×100cm",
    "arms": 5,
    "height": 100,
    "width": 48,
    "material": "K9 Crystal + Metal Base",
    "moq": 10,
    "lead_time": "7-10 days",
    "price_range": "$25-35",
    "best_seller": False,
    "featured": False
}

add_product('CA', new_product)
```

### 更新产品信息

```python
def update_product(model_number, updates):
    """更新指定型号的产品信息"""
    for series in catalog['product_series']:
        for product in series['products']:
            if product['new_model'] == model_number:
                product.update(updates)
                print(f"✅ 已更新产品: {model_number}")
                return True
    print(f"❌ 未找到产品: {model_number}")
    return False

# 示例：更新价格
update_product('MG-CA-001-083-N', {
    'price_range': '$18-28',
    'best_seller': True
})
```

---

## 📞 技术支持

如果您在使用过程中遇到任何问题，请联系：

- **技术支持**: support@miga.cc
- **销售咨询**: sales@miga.cc

---

## 📅 更新日志

### v2.0 (2026-03-30)
- ✨ 推出全新型号系统
- ✨ 创建 4 个产品系列，26 个产品
- ✨ 添加 Best Seller 和 Featured 标签
- 📚 提供完整的使用文档
- 💻 提供 JSON 数据文件

---

**使用指南 v2.0 | 最后更新: 2026-03-30**
