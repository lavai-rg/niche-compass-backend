from pymongo import MongoClient
from src.config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Connect to MongoDB/Cosmos DB"""
        try:
            connection_string = Config.COSMOS_DB_CONNECTION_STRING
            if not connection_string or 'YOUR_PRIMARY_KEY' in connection_string:
                logger.warning("No valid Cosmos DB connection string found. Running in mock mode.")
                # For development without Cosmos DB, we'll use a mock database
                self._client = None
                self._db = None
                return
            
            # For Cosmos DB, we need to handle SSL and other specific settings
            self._client = MongoClient(
                connection_string,
                ssl=True,
                ssl_cert_reqs='CERT_NONE',  # For development
                retryWrites=False,
                maxIdleTimeMS=120000
            )
            self._db = self._client[Config.DATABASE_NAME]
            
            # Test the connection with a simple operation
            self._db.command('ping')
            logger.info(f"Successfully connected to Cosmos DB: {Config.DATABASE_NAME}")
            
        except Exception as e:
            logger.warning(f"Failed to connect to Cosmos DB: {str(e)}")
            logger.info("Running in mock mode without database")
            # For development, we'll create a mock database
            self._client = None
            self._db = None
    
    def get_database(self):
        """Get the database instance"""
        return self._db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        if self._db is None:
            # Return a mock collection for development
            return MockCollection(collection_name)
        return self._db[collection_name]
    
    def close_connection(self):
        """Close the database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Database connection closed")

class MockCollection:
    """Mock collection for development without database"""
    
    def __init__(self, name):
        self.name = name
        self._data = {}  # Simple in-memory storage
        logger.info(f"Using mock collection: {name}")
    
    def find_one(self, query):
        """Mock find_one operation"""
        logger.debug(f"Mock find_one in {self.name}: {query}")
        return None  # Always return None for now
    
    def find(self, query=None):
        """Mock find operation"""
        logger.debug(f"Mock find in {self.name}: {query}")
        return MockCursor([])  # Return empty cursor
    
    def replace_one(self, filter_query, replacement, upsert=False):
        """Mock replace_one operation"""
        logger.debug(f"Mock replace_one in {self.name}: {filter_query}")
        return MockResult(upserted_id='mock_id', modified_count=1)
    
    def delete_one(self, query):
        """Mock delete_one operation"""
        logger.debug(f"Mock delete_one in {self.name}: {query}")
        return MockResult(deleted_count=1)

class MockCursor:
    """Mock cursor for development"""
    
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def skip(self, count):
        return self
    
    def limit(self, count):
        return self
    
    def sort(self, key, direction=1):
        return self
    
    def __iter__(self):
        return iter(self.data)

class MockResult:
    """Mock result for database operations"""
    
    def __init__(self, upserted_id=None, modified_count=0, deleted_count=0):
        self.upserted_id = upserted_id
        self.modified_count = modified_count
        self.deleted_count = deleted_count

# Global database instance
db_instance = Database()

def get_db():
    """Get the global database instance"""
    return db_instance.get_database()

def get_collection(collection_name):
    """Get a specific collection from the global database instance"""
    return db_instance.get_collection(collection_name)

