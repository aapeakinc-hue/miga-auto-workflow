#!/usr/bin/env python3
"""
Generate keywords for product images using AI vision system
"""

import os
import json
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict

# Product information from HTML
products = [
    {
        "file": "5 arms candelabra.jpg",
        "title": "Large Multi-Arm Crystal Candelabra",
        "description": "Most popular model for weddings and large events",
        "specs": ["Large Size", "Large Multi-Arm Design"]
    },
    {
        "file": "9 arms candelabra.jpg",
        "title": "9-Arm Crystal Candelabra",
        "description": "Elegant centerpiece for luxury events",
        "specs": ["9 Arms", "Medium Size"]
    },
    {
        "file": "9 arms candelabras.jpg",
        "title": "9 Arms Grand Crystal",
        "description": "Premium crystal candelabra for hotels",
        "specs": ["9 Arms", "Premium Quality"]
    },
    {
        "file": "color 5 arms candelabra.jpg",
        "title": "5-Arm Color Crystal Candelabra",
        "description": "Colorful design for modern events",
        "specs": ["5 Arms", "Color Design"]
    },
    {
        "file": "candle holders.jpg",
        "title": "Crystal Candle Holders",
        "description": "Elegant crystal holders for candles",
        "specs": ["Candle Holder", "Crystal"]
    },
    {
        "file": "9 candlesticks candelabra.jpg",
        "title": "9 Candlesticks Crystal Candelabra",
        "description": "Classic design with 9 candlesticks",
        "specs": ["9 Candlesticks", "Classic Design"]
    },
    {
        "file": "product-1.jpg",
        "title": "Crystal Decorative Crafts",
        "description": "Decorative crystal art piece",
        "specs": ["Decorative", "Art"]
    },
    {
        "file": "product-2.jpg",
        "title": "Premium Crystal Decor",
        "description": "High-end decorative crystal",
        "specs": ["Premium", "Decor"]
    },
    {
        "file": "product-3.jpg",
        "title": "Crystal Ornament",
        "description": "Beautiful crystal ornament",
        "specs": ["Ornament", "Crystal"]
    },
    {
        "file": "product-4.jpg",
        "title": "Crystal Craft Piece",
        "description": "Artistic crystal craft",
        "specs": ["Craft", "Artistic"]
    }
]

def generate_keywords_for_product(product_info: Dict) -> Dict:
    """
    Generate SEO keywords for a product using LLM
    
    Args:
        product_info: Dictionary containing product information
    
    Returns:
        Dictionary with generated keywords and alt text
    """
    
    prompt = f"""
    Generate SEO keywords and alt text for a crystal product based on the following information:
    
    Product Name: {product_info['title']}
    Description: {product_info['description']}
    Specifications: {', '.join(product_info['specs'])}
    
    Please provide:
    1. 5-8 relevant SEO keywords for this product (comma-separated)
    2. A descriptive alt text for the image (max 150 characters)
    3. 3-4 long-tail keywords for better search ranking
    
    Output in JSON format:
    {{
        "keywords": "keyword1, keyword2, keyword3, ...",
        "alt_text": "Descriptive alt text",
        "long_tail_keywords": ["long tail 1", "long tail 2", "long tail 3"]
    }}
    """
    
    try:
        client = LLMClient()
        
        messages = [
            SystemMessage(content="You are an SEO expert specializing in crystal crafts and candelabras."),
            HumanMessage(content=prompt)
        ]
        
        response = client.invoke(
            messages=messages,
            temperature=0.3,
            max_completion_tokens=500
        )
        
        # Parse JSON response
        if isinstance(response.content, str):
            content = response.content.strip()
            # Try to extract JSON from the response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
        
        # Fallback if JSON parsing fails
        return {
            "keywords": f"crystal candelabra, {product_info['title'].lower()}, crystal candle holder, wedding centerpiece",
            "alt_text": f"{product_info['title']} - {product_info['description']}",
            "long_tail_keywords": [
                f"buy {product_info['title'].lower()}",
                f"wholesale {product_info['title'].lower()}",
                f"luxury {product_info['title'].lower()}"
            ]
        }
        
    except Exception as e:
        print(f"Error generating keywords for {product_info['file']}: {e}")
        # Fallback keywords
        return {
            "keywords": f"crystal candelabra, {product_info['title'].lower()}, crystal candle holder, wedding centerpiece, event decoration",
            "alt_text": f"{product_info['title']} - {product_info['description']}",
            "long_tail_keywords": [
                f"buy {product_info['title'].lower()} online",
                f"wholesale {product_info['title'].lower()} for events",
                f"luxury {product_info['title'].lower()} wholesale"
            ]
        }

def main():
    """Main function to generate keywords for all products"""
    
    print("Generating keywords for products...")
    print("=" * 60)
    
    results = []
    
    for product in products:
        print(f"\nProcessing: {product['file']}")
        print(f"Product: {product['title']}")
        
        keywords = generate_keywords_for_product(product)
        
        result = {
            "file": product['file'],
            "title": product['title'],
            "keywords": keywords.get("keywords", ""),
            "alt_text": keywords.get("alt_text", ""),
            "long_tail_keywords": keywords.get("long_tail_keywords", [])
        }
        
        results.append(result)
        
        print(f"  Keywords: {result['keywords']}")
        print(f"  Alt Text: {result['alt_text']}")
        print(f"  Long-tail: {', '.join(result['long_tail_keywords'])}")
    
    # Save results to JSON
    output_file = "product_keywords.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"Results saved to {output_file}")
    print("\nSummary:")
    print(f"  Total products analyzed: {len(results)}")
    print(f"  Keywords generated for each product")

if __name__ == "__main__":
    main()
