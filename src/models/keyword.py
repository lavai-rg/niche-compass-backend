from datetime import datetime
from bson import ObjectId
from src.database import get_collection
from src.config import Config

class Keyword:
    def __init__(self, keyword, search_volume=None, competition_level=None,
                 trend_direction=None, related_keywords=None, niche=None,
                 price_range=None, seasonal_data=None, last_updated=None,
                 created_at=None, _id=None):
        self._id = _id or ObjectId()
        self.keyword = keyword.lower().strip()  # Normalize keyword
        self.search_volume = search_volume
        self.competition_level = competition_level  # 'low', 'medium', 'high'
        self.trend_direction = trend_direction  # 'rising', 'stable', 'declining'
        self.related_keywords = related_keywords or []
        self.niche = niche
        self.price_range = price_range or {}  # {'min': 0, 'max': 100, 'avg': 50}
        self.seasonal_data = seasonal_data or {}
        self.last_updated = last_updated or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            '_id': str(self._id),
            'keyword': self.keyword,
            'search_volume': self.search_volume,
            'competition_level': self.competition_level,
            'trend_direction': self.trend_direction,
            'related_keywords': self.related_keywords,
            'niche': self.niche,
            'price_range': self.price_range,
            'seasonal_data': self.seasonal_data,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Keyword instance from dictionary"""
        return cls(
            _id=data.get('_id'),
            keyword=data.get('keyword'),
            search_volume=data.get('search_volume'),
            competition_level=data.get('competition_level'),
            trend_direction=data.get('trend_direction'),
            related_keywords=data.get('related_keywords', []),
            niche=data.get('niche'),
            price_range=data.get('price_range', {}),
            seasonal_data=data.get('seasonal_data', {}),
            last_updated=data.get('last_updated'),
            created_at=data.get('created_at')
        )
    
    def save(self):
        """Save keyword to database"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return None
            
        self.last_updated = datetime.utcnow()
        data = self.to_dict()
        data['_id'] = self._id
        
        result = collection.replace_one(
            {'_id': self._id},
            data,
            upsert=True
        )
        return result
    
    @classmethod
    def find_by_keyword(cls, keyword):
        """Find keyword by exact match"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return None
            
        data = collection.find_one({'keyword': keyword.lower().strip()})
        if data:
            return cls.from_dict(data)
        return None
    
    @classmethod
    def search_keywords(cls, query, limit=20):
        """Search keywords by partial match"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return []
            
        cursor = collection.find({
            'keyword': {'$regex': query.lower(), '$options': 'i'}
        }).limit(limit).sort('search_volume', -1)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
    def get_trending_keywords(cls, limit=50):
        """Get trending keywords (rising trend direction)"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return []
            
        cursor = collection.find({
            'trend_direction': 'rising'
        }).limit(limit).sort('search_volume', -1)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
    def get_by_niche(cls, niche, limit=30):
        """Get keywords by niche"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return []
            
        cursor = collection.find({'niche': niche}).limit(limit).sort('search_volume', -1)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
    def get_low_competition(cls, max_competition='medium', limit=30):
        """Get keywords with low to medium competition"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return []
            
        competition_order = ['low', 'medium', 'high']
        max_index = competition_order.index(max_competition)
        allowed_levels = competition_order[:max_index + 1]
        
        cursor = collection.find({
            'competition_level': {'$in': allowed_levels}
        }).limit(limit).sort('search_volume', -1)
        return [cls.from_dict(data) for data in cursor]
    
    def add_related_keyword(self, related_keyword):
        """Add a related keyword"""
        if related_keyword not in self.related_keywords:
            self.related_keywords.append(related_keyword)
            self.save()
    
    def update_trend_data(self, search_volume=None, competition_level=None, trend_direction=None):
        """Update trend data for the keyword"""
        if search_volume is not None:
            self.search_volume = search_volume
        if competition_level is not None:
            self.competition_level = competition_level
        if trend_direction is not None:
            self.trend_direction = trend_direction
        
        self.last_updated = datetime.utcnow()
        self.save()
    
    def delete(self):
        """Delete keyword from database"""
        collection = get_collection(Config.COLLECTION_KEYWORDS)
        if collection is None:
            return None
            
        result = collection.delete_one({'_id': self._id})
        return result

