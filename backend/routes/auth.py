from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash
import re
import requests
from datetime import datetime

from models.user import User, db
from utils.validators import (
    validate_email, validate_password, validate_username, 
    sanitize_user_input, validate_json_data, ValidationError
)
from utils.rate_limiting import auth_rate_limit, sensitive_rate_limit

auth_bp = Blueprint('auth', __name__)

# Rate limiting for auth endpoints
limiter = Limiter(key_func=get_remote_address)

@auth_bp.route('/register', methods=['POST'])
@auth_rate_limit
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate and sanitize input data
        try:
            validated_data = validate_json_data(
                data,
                required_fields=['username', 'email', 'password'],
                optional_fields={
                    'first_name': str,
                    'last_name': str
                }
            )
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        
        # Sanitize and validate individual fields
        username = sanitize_user_input(validated_data['username'], 'username')
        email = sanitize_user_input(validated_data['email'], 'email')
        password = validated_data['password']  # Don't sanitize password
        first_name = sanitize_user_input(validated_data.get('first_name', ''), 'text')
        last_name = sanitize_user_input(validated_data.get('last_name', ''), 'text')
        
        # Validate sanitized input
        if not username:
            return jsonify({'error': 'Invalid username format'}), 400
        
        if not email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 8 characters long with uppercase, lowercase, digit, and special character'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
@auth_rate_limit
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate and sanitize input data
        try:
            validated_data = validate_json_data(
                data,
                required_fields=['password'],
                optional_fields={
                    'username': str,
                    'email': str
                }
            )
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        
        # Check if login with username or email
        identifier = validated_data.get('username') or validated_data.get('email')
        password = validated_data['password']
        
        if not identifier or not password:
            return jsonify({'error': 'Username/email and password are required'}), 400
        
        # Sanitize identifier
        identifier = sanitize_user_input(identifier, 'text')
        
        # Find user
        if '@' in identifier:
            user = User.query.filter_by(email=identifier.lower()).first()
        else:
            user = User.query.filter_by(username=identifier).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Update last login
        user.update_last_login()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@sensitive_rate_limit
def logout():
    """User logout endpoint"""
    try:
        # In a real application, you might want to blacklist the token
        # For now, we'll just return a success message
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@sensitive_rate_limit
def refresh():
    """Refresh access token endpoint"""
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
    except Exception as e:
        return jsonify({'error': 'Token refresh failed'}), 500

@auth_bp.route('/google', methods=['POST'])
@limiter.limit("10 per minute")
def google_oauth():
    """Google OAuth login endpoint"""
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        
        if not access_token:
            return jsonify({'error': 'Access token required'}), 400
        
        # Verify token with Google
        google_response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if google_response.status_code != 200:
            return jsonify({'error': 'Invalid Google token'}), 401
        
        google_user = google_response.json()
        
        # Check if user exists
        user = User.query.filter_by(oauth_provider='google', oauth_id=google_user['id']).first()
        
        if not user:
            # Create new user
            user = User(
                username=google_user['email'].split('@')[0],
                email=google_user['email'],
                first_name=google_user.get('given_name', ''),
                last_name=google_user.get('family_name', ''),
                avatar_url=google_user.get('picture'),
                oauth_provider='google',
                oauth_id=google_user['id'],
                email_verified=True
            )
            db.session.add(user)
            db.session.commit()
        
        # Update last login
        user.update_last_login()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Google login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Google login failed'}), 500

@auth_bp.route('/github', methods=['POST'])
@limiter.limit("10 per minute")
def github_oauth():
    """GitHub OAuth login endpoint"""
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        
        if not access_token:
            return jsonify({'error': 'Access token required'}), 400
        
        # Verify token with GitHub
        github_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        
        if github_response.status_code != 200:
            return jsonify({'error': 'Invalid GitHub token'}), 401
        
        github_user = github_response.json()
        
        # Get user email
        email_response = requests.get(
            'https://api.github.com/user/emails',
            headers={'Authorization': f'token {access_token}'}
        )
        
        if email_response.status_code == 200:
            emails = email_response.json()
            primary_email = next((email['email'] for email in emails if email['primary']), None)
        else:
            primary_email = github_user.get('email')
        
        # Check if user exists
        user = User.query.filter_by(oauth_provider='github', oauth_id=str(github_user['id'])).first()
        
        if not user:
            # Create new user
            user = User(
                username=github_user['login'],
                email=primary_email or f"{github_user['login']}@github.com",
                first_name=github_user.get('name', '').split()[0] if github_user.get('name') else '',
                last_name=' '.join(github_user.get('name', '').split()[1:]) if github_user.get('name') else '',
                avatar_url=github_user.get('avatar_url'),
                oauth_provider='github',
                oauth_id=str(github_user['id']),
                email_verified=bool(primary_email)
            )
            db.session.add(user)
            db.session.commit()
        
        # Update last login
        user.update_last_login()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'GitHub login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'GitHub login failed'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get user information'}), 500 