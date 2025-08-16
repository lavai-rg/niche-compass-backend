import os
import sys
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import configuration and database
from src.config import Config
from src.database import db_instance

# Import all route blueprints
from src.routes.user import user_bp
from src.routes.keywords import keywords_bp
from src.routes.niches import niches_bp
from src.routes.products import products_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Load configuration
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(keywords_bp, url_prefix='/api')
    app.register_blueprint(niches_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            db = db_instance.get_database()
            if db is not None:
                db_status = 'connected'
            else:
                db_status = 'disconnected'
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return {
            'status': 'healthy',
            'database': db_status,
            'version': '1.0.0'
        }
    
    # API info endpoint
    @app.route('/api', methods=['GET'])
    def api_info():
        """API information endpoint"""
        return {
            'name': 'Niche Compass API',
            'version': '1.0.0',
            'description': 'API for Etsy niche research and product analysis',
            'endpoints': {
                'keywords': '/api/keywords/*',
                'niches': '/api/niches/*',
                'products': '/api/products/*',
                'users': '/api/users/*',
                'health': '/api/health'
            }
        }
    
    # Serve frontend files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "Frontend not available. API is running at /api", 200

    return app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    try:
        # Validate configuration
        Config.validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.warning(f"Configuration validation failed: {e}")
        logger.info("Some features may not work properly without proper configuration")
    
    # Initialize database connection
    try:
        db_instance.connect()
        logger.info("Database connection initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.info("Running in development mode without database")
    
    logger.info("Starting Niche Compass API server...")
    app.run(host='0.0.0.0', port=5000, debug=False)