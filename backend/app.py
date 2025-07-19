from flask import Flask
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

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db = SQLAlchemy()
    db.init_app(app)
    
    # Use the same db instance across all models
    user_db.init_app(app)
    module_db.init_app(app)
    challenge_db.init_app(app)
    progress_db.init_app(app)
    leaderboard_db.init_app(app)
    
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    bcrypt.init_app(app)
    
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
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {'error': 'Rate limit exceeded'}, 429
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'CipherQuest API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 