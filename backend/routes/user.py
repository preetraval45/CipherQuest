from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.user import User, db
from models.progress import UserProgress
from models.leaderboard import LeaderboardEntry
from utils.validators import validate_email, validate_username, sanitize_input

user_bp = Blueprint('user', __name__)
limiter = Limiter(key_func=get_remote_address)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get profile'}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per minute")
def update_profile():
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = sanitize_input(data['first_name'])
        
        if 'last_name' in data:
            user.last_name = sanitize_input(data['last_name'])
        
        if 'bio' in data:
            user.bio = sanitize_input(data['bio'])
        
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@user_bp.route('/password', methods=['PUT'])
@jwt_required()
@limiter.limit("5 per minute")
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Set new password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to change password'}), 500

@user_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Get user progress"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get all progress for user
        progress = UserProgress.get_user_all_progress(current_user_id)
        
        # Get completed modules and challenges
        completed_modules = UserProgress.get_completed_modules(current_user_id)
        completed_challenges = UserProgress.get_completed_challenges(current_user_id)
        
        # Get leaderboard entry
        leaderboard_entry = LeaderboardEntry.query.filter_by(user_id=current_user_id).first()
        
        return jsonify({
            'progress': [p.to_dict() for p in progress],
            'completed_modules': len(completed_modules),
            'completed_challenges': len(completed_challenges),
            'leaderboard': leaderboard_entry.to_dict() if leaderboard_entry else None
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get progress'}), 500

@user_bp.route('/progress/<int:module_id>', methods=['GET'])
@jwt_required()
def get_module_progress(module_id):
    """Get user progress for specific module"""
    try:
        current_user_id = get_jwt_identity()
        
        progress = UserProgress.get_user_module_progress(current_user_id, module_id)
        
        if not progress:
            return jsonify({
                'progress': None,
                'message': 'No progress found for this module'
            }), 200
        
        return jsonify({
            'progress': progress.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get module progress'}), 500

@user_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get user statistics"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get progress statistics
        completed_modules = UserProgress.get_completed_modules(current_user_id)
        completed_challenges = UserProgress.get_completed_challenges(current_user_id)
        
        # Calculate total time spent
        all_progress = UserProgress.get_user_all_progress(current_user_id)
        total_time = sum(p.time_spent for p in all_progress)
        
        # Get leaderboard entry
        leaderboard_entry = LeaderboardEntry.query.filter_by(user_id=current_user_id).first()
        
        stats = {
            'level': user.level,
            'experience': user.experience,
            'rank': user.rank,
            'modules_completed': len(completed_modules),
            'challenges_completed': len(completed_challenges),
            'total_time_spent': total_time,
            'total_score': leaderboard_entry.total_score if leaderboard_entry else 0,
            'leaderboard_rank': leaderboard_entry.rank if leaderboard_entry else None
        }
        
        return jsonify({
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get statistics'}), 500 