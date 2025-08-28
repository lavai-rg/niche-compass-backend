from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import requests
import re
import random
from urllib.parse import urlparse

sales_estimator_bp = Blueprint('sales_estimator', __name__)

@sales_estimator_bp.route('/sales-estimator', methods=['POST'])
@cross_origin()
def sales_estimator():
    """
    Endpoint untuk estimasi penjualan berdasarkan URL produk Shopify
    """
    try:
        data = request.get_json()
        product_url = data.get('product_url', '')
        
        if not product_url:
            return jsonify({'error': 'URL produk diperlukan'}), 400
        
        # Validasi URL Shopify
        if not is_valid_shopify_url(product_url):
            return jsonify({'error': 'URL harus berupa URL produk Shopify yang valid'}), 400
        
        # Simulasi analisis produk (dalam implementasi nyata, ini akan menggunakan Shopify API)
        product_analysis = analyze_product_url(product_url)
        
        # Estimasi penjualan berdasarkan berbagai faktor
        sales_estimate = calculate_sales_estimate(product_analysis)
        
        return jsonify({
            'success': True,
            'product_analysis': product_analysis,
            'sales_estimate': sales_estimate,
            'recommendations': generate_recommendations(product_analysis, sales_estimate)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def is_valid_shopify_url(url):
    """
    Validasi apakah URL adalah URL produk Shopify yang valid
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Cek apakah domain mengandung 'shopify' atau berakhiran '.myshopify.com'
        if 'myshopify.com' in domain or 'shopify' in domain:
            # Cek apakah path mengandung '/products/'
            if '/products/' in parsed_url.path:
                return True
        
        # Cek untuk custom domain yang mungkin menggunakan Shopify
        # Dalam implementasi nyata, ini bisa lebih sophisticated
        if '/products/' in parsed_url.path and domain:
            return True
            
        return False
    except:
        return False

def analyze_product_url(url):
    """
    Analisis URL produk untuk mendapatkan informasi dasar
    """
    try:
        # Ekstrak nama produk dari URL
        product_name = extract_product_name_from_url(url)
        
        # Simulasi analisis (dalam implementasi nyata, ini akan menggunakan web scraping atau API)
        analysis = {
            'product_name': product_name,
            'estimated_price': random.randint(15, 200),  # Simulasi harga
            'category': determine_category(product_name),
            'competition_level': random.choice(['Low', 'Medium', 'High']),
            'market_demand': random.randint(60, 95),
            'seasonality': random.choice(['High', 'Medium', 'Low']),
            'target_audience': determine_target_audience(product_name),
            'conversion_factors': analyze_conversion_factors(url)
        }
        
        return analysis
        
    except Exception as e:
        return {
            'product_name': 'Unknown Product',
            'estimated_price': 50,
            'category': 'General',
            'competition_level': 'Medium',
            'market_demand': 75,
            'seasonality': 'Medium',
            'target_audience': 'General',
            'conversion_factors': {
                'url_quality': 'Medium',
                'product_name_clarity': 'Medium'
            }
        }

def extract_product_name_from_url(url):
    """
    Ekstrak nama produk dari URL
    """
    try:
        # Ambil bagian setelah '/products/'
        if '/products/' in url:
            product_slug = url.split('/products/')[-1].split('?')[0].split('#')[0]
            # Konversi slug ke nama yang lebih readable
            product_name = product_slug.replace('-', ' ').replace('_', ' ').title()
            return product_name
        return 'Unknown Product'
    except:
        return 'Unknown Product'

def determine_category(product_name):
    """
    Tentukan kategori produk berdasarkan nama
    """
    categories = {
        'jewelry': ['ring', 'necklace', 'bracelet', 'earring', 'jewelry'],
        'clothing': ['shirt', 'dress', 'pants', 'jacket', 'clothing', 'apparel'],
        'home_decor': ['lamp', 'pillow', 'candle', 'decor', 'home'],
        'electronics': ['phone', 'laptop', 'headphone', 'electronic', 'tech'],
        'beauty': ['cream', 'serum', 'makeup', 'beauty', 'skincare'],
        'fitness': ['yoga', 'fitness', 'exercise', 'workout', 'gym']
    }
    
    product_name_lower = product_name.lower()
    
    for category, keywords in categories.items():
        if any(keyword in product_name_lower for keyword in keywords):
            return category.replace('_', ' ').title()
    
    return 'General'

def determine_target_audience(product_name):
    """
    Tentukan target audience berdasarkan nama produk
    """
    audiences = {
        'Women 25-45': ['jewelry', 'beauty', 'skincare', 'dress', 'handbag'],
        'Men 25-40': ['watch', 'wallet', 'tech', 'fitness', 'gadget'],
        'Young Adults 18-30': ['phone', 'headphone', 'fashion', 'trendy'],
        'Families': ['home', 'kitchen', 'kids', 'family', 'household'],
        'Professionals': ['office', 'business', 'professional', 'work']
    }
    
    product_name_lower = product_name.lower()
    
    for audience, keywords in audiences.items():
        if any(keyword in product_name_lower for keyword in keywords):
            return audience
    
    return 'General Audience'

def analyze_conversion_factors(url):
    """
    Analisis faktor-faktor yang mempengaruhi konversi
    """
    factors = {}
    
    # Analisis kualitas URL
    if len(url) < 100 and '-' in url:
        factors['url_quality'] = 'Good'
    elif len(url) > 150:
        factors['url_quality'] = 'Poor'
    else:
        factors['url_quality'] = 'Medium'
    
    # Analisis kejelasan nama produk
    product_name = extract_product_name_from_url(url)
    if len(product_name.split()) >= 3:
        factors['product_name_clarity'] = 'Good'
    elif len(product_name.split()) == 2:
        factors['product_name_clarity'] = 'Medium'
    else:
        factors['product_name_clarity'] = 'Poor'
    
    return factors

def calculate_sales_estimate(analysis):
    """
    Hitung estimasi penjualan berdasarkan analisis produk
    """
    base_sales = 100  # Base monthly sales
    
    # Faktor harga
    price = analysis['estimated_price']
    if price < 25:
        price_factor = 1.3
    elif price < 50:
        price_factor = 1.1
    elif price < 100:
        price_factor = 1.0
    else:
        price_factor = 0.8
    
    # Faktor kompetisi
    competition_factors = {
        'Low': 1.4,
        'Medium': 1.0,
        'High': 0.7
    }
    competition_factor = competition_factors.get(analysis['competition_level'], 1.0)
    
    # Faktor demand
    demand_factor = analysis['market_demand'] / 100
    
    # Faktor musiman
    seasonality_factors = {
        'High': 1.3,
        'Medium': 1.0,
        'Low': 0.8
    }
    seasonality_factor = seasonality_factors.get(analysis['seasonality'], 1.0)
    
    # Hitung estimasi
    estimated_monthly_sales = int(base_sales * price_factor * competition_factor * demand_factor * seasonality_factor)
    estimated_revenue = estimated_monthly_sales * price
    
    # Estimasi abandoned cart rate berdasarkan kategori
    category_cart_rates = {
        'Jewelry': 68,
        'Clothing': 72,
        'Home Decor': 65,
        'Electronics': 70,
        'Beauty': 66,
        'Fitness': 69,
        'General': 70
    }
    
    abandoned_cart_rate = category_cart_rates.get(analysis['category'], 70)
    potential_sales_with_recovery = int(estimated_monthly_sales / (1 - abandoned_cart_rate/100))
    
    return {
        'estimated_monthly_sales': estimated_monthly_sales,
        'estimated_monthly_revenue': estimated_revenue,
        'abandoned_cart_rate': abandoned_cart_rate,
        'potential_sales_with_cart_recovery': potential_sales_with_recovery,
        'potential_additional_revenue': (potential_sales_with_recovery - estimated_monthly_sales) * price,
        'confidence_level': calculate_confidence_level(analysis)
    }

def calculate_confidence_level(analysis):
    """
    Hitung tingkat kepercayaan estimasi
    """
    confidence = 70  # Base confidence
    
    # Faktor kompetisi
    if analysis['competition_level'] == 'Low':
        confidence += 10
    elif analysis['competition_level'] == 'High':
        confidence -= 10
    
    # Faktor demand
    if analysis['market_demand'] > 85:
        confidence += 10
    elif analysis['market_demand'] < 65:
        confidence -= 10
    
    # Faktor conversion factors
    conversion_factors = analysis.get('conversion_factors', {})
    if conversion_factors.get('url_quality') == 'Good':
        confidence += 5
    if conversion_factors.get('product_name_clarity') == 'Good':
        confidence += 5
    
    return min(95, max(50, confidence))

def generate_recommendations(analysis, sales_estimate):
    """
    Generate rekomendasi berdasarkan analisis dan estimasi
    """
    recommendations = []
    
    # Rekomendasi berdasarkan tingkat kompetisi
    if analysis['competition_level'] == 'High':
        recommendations.append({
            'type': 'Competition',
            'title': 'Tingkat Kompetisi Tinggi',
            'description': 'Fokus pada diferensiasi produk dan unique selling proposition yang kuat.',
            'action': 'Analisis kompetitor dan cari celah pasar yang belum terisi.'
        })
    
    # Rekomendasi berdasarkan abandoned cart rate
    if sales_estimate['abandoned_cart_rate'] > 70:
        recommendations.append({
            'type': 'Conversion',
            'title': 'Tingkat Abandoned Cart Tinggi',
            'description': f'Kategori {analysis["category"]} memiliki tingkat abandoned cart {sales_estimate["abandoned_cart_rate"]}%.',
            'action': 'Implementasikan email recovery, simplifikasi checkout, dan tambahkan trust signals.'
        })
    
    # Rekomendasi berdasarkan harga
    if analysis['estimated_price'] > 100:
        recommendations.append({
            'type': 'Pricing',
            'title': 'Produk High-Ticket',
            'description': 'Produk dengan harga tinggi memerlukan strategi pemasaran yang berbeda.',
            'action': 'Fokus pada kualitas konten, testimonial, dan garansi untuk membangun kepercayaan.'
        })
    
    # Rekomendasi berdasarkan musiman
    if analysis['seasonality'] == 'High':
        recommendations.append({
            'type': 'Seasonality',
            'title': 'Produk Musiman',
            'description': 'Produk ini memiliki fluktuasi permintaan yang tinggi berdasarkan musim.',
            'action': 'Rencanakan inventory dan kampanye pemasaran sesuai dengan pola musiman.'
        })
    
    # Rekomendasi untuk meningkatkan confidence
    if sales_estimate['confidence_level'] < 75:
        recommendations.append({
            'type': 'Data Quality',
            'title': 'Tingkatkan Akurasi Estimasi',
            'description': 'Estimasi dapat ditingkatkan dengan data yang lebih lengkap.',
            'action': 'Lakukan riset pasar lebih mendalam dan analisis kompetitor yang detail.'
        })
    
    return recommendations

