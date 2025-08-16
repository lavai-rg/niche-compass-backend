from flask import Blueprint, jsonify, request
from src.models.user import User
import logging

logger = logging.getLogger(__name__)
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users (for admin purposes)"""
    try:
        # For MVP, we'll return a simple response
        # In production, this would have proper pagination and admin authentication
        return jsonify({
            'message': 'User management endpoint',
            'note': 'This endpoint will be implemented with proper authentication'
        })
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'{field} is required'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        
        # Check if user already exists
        if User.find_by_email(email):
            return jsonify({'error': 'User with this email already exists'}), 409
        
        if User.find_by_username(username):
            return jsonify({'error': 'Username already taken'}), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            subscription_tier=data.get('subscription_tier', 'free')
        )
        
        result = user.save()
        if result:
            return jsonify({
                'message': 'User created successfully',
                'user': user.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update allowed fields
        if 'username' in data and data['username'].strip():
            # Check if username is already taken by another user
            existing_user = User.find_by_username(data['username'].strip())
            if existing_user and str(existing_user._id) != user_id:
                return jsonify({'error': 'Username already taken'}), 409
            user.username = data['username'].strip()
        
        if 'email' in data and data['email'].strip():
            # Check if email is already taken by another user
            email = data['email'].strip().lower()
            existing_user = User.find_by_email(email)
            if existing_user and str(existing_user._id) != user_id:
                return jsonify({'error': 'Email already taken'}), 409
            user.email = email
        
        if 'subscription_tier' in data:
            if data['subscription_tier'] in ['free', 'basic', 'premium']:
                user.subscription_tier = data['subscription_tier']
        
        result = user.save()
        if result:
            return jsonify({
                'message': 'User updated successfully',
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to update user'}), 500
        
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        result = user.delete()
        if result and result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
        
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>/keywords', methods=['POST'])
def add_tracked_keyword(user_id):
    """Add a keyword to user's tracking list"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Keyword is required'}), 400
        
        keyword = data['keyword'].strip()
        if not keyword:
            return jsonify({'error': 'Keyword cannot be empty'}), 400
        
        user.add_tracked_keyword(keyword)
        
        return jsonify({
            'message': 'Keyword added to tracking list',
            'tracked_keywords': user.tracked_keywords
        })
        
    except Exception as e:
        logger.error(f"Error adding tracked keyword: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>/keywords/<keyword>', methods=['DELETE'])
def remove_tracked_keyword(user_id, keyword):
    """Remove a keyword from user's tracking list"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.remove_tracked_keyword(keyword)
        
        return jsonify({
            'message': 'Keyword removed from tracking list',
            'tracked_keywords': user.tracked_keywords
        })
        
    except Exception as e:
        logger.error(f"Error removing tracked keyword: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>/niches', methods=['POST'])
def add_favorite_niche(user_id):
    """Add a niche to user's favorites"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data or 'niche' not in data:
            return jsonify({'error': 'Niche is required'}), 400
        
        niche = data['niche'].strip()
        if not niche:
            return jsonify({'error': 'Niche cannot be empty'}), 400
        
        user.add_favorite_niche(niche)
        
        return jsonify({
            'message': 'Niche added to favorites',
            'favorite_niches': user.favorite_niches
        })
        
    except Exception as e:
        logger.error(f"Error adding favorite niche: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/users/<user_id>/niches/<niche>', methods=['DELETE'])
def remove_favorite_niche(user_id, niche):
    """Remove a niche from user's favorites"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.remove_favorite_niche(niche)
        
        return jsonify({
            'message': 'Niche removed from favorites',
            'favorite_niches': user.favorite_niches
        })
        
    except Exception as e:
        logger.error(f"Error removing favorite niche: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
