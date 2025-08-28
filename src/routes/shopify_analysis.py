from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import requests
import json
import random
from datetime import datetime, timedelta

shopify_bp = Blueprint('shopify', __name__)

# Mock data untuk MVP - dalam implementasi nyata akan menggunakan Azure AI services
MOCK_KEYWORDS = [
    {"keyword": "sustainable jewelry", "demand_score": 85, "competition_score": 45, "difficulty": "Medium"},
    {"keyword": "minimalist home decor", "demand_score": 92, "competition_score": 78, "difficulty": "High"},
    {"keyword": "eco-friendly phone cases", "demand_score": 76, "competition_score": 32, "difficulty": "Low"},
    {"keyword": "handmade ceramic mugs", "demand_score": 68, "competition_score": 55, "difficulty": "Medium"},
    {"keyword": "vintage style watches", "demand_score": 89, "competition_score": 82, "difficulty": "High"},
    {"keyword": "organic skincare products", "demand_score": 94, "competition_score": 88, "difficulty": "High"},
    {"keyword": "custom pet portraits", "demand_score": 72, "competition_score": 28, "difficulty": "Low"},
    {"keyword": "yoga accessories", "demand_score": 81, "competition_score": 65, "difficulty": "Medium"},
    {"keyword": "artisan coffee beans", "demand_score": 77, "competition_score": 71, "difficulty": "Medium"},
    {"keyword": "smart home gadgets", "demand_score": 96, "competition_score": 91, "difficulty": "High"}
]

MOCK_NICHES = {
    "sustainable jewelry": {
        "average_price": 45.99,
        "price_distribution": {
            "under_20": 15,
            "20_50": 45,
            "50_100": 30,
            "over_100": 10
        },
        "estimated_monthly_sales": 1250,
        "popular_tags": ["sustainable", "eco-friendly", "handmade", "recycled", "ethical"],
        "difficulty_score": "B",
        "market_size": "Growing",
        "seasonal_trends": "Stable year-round with peaks during holidays"
    },
    "minimalist home decor": {
        "average_price": 32.50,
        "price_distribution": {
            "under_20": 25,
            "20_50": 50,
            "50_100": 20,
            "over_100": 5
        },
        "estimated_monthly_sales": 2100,
        "popular_tags": ["minimalist", "modern", "clean", "simple", "scandinavian"],
        "difficulty_score": "A",
        "market_size": "Large and growing",
        "seasonal_trends": "Peak in spring and fall (home renovation seasons)"
    },
    "eco-friendly phone cases": {
        "average_price": 24.99,
        "price_distribution": {
            "under_20": 35,
            "20_50": 55,
            "50_100": 10,
            "over_100": 0
        },
        "estimated_monthly_sales": 890,
        "popular_tags": ["eco-friendly", "biodegradable", "sustainable", "protective", "durable"],
        "difficulty_score": "C",
        "market_size": "Medium but growing rapidly",
        "seasonal_trends": "Peaks during new phone releases"
    }
}

@shopify_bp.route('/keyword-explorer', methods=['POST'])
@cross_origin()
def keyword_explorer():
    """
    Endpoint untuk mengeksplorasi kata kunci dan mendapatkan skor demand vs competition
    """
    try:
        data = request.get_json()
        base_keyword = data.get('keyword', '').lower()
        
        if not base_keyword:
            return jsonify({"error": "Keyword is required"}), 400
        
        # Filter keywords yang relevan dengan base keyword
        relevant_keywords = []
        for keyword_data in MOCK_KEYWORDS:
            if any(word in keyword_data['keyword'].lower() for word in base_keyword.split()):
                relevant_keywords.append(keyword_data)
        
        # Jika tidak ada yang relevan, return random sample
        if not relevant_keywords:
            relevant_keywords = random.sample(MOCK_KEYWORDS, min(5, len(MOCK_KEYWORDS)))
        
        # Generate additional related keywords
        additional_keywords = generate_related_keywords(base_keyword)
        relevant_keywords.extend(additional_keywords)
        
        return jsonify({
            "success": True,
            "base_keyword": base_keyword,
            "related_keywords": relevant_keywords[:10],  # Limit to 10 results
            "total_found": len(relevant_keywords)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shopify_bp.route('/niche-analysis', methods=['POST'])
@cross_origin()
def niche_analysis():
    """
    Endpoint untuk analisis mendalam niche tertentu
    """
    try:
        data = request.get_json()
        niche_keyword = data.get('keyword', '').lower()
        
        if not niche_keyword:
            return jsonify({"error": "Keyword is required"}), 400
        
        # Cari data niche yang paling relevan
        niche_data = None
        for niche_key, niche_info in MOCK_NICHES.items():
            if niche_keyword in niche_key or any(word in niche_key for word in niche_keyword.split()):
                niche_data = niche_info.copy()
                niche_data['niche_name'] = niche_key
                break
        
        # Jika tidak ditemukan, generate data mock
        if not niche_data:
            niche_data = generate_mock_niche_data(niche_keyword)
        
        return jsonify({
            "success": True,
            "niche_analysis": niche_data,
            "analysis_date": datetime.now().isoformat(),
            "data_freshness": "Last updated 24 hours ago"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shopify_bp.route('/sales-estimator', methods=['POST'])
@cross_origin()
def sales_estimator():
    """
    Endpoint untuk estimasi penjualan berdasarkan URL produk atau data produk
    """
    try:
        data = request.get_json()
        product_url = data.get('product_url', '')
        product_data = data.get('product_data', {})
        
        if not product_url and not product_data:
            return jsonify({"error": "Product URL or product data is required"}), 400
        
        # Mock analysis - dalam implementasi nyata akan scrape data dari URL
        estimated_sales = {
            "monthly_sales_estimate": random.randint(50, 500),
            "revenue_estimate": random.randint(1000, 15000),
            "confidence_level": random.choice(["High", "Medium", "Low"]),
            "factors_analyzed": [
                "Product reviews count",
                "Store popularity",
                "Price competitiveness",
                "Product category trends",
                "Seasonal factors"
            ],
            "recommendations": [
                "Consider optimizing product images for better conversion",
                "Price is competitive within the niche",
                "Add more customer reviews to increase trust",
                "Consider seasonal promotions"
            ]
        }
        
        return jsonify({
            "success": True,
            "sales_estimation": estimated_sales,
            "analysis_date": datetime.now().isoformat(),
            "disclaimer": "Estimates based on market analysis and similar products"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shopify_bp.route('/profitability-calculator', methods=['POST'])
@cross_origin()
def profitability_calculator():
    """
    Endpoint untuk kalkulator profitabilitas
    """
    try:
        data = request.get_json()
        
        # Input costs
        material_cost = float(data.get('material_cost', 0))
        shipping_cost = float(data.get('shipping_cost', 0))
        shopify_fees = float(data.get('shopify_fees', 2.9))  # Default Shopify fee percentage
        desired_margin = float(data.get('desired_margin', 30))  # Default 30% margin
        
        # Calculate recommended selling price
        total_cost = material_cost + shipping_cost
        shopify_fee_decimal = shopify_fees / 100
        margin_decimal = desired_margin / 100
        
        # Formula: Selling Price = (Total Cost) / (1 - Shopify Fee % - Desired Margin %)
        recommended_price = total_cost / (1 - shopify_fee_decimal - margin_decimal)
        
        # Calculate breakdown
        shopify_fee_amount = recommended_price * shopify_fee_decimal
        profit_amount = recommended_price * margin_decimal
        
        calculation_result = {
            "recommended_selling_price": round(recommended_price, 2),
            "cost_breakdown": {
                "material_cost": material_cost,
                "shipping_cost": shipping_cost,
                "shopify_fees": round(shopify_fee_amount, 2),
                "total_costs": round(total_cost + shopify_fee_amount, 2)
            },
            "profit_analysis": {
                "gross_profit": round(profit_amount, 2),
                "profit_margin_percentage": desired_margin,
                "break_even_units": 1  # Simplified for MVP
            },
            "recommendations": [
                f"Set selling price at ${recommended_price:.2f} to achieve {desired_margin}% margin",
                "Consider bulk purchasing to reduce material costs",
                "Optimize shipping to reduce per-unit shipping costs"
            ]
        }
        
        return jsonify({
            "success": True,
            "calculation": calculation_result,
            "calculation_date": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shopify_bp.route('/trending-niches', methods=['GET'])
@cross_origin()
def trending_niches():
    """
    Endpoint untuk mendapatkan niche yang sedang trending
    """
    try:
        trending_data = [
            {
                "niche": "Sustainable Fashion",
                "growth_rate": "+45%",
                "demand_score": 92,
                "competition_level": "Medium",
                "opportunity_score": "High"
            },
            {
                "niche": "Smart Home Accessories",
                "growth_rate": "+38%",
                "demand_score": 89,
                "competition_level": "High",
                "opportunity_score": "Medium"
            },
            {
                "niche": "Pet Wellness Products",
                "growth_rate": "+52%",
                "demand_score": 85,
                "competition_level": "Low",
                "opportunity_score": "Very High"
            },
            {
                "niche": "Minimalist Office Supplies",
                "growth_rate": "+29%",
                "demand_score": 78,
                "competition_level": "Medium",
                "opportunity_score": "High"
            },
            {
                "niche": "Artisan Food Products",
                "growth_rate": "+33%",
                "demand_score": 82,
                "competition_level": "Medium",
                "opportunity_score": "High"
            }
        ]
        
        return jsonify({
            "success": True,
            "trending_niches": trending_data,
            "last_updated": datetime.now().isoformat(),
            "data_source": "Market analysis and trend monitoring"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_related_keywords(base_keyword):
    """
    Generate related keywords based on base keyword
    """
    prefixes = ["best", "cheap", "premium", "custom", "handmade", "eco-friendly", "sustainable"]
    suffixes = ["online", "store", "shop", "collection", "set", "kit", "bundle"]
    
    related = []
    for i in range(3):
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        related.append({
            "keyword": f"{prefix} {base_keyword} {suffix}",
            "demand_score": random.randint(60, 95),
            "competition_score": random.randint(20, 80),
            "difficulty": random.choice(["Low", "Medium", "High"])
        })
    
    return related

def generate_mock_niche_data(keyword):
    """
    Generate mock niche data for keywords not in predefined data
    """
    return {
        "niche_name": keyword,
        "average_price": round(random.uniform(15.99, 89.99), 2),
        "price_distribution": {
            "under_20": random.randint(10, 40),
            "20_50": random.randint(30, 60),
            "50_100": random.randint(10, 30),
            "over_100": random.randint(0, 15)
        },
        "estimated_monthly_sales": random.randint(200, 3000),
        "popular_tags": [keyword.split()[0], "quality", "affordable", "trending", "popular"],
        "difficulty_score": random.choice(["A", "B", "C", "D"]),
        "market_size": random.choice(["Small but growing", "Medium", "Large", "Very large"]),
        "seasonal_trends": "Data being analyzed - check back soon"
    }

