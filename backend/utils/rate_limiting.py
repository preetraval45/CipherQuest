from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from flask import request, jsonify, current_app
import redis
import time
from typing import Optional, Callable, Dict, Any

class RateLimitConfig:
    """Configuration for rate limiting"""
    
    # Authentication routes
    AUTH_REGISTER = "5 per minute"
    AUTH_LOGIN = "10 per minute"
    AUTH_OAUTH = "10 per minute"
    AUTH_REFRESH = "30 per minute"
    AUTH_LOGOUT = "30 per minute"
    
    # User routes
    USER_PROFILE_GET = "60 per minute"
    USER_PROFILE_UPDATE = "30 per minute"
    USER_PROGRESS = "60 per minute"
    
    # Module routes
    MODULES_LIST = "120 per minute"
    MODULE_DETAIL = "120 per minute"
    MODULE_COMPLETE = "30 per minute"
    MODULE_PROGRESS = "60 per minute"
    
    # Challenge routes
    CHALLENGES_LIST = "120 per minute"
    CHALLENGE_DETAIL = "120 per minute"
    CHALLENGE_SUBMIT = "20 per minute"
    CHALLENGE_HINT = "5 per minute"
    CHALLENGE_PROGRESS = "60 per minute"
    
    # Leaderboard routes
    LEADERBOARD_GLOBAL = "60 per minute"
    LEADERBOARD_TOP = "60 per minute"
    LEADERBOARD_USER_RANK = "60 per minute"
    
    # AI Tutor routes
    AI_CHAT = "30 per minute"
    AI_HINT = "10 per minute"
    
    # Admin routes
    ADMIN_DASHBOARD = "60 per minute"
    ADMIN_USERS = "30 per minute"
    ADMIN_MODULES = "30 per minute"
    ADMIN_CHALLENGES = "30 per minute"
    
    # File upload routes
    FILE_UPLOAD = "10 per minute"
    FILE_DOWNLOAD = "60 per minute"
    
    # Search routes
    SEARCH_MODULES = "60 per minute"
    SEARCH_CHALLENGES = "60 per minute"
    SEARCH_USERS = "30 per minute"

class RateLimitManager:
    """Manages rate limiting across the application"""
    
    def __init__(self, app=None):
        self.app = app
        self.limiter = None
        self.redis_client = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize rate limiting with the Flask app"""
        self.app = app
        
        # Initialize Redis for rate limiting storage
        try:
            self.redis_client = redis.Redis(
                host=app.config.get('REDIS_HOST', 'localhost'),
                port=app.config.get('REDIS_PORT', 6379),
                db=app.config.get('REDIS_DB', 0),
                decode_responses=True
            )
            # Test Redis connection
            self.redis_client.ping()
        except Exception as e:
            app.logger.warning(f"Redis not available for rate limiting: {e}")
            self.redis_client = None
        
        # Initialize Flask-Limiter
        self.limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://'),
            default_limits=["200 per day", "50 per hour"],
            strategy="fixed-window-elastic-expiry"
        )
        
        # Register error handlers
        self._register_error_handlers()
    
    def _register_error_handlers(self):
        """Register rate limit error handlers"""
        
        @self.app.errorhandler(429)
        def ratelimit_handler(e):
            """Handle rate limit exceeded errors"""
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.',
                'retry_after': getattr(e, 'retry_after', 60)
            }), 429
        
        @self.limiter.request_filter
        def ip_whitelist():
            """Whitelist certain IPs from rate limiting"""
            whitelist = self.app.config.get('RATELIMIT_WHITELIST', [])
            return request.remote_addr in whitelist

def create_rate_limiter(app):
    """Create and configure rate limiter for the application"""
    rate_limit_manager = RateLimitManager(app)
    return rate_limit_manager.limiter

def rate_limit_by_user_role(role_limits: Dict[str, str]):
    """
    Decorator to apply different rate limits based on user role
    
    Args:
        role_limits (dict): Dictionary mapping roles to rate limit strings
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get user role from JWT token or session
            user_role = get_user_role_from_request()
            
            # Get appropriate rate limit for user role
            rate_limit = role_limits.get(user_role, role_limits.get('default', '60 per minute'))
            
            # Apply rate limiting
            limiter = current_app.extensions.get('limiter')
            if limiter:
                with limiter.limit(rate_limit):
                    return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def get_user_role_from_request() -> str:
    """Get user role from the current request"""
    try:
        from flask_jwt_extended import get_jwt_identity
        from models.user import User
        
        user_id = get_jwt_identity()
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.role if hasattr(user, 'role') else 'user'
    except Exception:
        pass
    
    return 'anonymous'

def rate_limit_by_ip(limit: str):
    """
    Apply rate limiting based on IP address
    
    Args:
        limit (str): Rate limit string (e.g., "100 per hour")
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            limiter = current_app.extensions.get('limiter')
            if limiter:
                with limiter.limit(limit, key_func=lambda: request.remote_addr):
                    return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit_by_user_id(limit: str):
    """
    Apply rate limiting based on user ID
    
    Args:
        limit (str): Rate limit string (e.g., "100 per hour")
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            def get_user_key():
                try:
                    from flask_jwt_extended import get_jwt_identity
                    user_id = get_jwt_identity()
                    return f"user:{user_id}" if user_id else f"ip:{request.remote_addr}"
                except Exception:
                    return f"ip:{request.remote_addr}"
            
            limiter = current_app.extensions.get('limiter')
            if limiter:
                with limiter.limit(limit, key_func=get_user_key):
                    return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit_by_endpoint(endpoint_limits: Dict[str, str]):
    """
    Apply rate limiting based on endpoint
    
    Args:
        endpoint_limits (dict): Dictionary mapping endpoints to rate limit strings
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            endpoint = request.endpoint
            limit = endpoint_limits.get(endpoint, endpoint_limits.get('default', '60 per minute'))
            
            limiter = current_app.extensions.get('limiter')
            if limiter:
                with limiter.limit(limit):
                    return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

class AdaptiveRateLimiter:
    """Adaptive rate limiting based on user behavior and system load"""
    
    def __init__(self, base_limit: str, max_limit: str, min_limit: str):
        self.base_limit = base_limit
        self.max_limit = max_limit
        self.min_limit = min_limit
    
    def get_adaptive_limit(self, user_id: Optional[str] = None) -> str:
        """
        Get adaptive rate limit based on user behavior and system load
        
        Args:
            user_id (str): User ID for personalized limits
            
        Returns:
            str: Adaptive rate limit string
        """
        # Base limit
        limit = self.base_limit
        
        # Adjust based on user reputation (if available)
        if user_id:
            reputation = self._get_user_reputation(user_id)
            if reputation > 0.8:  # High reputation users get higher limits
                limit = self.max_limit
            elif reputation < 0.3:  # Low reputation users get lower limits
                limit = self.min_limit
        
        # Adjust based on system load
        system_load = self._get_system_load()
        if system_load > 0.8:  # High system load
            limit = self.min_limit
        elif system_load < 0.3:  # Low system load
            limit = self.max_limit
        
        return limit
    
    def _get_user_reputation(self, user_id: str) -> float:
        """Get user reputation score (0.0 to 1.0)"""
        try:
            from models.user import User
            user = User.query.get(user_id)
            if user:
                # Calculate reputation based on various factors
                factors = []
                
                # Account age (older accounts get higher reputation)
                if hasattr(user, 'created_at'):
                    age_days = (time.time() - user.created_at.timestamp()) / 86400
                    factors.append(min(age_days / 365, 1.0))  # Max 1 year
                
                # Activity level
                if hasattr(user, 'last_login'):
                    days_since_login = (time.time() - user.last_login.timestamp()) / 86400
                    factors.append(max(0, 1 - days_since_login / 30))  # Decay over 30 days
                
                # Completion rate
                if hasattr(user, 'completed_modules') and hasattr(user, 'total_modules'):
                    if user.total_modules > 0:
                        factors.append(user.completed_modules / user.total_modules)
                
                # No violations
                if hasattr(user, 'violations'):
                    factors.append(max(0, 1 - user.violations / 10))  # Decay with violations
                
                return sum(factors) / len(factors) if factors else 0.5
        except Exception:
            pass
        
        return 0.5  # Default reputation
    
    def _get_system_load(self) -> float:
        """Get current system load (0.0 to 1.0)"""
        try:
            import psutil
            return psutil.cpu_percent() / 100.0
        except ImportError:
            return 0.5  # Default load

def create_adaptive_rate_limiter(base_limit: str, max_limit: str, min_limit: str):
    """Create an adaptive rate limiter"""
    return AdaptiveRateLimiter(base_limit, max_limit, min_limit)

# Predefined rate limit decorators for common use cases
def auth_rate_limit(f):
    """Rate limit for authentication endpoints"""
    return rate_limit_by_ip(RateLimitConfig.AUTH_LOGIN)(f)

def sensitive_rate_limit(f):
    """Rate limit for sensitive operations"""
    return rate_limit_by_user_id("10 per minute")(f)

def admin_rate_limit(f):
    """Rate limit for admin operations"""
    return rate_limit_by_user_role({
        'admin': '60 per minute',
        'moderator': '30 per minute',
        'user': '10 per minute',
        'anonymous': '5 per minute'
    })(f)

def api_rate_limit(f):
    """Rate limit for API endpoints"""
    return rate_limit_by_user_id("100 per hour")(f)

def file_upload_rate_limit(f):
    """Rate limit for file uploads"""
    return rate_limit_by_user_id(RateLimitConfig.FILE_UPLOAD)(f)

def search_rate_limit(f):
    """Rate limit for search operations"""
    return rate_limit_by_user_id("60 per minute")(f) 