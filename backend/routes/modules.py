from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.module import Module, db
from models.progress import UserProgress
from models.user import User

modules_bp = Blueprint('modules', __name__)
limiter = Limiter(key_func=get_remote_address)

@modules_bp.route('/', methods=['GET'])
@jwt_required()
def get_modules():
    """Get all learning modules"""
    try:
        # Get query parameters
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Build query
        query = Module.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        # Order by order field
        query = query.order_by(Module.order)
        
        # Apply pagination
        modules = query.offset(offset).limit(limit).all()
        
        # Get current user for progress tracking
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        # Add progress information to each module
        modules_with_progress = []
        for module in modules:
            module_data = module.to_dict()
            
            # Get user progress for this module
            progress = UserProgress.get_user_module_progress(current_user_id, module.id)
            if progress:
                module_data['user_progress'] = progress.to_dict()
            else:
                module_data['user_progress'] = None
            
            modules_with_progress.append(module_data)
        
        return jsonify({
            'modules': modules_with_progress,
            'total': query.count(),
            'limit': limit,
            'offset': offset
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch modules'}), 500

@modules_bp.route('/<int:module_id>', methods=['GET'])
@jwt_required()
def get_module(module_id):
    """Get specific module details"""
    try:
        module = Module.query.filter_by(id=module_id, is_active=True).first()
        
        if not module:
            return jsonify({'error': 'Module not found'}), 404
        
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Get user progress for this module
        progress = UserProgress.get_user_module_progress(current_user_id, module_id)
        
        # Get module with challenges
        module_data = module.to_dict_with_challenges()
        
        if progress:
            module_data['user_progress'] = progress.to_dict()
        else:
            module_data['user_progress'] = None
        
        return jsonify({
            'module': module_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch module'}), 500

@modules_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all module categories"""
    try:
        categories = db.session.query(Module.category).distinct().filter_by(is_active=True).all()
        category_list = [cat[0] for cat in categories]
        
        return jsonify({
            'categories': category_list
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories'}), 500

@modules_bp.route('/difficulties', methods=['GET'])
@jwt_required()
def get_difficulties():
    """Get all module difficulties"""
    try:
        difficulties = db.session.query(Module.difficulty).distinct().filter_by(is_active=True).all()
        difficulty_list = [diff[0] for diff in difficulties]
        
        return jsonify({
            'difficulties': difficulty_list
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch difficulties'}), 500

@modules_bp.route('/<int:module_id>/complete', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def complete_module(module_id):
    """Mark module as completed"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if module exists
        module = Module.query.filter_by(id=module_id, is_active=True).first()
        if not module:
            return jsonify({'error': 'Module not found'}), 404
        
        # Get or create progress entry
        progress = UserProgress.get_user_module_progress(current_user_id, module_id)
        
        if not progress:
            progress = UserProgress(
                user_id=current_user_id,
                module_id=module_id
            )
            db.session.add(progress)
        
        # Mark as completed
        progress.mark_completed(module.points)
        
        # Update user experience
        user = User.query.get(current_user_id)
        user.add_experience(module.points)
        
        # Update leaderboard
        from models.leaderboard import LeaderboardEntry
        leaderboard_entry = LeaderboardEntry.query.filter_by(user_id=current_user_id).first()
        
        if not leaderboard_entry:
            leaderboard_entry = LeaderboardEntry(user_id=current_user_id)
            db.session.add(leaderboard_entry)
        
        # Recalculate total score and counts
        completed_modules = UserProgress.get_completed_modules(current_user_id)
        completed_challenges = UserProgress.get_completed_challenges(current_user_id)
        
        total_score = sum([m.module.points for m in completed_modules if m.module]) + \
                     sum([c.challenge.points for c in completed_challenges if c.challenge])
        
        leaderboard_entry.update_score(total_score)
        leaderboard_entry.update_completed_counts(len(completed_modules), len(completed_challenges))
        
        db.session.commit()
        
        return jsonify({
            'message': 'Module completed successfully',
            'progress': progress.to_dict(),
            'experience_gained': module.points
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete module'}), 500

@modules_bp.route('/<int:module_id>/progress', methods=['PUT'])
@jwt_required()
@limiter.limit("30 per minute")
def update_module_progress(module_id):
    """Update module progress (time spent, attempts, etc.)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if module exists
        module = Module.query.filter_by(id=module_id, is_active=True).first()
        if not module:
            return jsonify({'error': 'Module not found'}), 404
        
        # Get or create progress entry
        progress = UserProgress.get_user_module_progress(current_user_id, module_id)
        
        if not progress:
            progress = UserProgress(
                user_id=current_user_id,
                module_id=module_id
            )
            db.session.add(progress)
        
        # Update progress fields
        if 'time_spent' in data:
            progress.add_time_spent(data['time_spent'])
        
        if 'increment_attempts' in data and data['increment_attempts']:
            progress.increment_attempts()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progress updated successfully',
            'progress': progress.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update progress'}), 500 