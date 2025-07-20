from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

from config import config
from models.user import db as user_db, bcrypt
from models.module import db as module_db
from models.challenge import db as challenge_db
from models.progress import db as progress_db
from models.leaderboard import db as leaderboard_db

# Import blueprints
from routes.auth import auth_bp
from routes.user import user_bp
from routes.modules import modules_bp
from routes.challenges import challenges_bp
from routes.leaderboard import leaderboard_bp
from routes.admin import admin_bp
from routes.ai import ai_bp
from routes.docs import docs_bp

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db = SQLAlchemy()
    db.init_app(app)
    
    # Use the same db instance across all models
    # user_db.init_app(app)
    # module_db.init_app(app)
    # challenge_db.init_app(app)
    # progress_db.init_app(app)
    # leaderboard_db.init_app(app)
    
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Configure CORS with security settings
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000']),
         methods=app.config.get('CORS_METHODS', ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
         allow_headers=app.config.get('CORS_ALLOW_HEADERS', ['Content-Type', 'Authorization', 'X-Requested-With']),
         supports_credentials=True)
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    bcrypt.init_app(app)
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        # Content Security Policy
        response.headers['Content-Security-Policy'] = app.config.get('CONTENT_SECURITY_POLICY', 
            "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:; frame-ancestors 'none';")
        
        # Strict Transport Security
        response.headers['Strict-Transport-Security'] = app.config.get('STRICT_TRANSPORT_SECURITY', 
            'max-age=31536000; includeSubDomains')
        
        # X-Frame-Options
        response.headers['X-Frame-Options'] = 'DENY'
        
        # X-Content-Type-Options
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # X-XSS-Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server information
        response.headers['Server'] = 'CipherQuest'
        
        return response
    
    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cipherquest.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('CipherQuest startup')
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(modules_bp, url_prefix='/api/modules')
    app.register_blueprint(challenges_bp, url_prefix='/api/challenges')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(docs_bp, url_prefix='/api')
    
    # Error handlers
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle generic HTTP exceptions with JSON response."""
        response = error.get_response()
        response.data = jsonify({
            'error': error.name,
            'description': error.description
        }).data
        response.content_type = "application/json"
        return response, error.code

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return jsonify({'error': 'Unauthorized'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors."""
        return jsonify({'error': 'Forbidden'}), 403

    @app.errorhandler(429)
    def ratelimit_handler(error):
        """Handle 429 Too Many Requests errors."""
        return jsonify({'error': 'Rate limit exceeded'}), 429

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error and rollback DB session."""
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle uncaught exceptions with a generic message."""
        app.logger.error(f"Unhandled Exception: {error}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'CipherQuest API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 