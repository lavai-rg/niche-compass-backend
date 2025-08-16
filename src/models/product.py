from datetime import datetime
from bson import ObjectId
from src.database import get_collection
from src.config import Config

class Product:
    def __init__(self, title, url, store_name, price=None, currency='USD', 
                 description=None, images=None, tags=None, category=None,
                 sales_estimate=None, reviews_count=None, rating=None,
                 listing_date=None, niche=None, sentiment_analysis=None,
                 created_at=None, updated_at=None, _id=None):
        self._id = _id or ObjectId()
        self.title = title
        self.url = url
        self.store_name = store_name
        self.price = price
        self.currency = currency
        self.description = description
        self.images = images or []
        self.tags = tags or []
        self.category = category
        self.sales_estimate = sales_estimate
        self.reviews_count = reviews_count or 0
        self.rating = rating
        self.listing_date = listing_date
        self.niche = niche
        self.sentiment_analysis = sentiment_analysis or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            '_id': str(self._id),
            'title': self.title,
            'url': self.url,
            'store_name': self.store_name,
            'price': self.price,
            'currency': self.currency,
            'description': self.description,
            'images': self.images,
            'tags': self.tags,
            'category': self.category,
            'sales_estimate': self.sales_estimate,
            'reviews_count': self.reviews_count,
            'rating': self.rating,
            'listing_date': self.listing_date.isoformat() if self.listing_date else None,
            'niche': self.niche,
            'sentiment_analysis': self.sentiment_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Product instance from dictionary"""
        return cls(
            _id=data.get('_id'),
            title=data.get('title'),
            url=data.get('url'),
            store_name=data.get('store_name'),
            price=data.get('price'),
            currency=data.get('currency', 'USD'),
            description=data.get('description'),
            images=data.get('images', []),
            tags=data.get('tags', []),
            category=data.get('category'),
            sales_estimate=data.get('sales_estimate'),
            reviews_count=data.get('reviews_count', 0),
            rating=data.get('rating'),
            listing_date=data.get('listing_date'),
            niche=data.get('niche'),
            sentiment_analysis=data.get('sentiment_analysis', {}),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def save(self):
        """Save product to database"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return None
            
        self.updated_at = datetime.utcnow()
        data = self.to_dict()
        data['_id'] = self._id
        
        result = collection.replace_one(
            {'_id': self._id},
            data,
            upsert=True
        )
        return result
    
    @classmethod
    def find_by_id(cls, product_id):
        """Find product by ID"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return None
            
        data = collection.find_one({'_id': ObjectId(product_id)})
        if data:
            return cls.from_dict(data)
        return None
    
    @classmethod
    def find_by_url(cls, url):
        """Find product by URL"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return None
            
        data = collection.find_one({'url': url})
        if data:
            return cls.from_dict(data)
        return None
    
    @classmethod
    def find_by_niche(cls, niche, limit=50, skip=0):
        """Find products by niche"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return []
            
        cursor = collection.find({'niche': niche}).skip(skip).limit(limit).sort('sales_estimate', -1)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
    def find_by_store(cls, store_name, limit=50):
        """Find products by store name"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return []
            
        cursor = collection.find({'store_name': store_name}).limit(limit).sort('sales_estimate', -1)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
    def get_top_selling(cls, niche=None, limit=20):
        """Get top selling products, optionally filtered by niche"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return []
            
        query = {}
        if niche:
            query['niche'] = niche
            
        cursor = collection.find(query).limit(limit).sort('sales_estimate', -1)
        return [cls.from_dict(data) for data in cursor]
    
    def delete(self):
        """Delete product from database"""
        collection = get_collection(Config.COLLECTION_PRODUCTS)
        if collection is None:
            return None
            
        result = collection.delete_one({'_id': self._id})
        return result

