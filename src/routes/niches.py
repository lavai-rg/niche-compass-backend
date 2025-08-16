from flask import Blueprint, jsonify, request
from src.models.niche import Niche
from src.models.product import Product
from src.models.keyword import Keyword
import logging

logger = logging.getLogger(__name__)
niches_bp = Blueprint('niches', __name__)

@niches_bp.route('/niches', methods=['GET'])
def get_niches():
    """Get all niches with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 50)
        skip = (page - 1) * limit
        
        niches = Niche.find_all(limit, skip)
        results = [niche.to_dict() for niche in niches]
        
        return jsonify({
            'niches': results,
            'page': page,
            'limit': limit,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting niches: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/<niche_id>', methods=['GET'])
def get_niche_by_id(niche_id):
    """Get detailed information about a specific niche"""
    try:
        niche = Niche.find_by_id(niche_id)
        
        if not niche:
            return jsonify({'error': 'Niche not found'}), 404
        
        return jsonify({
            'niche': niche.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting niche by ID: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/analyze', methods=['POST'])
def analyze_niche():
    """Analyze a niche and return comprehensive data"""
    try:
        data = request.get_json()
        if not data or 'niche_name' not in data:
            return jsonify({'error': 'niche_name is required'}), 400
        
        niche_name = data['niche_name'].strip()
        if not niche_name:
            return jsonify({'error': 'niche_name cannot be empty'}), 400
        
        # Check if niche already exists
        existing_niche = Niche.find_by_name(niche_name)
        
        if existing_niche:
            result = existing_niche.to_dict()
            result['source'] = 'database'
        else:
            # Create new niche analysis (mock data for MVP)
            # In production, this would integrate with real data sources
            
            # Mock trend data
            trend_data = {
                'search_volume_trend': [100, 120, 150, 180, 200, 190, 210],
                'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                'growth_rate': 15.5,
                'seasonality': 'stable'
            }
            
            # Mock price analysis
            price_analysis = {
                'average_price': 45.50,
                'price_range': {'min': 15, 'max': 150},
                'price_distribution': {
                    'under_25': 30,
                    '25_50': 40,
                    '50_100': 25,
                    'over_100': 5
                }
            }
            
            # Mock visual analysis
            visual_analysis = {
                'dominant_colors': ['#F5F5DC', '#8B4513', '#228B22'],
                'popular_styles': ['minimalist', 'rustic', 'modern'],
                'image_types': ['lifestyle', 'product_only', 'flat_lay']
            }
            
            new_niche = Niche(
                name=niche_name,
                category=data.get('category', 'general'),
                description=f"Analysis for {niche_name} niche",
                trend_data=trend_data,
                competition_score=65,  # Mock score
                demand_score=75,       # Mock score
                visual_analysis=visual_analysis,
                price_analysis=price_analysis,
                top_products=[]  # Will be populated separately
            )
            new_niche.save()
            
            result = new_niche.to_dict()
            result['source'] = 'analysis'
        
        return jsonify({
            'niche_analysis': result
        })
        
    except Exception as e:
        logger.error(f"Error analyzing niche: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/search', methods=['GET'])
def search_niches():
    """Search niches by category or name"""
    try:
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        limit = min(int(request.args.get('limit', 20)), 50)
        
        if not query and not category:
            return jsonify({'error': 'Either query "q" or "category" parameter is required'}), 400
        
        if category:
            niches = Niche.search_by_category(category, limit)
        else:
            # For now, we'll search by name (in production, this would be more sophisticated)
            niches = [Niche.find_by_name(query)] if Niche.find_by_name(query) else []
        
        results = [niche.to_dict() for niche in niches if niche]
        
        return jsonify({
            'query': query or category,
            'search_type': 'category' if category else 'name',
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error searching niches: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/<niche_name>/products', methods=['GET'])
def get_niche_products(niche_name):
    """Get top products for a specific niche"""
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        
        products = Product.find_by_niche(niche_name, limit)
        results = [product.to_dict() for product in products]
        
        return jsonify({
            'niche': niche_name,
            'products': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting niche products: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/<niche_name>/keywords', methods=['GET'])
def get_niche_keywords(niche_name):
    """Get keywords associated with a specific niche"""
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        
        keywords = Keyword.get_by_niche(niche_name, limit)
        results = [keyword.to_dict() for keyword in keywords]
        
        return jsonify({
            'niche': niche_name,
            'keywords': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting niche keywords: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/trending', methods=['GET'])
def get_trending_niches():
    """Get trending niches based on recent activity"""
    try:
        limit = min(int(request.args.get('limit', 10)), 20)
        
        # For MVP, return mock trending niches
        # In production, this would be based on real trend analysis
        trending_niches = [
            {
                'name': 'Sustainable Home Decor',
                'category': 'home_decor',
                'growth_rate': 25.5,
                'competition_score': 45,
                'demand_score': 80
            },
            {
                'name': 'Minimalist Jewelry',
                'category': 'jewelry',
                'growth_rate': 18.2,
                'competition_score': 70,
                'demand_score': 75
            },
            {
                'name': 'Pet Accessories',
                'category': 'pets',
                'growth_rate': 22.1,
                'competition_score': 60,
                'demand_score': 85
            }
        ]
        
        return jsonify({
            'trending_niches': trending_niches[:limit],
            'count': len(trending_niches[:limit])
        })
        
    except Exception as e:
        logger.error(f"Error getting trending niches: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@niches_bp.route('/niches/opportunities', methods=['GET'])
def get_niche_opportunities():
    """Get niche opportunities (high demand, low competition)"""
    try:
        limit = min(int(request.args.get('limit', 10)), 20)
        
        # For MVP, return mock opportunities
        # In production, this would calculate based on real metrics
        opportunities = [
            {
                'name': 'Eco-Friendly Phone Cases',
                'category': 'electronics',
                'opportunity_score': 85,
                'demand_score': 75,
                'competition_score': 35,
                'reason': 'High demand for sustainable tech accessories with relatively low competition'
            },
            {
                'name': 'Vintage Map Prints',
                'category': 'art',
                'opportunity_score': 78,
                'demand_score': 70,
                'competition_score': 40,
                'reason': 'Growing interest in vintage decor with moderate competition'
            }
        ]
        
        return jsonify({
            'opportunities': opportunities[:limit],
            'count': len(opportunities[:limit])
        })
        
    except Exception as e:
        logger.error(f"Error getting niche opportunities: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

