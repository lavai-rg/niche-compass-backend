from datetime import datetime
from bson import ObjectId
from src.database import get_collection
from src.config import Config

class User:
    def __init__(self, username, email, password_hash=None, subscription_tier='free',
                 tracked_keywords=None, favorite_niches=None, api_usage=None,
                 created_at=None, updated_at=None, _id=None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.subscription_tier = subscription_tier  # 'free', 'basic', 'premium'
        self.tracked_keywords = tracked_keywords or []
        self.favorite_niches = favorite_niches or []
        self.api_usage = api_usage or {'requests_today': 0, 'last_reset': datetime.utcnow()}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            '_id': str(self._id),
            'username': self.username,
            'email': self.email,
            'subscription_tier': self.subscription_tier,
            'tracked_keywords': self.tracked_keywords,
            'favorite_niches': self.favorite_niches,
            'api_usage': self.api_usage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User instance from dictionary"""
        return cls(
            _id=data.get('_id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            subscription_tier=data.get('subscription_tier', 'free'),
            tracked_keywords=data.get('tracked_keywords', []),
            favorite_niches=data.get('favorite_niches', []),
            api_usage=data.get('api_usage', {'requests_today': 0, 'last_reset': datetime.utcnow()}),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def save(self):
        """Save user to database"""
        collection = get_collection(Config.COLLECTION_USERS)
        if collection is None:
            return None
            
        self.updated_at = datetime.utcnow()
        data = self.to_dict()
        data['_id'] = self._id
        # Don't include password_hash in the saved data for security
        if self.password_hash:
            data['password_hash'] = self.password_hash
        
        result = collection.replace_one(
            {'_id': self._id},
            data,
            upsert=True
        )
        return result
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        collection = get_collection(Config.COLLECTION_USERS)
        if collection is None:
            return None
            
        data = collection.find_one({'_id': ObjectId(user_id)})
        if data:
            return cls.from_dict(data)
        return None
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        collection = get_collection(Config.COLLECTION_USERS)
        if collection is None:
            return None
            
        data = collection.find_one({'email': email.lower()})
        if data:
            return cls.from_dict(data)
        return None
    
    @classmethod
    def find_by_username(cls, username):
        """Find user by username"""
        collection = get_collection(Config.COLLECTION_USERS)
        if collection is None:
            return None
            
        data = collection.find_one({'username': username})
        if data:
            return cls.from_dict(data)
        return None
    
    def add_tracked_keyword(self, keyword):
        """Add a keyword to user's tracking list"""
        if keyword not in self.tracked_keywords:
            self.tracked_keywords.append(keyword)
            self.save()
    
    def remove_tracked_keyword(self, keyword):
        """Remove a keyword from user's tracking list"""
        if keyword in self.tracked_keywords:
            self.tracked_keywords.remove(keyword)
            self.save()
    
    def add_favorite_niche(self, niche):
        """Add a niche to user's favorites"""
        if niche not in self.favorite_niches:
            self.favorite_niches.append(niche)
            self.save()
    
    def remove_favorite_niche(self, niche):
        """Remove a niche from user's favorites"""
        if niche in self.favorite_niches:
            self.favorite_niches.remove(niche)
            self.save()
    
    def increment_api_usage(self):
        """Increment API usage counter"""
        today = datetime.utcnow().date()
        last_reset = self.api_usage.get('last_reset', datetime.utcnow()).date()
        
        if today > last_reset:
            # Reset counter for new day
            self.api_usage = {
                'requests_today': 1,
                'last_reset': datetime.utcnow()
            }
        else:
            self.api_usage['requests_today'] += 1
        
        self.save()
    
    def can_make_request(self):
        """Check if user can make another API request based on their tier"""
        limits = {
            'free': 10,
            'basic': 100,
            'premium': 1000
        }
        
        limit = limits.get(self.subscription_tier, 10)
        return self.api_usage.get('requests_today', 0) < limit
    
    def delete(self):
        """Delete user from database"""
        collection = get_collection(Config.COLLECTION_USERS)
        if collection is None:
            return None
            
        result = collection.delete_one({'_id': self._id})
        return result
