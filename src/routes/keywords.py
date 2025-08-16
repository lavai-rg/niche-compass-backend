from flask import Blueprint, jsonify, request
from src.models.keyword import Keyword
from src.models.user import User
import logging

logger = logging.getLogger(__name__)
keywords_bp = Blueprint('keywords', __name__)

@keywords_bp.route('/keywords/search', methods=['GET'])
def search_keywords():
    """Search keywords by query"""
    try:
        query = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 20)), 50)  # Max 50 results
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Query must be at least 2 characters long'}), 400
        
        # Search keywords
        keywords = Keyword.search_keywords(query, limit)
        
        # Convert to dict format
        results = [keyword.to_dict() for keyword in keywords]
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error searching keywords: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@keywords_bp.route('/keywords/trending', methods=['GET'])
def get_trending_keywords():
    """Get trending keywords"""
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        
        keywords = Keyword.get_trending_keywords(limit)
        results = [keyword.to_dict() for keyword in keywords]
        
        return jsonify({
            'trending_keywords': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting trending keywords: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@keywords_bp.route('/keywords/low-competition', methods=['GET'])
def get_low_competition_keywords():
    """Get keywords with low to medium competition"""
    try:
        max_competition = request.args.get('max_competition', 'medium')
        limit = min(int(request.args.get('limit', 20)), 50)
        
        if max_competition not in ['low', 'medium', 'high']:
            return jsonify({'error': 'max_competition must be low, medium, or high'}), 400
        
        keywords = Keyword.get_low_competition(max_competition, limit)
        results = [keyword.to_dict() for keyword in keywords]
        
        return jsonify({
            'low_competition_keywords': results,
            'max_competition': max_competition,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting low competition keywords: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@keywords_bp.route('/keywords/analyze', methods=['POST'])
def analyze_keyword():
    """Analyze a specific keyword and return detailed data"""
    try:
        data = request.get_json()
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Keyword is required'}), 400
        
        keyword_text = data['keyword'].strip()
        if not keyword_text:
            return jsonify({'error': 'Keyword cannot be empty'}), 400
        
        # Check if keyword already exists in database
        existing_keyword = Keyword.find_by_keyword(keyword_text)
        
        if existing_keyword:
            # Return existing data
            result = existing_keyword.to_dict()
            result['source'] = 'database'
        else:
            # For MVP, we'll create a mock analysis
            # In production, this would integrate with real APIs
            mock_keyword = Keyword(
                keyword=keyword_text,
                search_volume=1000,  # Mock data
                competition_level='medium',
                trend_direction='stable',
                related_keywords=[f"{keyword_text} ideas", f"best {keyword_text}", f"{keyword_text} design"],
                price_range={'min': 10, 'max': 100, 'avg': 35}
            )
            mock_keyword.save()
            
            result = mock_keyword.to_dict()
            result['source'] = 'analysis'
        
        return jsonify({
            'keyword_analysis': result
        })
        
    except Exception as e:
        logger.error(f"Error analyzing keyword: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@keywords_bp.route('/keywords/by-niche/<niche>', methods=['GET'])
def get_keywords_by_niche(niche):
    """Get keywords for a specific niche"""
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        
        keywords = Keyword.get_by_niche(niche, limit)
        results = [keyword.to_dict() for keyword in keywords]
        
        return jsonify({
            'niche': niche,
            'keywords': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting keywords by niche: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@keywords_bp.route('/keywords/suggestions', methods=['POST'])
def get_keyword_suggestions():
    """Get keyword suggestions based on a seed keyword"""
    try:
        data = request.get_json()
        if not data or 'seed_keyword' not in data:
            return jsonify({'error': 'seed_keyword is required'}), 400
        
        seed_keyword = data['seed_keyword'].strip()
        limit = min(int(data.get('limit', 10)), 20)
        
        if not seed_keyword:
            return jsonify({'error': 'seed_keyword cannot be empty'}), 400
        
        # For MVP, generate simple keyword variations
        # In production, this would use more sophisticated keyword research APIs
        suggestions = []
        
        # Common keyword modifiers
        modifiers = [
            'best', 'cheap', 'affordable', 'unique', 'custom', 'handmade',
            'vintage', 'modern', 'minimalist', 'luxury', 'eco friendly',
            'personalized', 'gift', 'ideas', 'design', 'diy'
        ]
        
        # Generate suggestions
        for modifier in modifiers[:limit]:
            suggestion = f"{modifier} {seed_keyword}"
            suggestions.append({
                'keyword': suggestion,
                'search_volume': 500,  # Mock data
                'competition_level': 'low',
                'relevance_score': 0.8
            })
        
        return jsonify({
            'seed_keyword': seed_keyword,
            'suggestions': suggestions,
            'count': len(suggestions)
        })
        
    except Exception as e:
        logger.error(f"Error getting keyword suggestions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

