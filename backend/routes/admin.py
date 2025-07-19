from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.user import User, db
from models.module import Module
from models.challenge import Challenge, Flag
from models.progress import UserProgress
from models.leaderboard import LeaderboardEntry
from utils.validators import sanitize_input

admin_bp = Blueprint('admin', __name__)
limiter = Limiter(key_func=get_remote_address)

def admin_required(f):
    """Decorator to check if user is admin"""
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard():
    """Get admin dashboard statistics"""
    try:
        # Get basic statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_modules = Module.query.count()
        active_modules = Module.query.filter_by(is_active=True).count()
        total_challenges = Challenge.query.count()
        active_challenges = Challenge.query.filter_by(is_active=True).count()
        
        # Get recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_progress = UserProgress.query.order_by(UserProgress.created_at.desc()).limit(10).all()
        
        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'total_modules': total_modules,
            'active_modules': active_modules,
            'total_challenges': total_challenges,
            'active_challenges': active_challenges,
            'recent_users': [user.to_dict() for user in recent_users],
            'recent_progress': [progress.to_dict() for progress in recent_progress]
        }
        
        return jsonify({
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get dashboard stats'}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get all users (admin only)"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        search = request.args.get('search', '')
        
        # Build query
        query = User.query
        
        if search:
            query = query.filter(
                db.or_(
                    User.username.contains(search),
                    User.email.contains(search)
                )
            )
        
        # Apply pagination
        users = query.offset(offset).limit(limit).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': query.count(),
            'limit': limit,
            'offset': offset
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
@limiter.limit("10 per minute")
def update_user(user_id):
    """Update user (admin only)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update allowed fields
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        
        if 'level' in data:
            user.level = data['level']
        
        if 'experience' in data:
            user.experience = data['experience']
        
        if 'rank' in data:
            user.rank = data['rank']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user'}), 500

@admin_bp.route('/modules', methods=['POST'])
@jwt_required()
@admin_required
@limiter.limit("5 per minute")
def create_module():
    """Create new module (admin only)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'category']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new module
        module = Module(
            title=sanitize_input(data['title']),
            description=sanitize_input(data['description']),
            content=sanitize_input(data.get('content', '')),
            category=data['category'],
            difficulty=data.get('difficulty', 'Beginner'),
            order=data.get('order', 0),
            estimated_time=data.get('estimated_time'),
            points=data.get('points', 10)
        )
        
        db.session.add(module)
        db.session.commit()
        
        return jsonify({
            'message': 'Module created successfully',
            'module': module.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create module'}), 500

@admin_bp.route('/modules/<int:module_id>', methods=['PUT'])
@jwt_required()
@admin_required
@limiter.limit("10 per minute")
def update_module(module_id):
    """Update module (admin only)"""
    try:
        module = Module.query.get(module_id)
        if not module:
            return jsonify({'error': 'Module not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'title' in data:
            module.title = sanitize_input(data['title'])
        
        if 'description' in data:
            module.description = sanitize_input(data['description'])
        
        if 'content' in data:
            module.content = sanitize_input(data['content'])
        
        if 'category' in data:
            module.category = data['category']
        
        if 'difficulty' in data:
            module.difficulty = data['difficulty']
        
        if 'order' in data:
            module.order = data['order']
        
        if 'estimated_time' in data:
            module.estimated_time = data['estimated_time']
        
        if 'points' in data:
            module.points = data['points']
        
        if 'is_active' in data:
            module.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Module updated successfully',
            'module': module.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update module'}), 500

@admin_bp.route('/challenges', methods=['POST'])
@jwt_required()
@admin_required
@limiter.limit("5 per minute")
def create_challenge():
    """Create new challenge (admin only)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'module_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if module exists
        module = Module.query.get(data['module_id'])
        if not module:
            return jsonify({'error': 'Module not found'}), 404
        
        # Create new challenge
        challenge = Challenge(
            title=sanitize_input(data['title']),
            description=sanitize_input(data['description']),
            category=data['category'],
            difficulty=data.get('difficulty', 'Easy'),
            points=data.get('points', 10),
            hints=data.get('hints', []),
            files=data.get('files', []),
            module_id=data['module_id']
        )
        
        db.session.add(challenge)
        db.session.commit()
        
        # Add flags if provided
        if 'flags' in data and isinstance(data['flags'], list):
            for flag_data in data['flags']:
                flag = Flag(
                    flag_value=flag_data['value'],
                    flag_type=flag_data.get('type', 'exact'),
                    points=flag_data.get('points', 10),
                    challenge_id=challenge.id
                )
                db.session.add(flag)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Challenge created successfully',
            'challenge': challenge.to_dict_with_flags()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create challenge'}), 500

@admin_bp.route('/challenges/<int:challenge_id>', methods=['PUT'])
@jwt_required()
@admin_required
@limiter.limit("10 per minute")
def update_challenge(challenge_id):
    """Update challenge (admin only)"""
    try:
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'title' in data:
            challenge.title = sanitize_input(data['title'])
        
        if 'description' in data:
            challenge.description = sanitize_input(data['description'])
        
        if 'category' in data:
            challenge.category = data['category']
        
        if 'difficulty' in data:
            challenge.difficulty = data['difficulty']
        
        if 'points' in data:
            challenge.points = data['points']
        
        if 'hints' in data:
            challenge.hints = data['hints']
        
        if 'files' in data:
            challenge.files = data['files']
        
        if 'is_active' in data:
            challenge.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Challenge updated successfully',
            'challenge': challenge.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update challenge'}), 500

@admin_bp.route('/challenges/<int:challenge_id>/flags', methods=['POST'])
@jwt_required()
@admin_required
@limiter.limit("10 per minute")
def add_flag(challenge_id):
    """Add flag to challenge (admin only)"""
    try:
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        data = request.get_json()
        if not data or 'flag_value' not in data:
            return jsonify({'error': 'Flag value is required'}), 400
        
        # Create new flag
        flag = Flag(
            flag_value=data['flag_value'],
            flag_type=data.get('flag_type', 'exact'),
            points=data.get('points', 10),
            challenge_id=challenge_id
        )
        
        db.session.add(flag)
        db.session.commit()
        
        return jsonify({
            'message': 'Flag added successfully',
            'flag': flag.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add flag'}), 500

@admin_bp.route('/system/update-ranks', methods=['POST'])
@jwt_required()
@admin_required
@limiter.limit("1 per minute")
def update_ranks():
    """Update all user ranks (admin only)"""
    try:
        # Update all ranks
        LeaderboardEntry.update_all_ranks()
        
        return jsonify({
            'message': 'Ranks updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update ranks'}), 500 