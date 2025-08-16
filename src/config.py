import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Azure Cosmos DB Configuration
    COSMOS_DB_CONNECTION_STRING = os.getenv('COSMOS_DB_CONNECTION_STRING')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'nichecompass')
    
    # Collections
    COLLECTION_USERS = os.getenv('COLLECTION_USERS', 'users')
    COLLECTION_NICHES = os.getenv('COLLECTION_NICHES', 'niches')
    COLLECTION_PRODUCTS = os.getenv('COLLECTION_PRODUCTS', 'products')
    COLLECTION_KEYWORDS = os.getenv('COLLECTION_KEYWORDS', 'keywords')
    COLLECTION_STORES = os.getenv('COLLECTION_STORES', 'stores')
    
    # Azure AI Services
    AZURE_COMPUTER_VISION_ENDPOINT = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT')
    AZURE_COMPUTER_VISION_KEY = os.getenv('AZURE_COMPUTER_VISION_KEY')
    AZURE_TEXT_ANALYTICS_ENDPOINT = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    AZURE_TEXT_ANALYTICS_KEY = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
    
    # External APIs
    ETSY_API_KEY = os.getenv('ETSY_API_KEY')
    
    # Application Settings
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 100))
    CACHE_TIMEOUT_SECONDS = int(os.getenv('CACHE_TIMEOUT_SECONDS', 3600))
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        required_vars = [
            'COSMOS_DB_CONNECTION_STRING',
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

