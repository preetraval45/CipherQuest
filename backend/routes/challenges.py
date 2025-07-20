from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.challenge import Challenge, Flag, db
from models.progress import UserProgress
from models.user import User
from utils.validators import validate_flag_format, sanitize_user_input, validate_json_data, ValidationError
from utils.rate_limiting import sensitive_rate_limit, api_rate_limit

challenges_bp = Blueprint('challenges', __name__)
limiter = Limiter(key_func=get_remote_address)

@challenges_bp.route('/', methods=['GET'])
@jwt_required()
def get_challenges():
    """Get all CTF challenges"""
    try:
        # Get query parameters
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        module_id = request.args.get('module_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Build query
        query = Challenge.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        if module_id:
            query = query.filter_by(module_id=module_id)
        
        # Apply pagination
        challenges = query.offset(offset).limit(limit).all()
        
        # Get current user for progress tracking
        current_user_id = get_jwt_identity()
        
        # Add progress information to each challenge
        challenges_with_progress = []
        for challenge in challenges:
            challenge_data = challenge.to_dict()
            
            # Get user progress for this challenge
            progress = UserProgress.get_user_challenge_progress(current_user_id, challenge.id)
            if progress:
                challenge_data['user_progress'] = progress.to_dict()
            else:
                challenge_data['user_progress'] = None
            
            challenges_with_progress.append(challenge_data)
        
        return jsonify({
            'challenges': challenges_with_progress,
            'total': query.count(),
            'limit': limit,
            'offset': offset
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch challenges'}), 500

@challenges_bp.route('/<int:challenge_id>', methods=['GET'])
@jwt_required()
def get_challenge(challenge_id):
    """Get specific challenge details"""
    try:
        challenge = Challenge.query.filter_by(id=challenge_id, is_active=True).first()
        
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Get user progress for this challenge
        progress = UserProgress.get_user_challenge_progress(current_user_id, challenge_id)
        
        challenge_data = challenge.to_dict()
        
        if progress:
            challenge_data['user_progress'] = progress.to_dict()
        else:
            challenge_data['user_progress'] = None
        
        return jsonify({
            'challenge': challenge_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch challenge'}), 500

@challenges_bp.route('/<int:challenge_id>/submit', methods=['POST'])
@jwt_required()
@sensitive_rate_limit
def submit_flag(challenge_id):
    """Submit flag for a challenge"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate and sanitize input data
        try:
            validated_data = validate_json_data(
                data,
                required_fields=['flag']
            )
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        
        # Sanitize and validate flag
        submitted_flag = sanitize_user_input(validated_data['flag'], 'flag')
        
        if not submitted_flag:
            return jsonify({'error': 'Invalid flag format'}), 400
        
        # Check if challenge exists
        challenge = Challenge.query.filter_by(id=challenge_id, is_active=True).first()
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Get or create progress entry
        progress = UserProgress.get_user_challenge_progress(current_user_id, challenge_id)
        
        if not progress:
            progress = UserProgress(
                user_id=current_user_id,
                challenge_id=challenge_id
            )
            db.session.add(progress)
        
        # Increment attempts
        progress.increment_attempts()
        
        # Check if flag is correct
        flags = Flag.query.filter_by(challenge_id=challenge_id, is_active=True).all()
        correct_flag = None
        
        for flag in flags:
            if flag.check_flag(submitted_flag):
                correct_flag = flag
                break
        
        if correct_flag:
            # Mark as completed if not already
            if not progress.completed:
                progress.mark_completed(correct_flag.points)
                
                # Update user experience
                user = User.query.get(current_user_id)
                user.add_experience(correct_flag.points)
                
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
                'success': True,
                'message': 'Flag is correct!',
                'points_earned': correct_flag.points,
                'progress': progress.to_dict()
            }), 200
        else:
            db.session.commit()
            
            return jsonify({
                'success': False,
                'message': 'Incorrect flag. Try again!',
                'attempts': progress.attempts
            }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit flag'}), 500

@challenges_bp.route('/<int:challenge_id>/hint', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")
def get_hint(challenge_id):
    """Get hint for a challenge"""
    try:
        challenge = Challenge.query.filter_by(id=challenge_id, is_active=True).first()
        
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        if not challenge.hints:
            return jsonify({'error': 'No hints available for this challenge'}), 404
        
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Get user progress to track hint usage
        progress = UserProgress.get_user_challenge_progress(current_user_id, challenge_id)
        
        if not progress:
            progress = UserProgress(
                user_id=current_user_id,
                challenge_id=challenge_id
            )
            db.session.add(progress)
        
        # For now, return the first hint
        # In a more advanced implementation, you might want to unlock hints progressively
        hint = challenge.hints[0] if isinstance(challenge.hints, list) else challenge.hints
        
        return jsonify({
            'hint': hint,
            'total_hints': len(challenge.hints) if isinstance(challenge.hints, list) else 1
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get hint'}), 500

@challenges_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all challenge categories"""
    try:
        categories = db.session.query(Challenge.category).distinct().filter_by(is_active=True).all()
        category_list = [cat[0] for cat in categories]
        
        return jsonify({
            'categories': category_list
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories'}), 500

@challenges_bp.route('/difficulties', methods=['GET'])
@jwt_required()
def get_difficulties():
    """Get all challenge difficulties"""
    try:
        difficulties = db.session.query(Challenge.difficulty).distinct().filter_by(is_active=True).all()
        difficulty_list = [diff[0] for diff in difficulties]
        
        return jsonify({
            'difficulties': difficulty_list
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch difficulties'}), 500

@challenges_bp.route('/<int:challenge_id>/progress', methods=['PUT'])
@jwt_required()
@limiter.limit("30 per minute")
def update_challenge_progress(challenge_id):
    """Update challenge progress (time spent, etc.)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if challenge exists
        challenge = Challenge.query.filter_by(id=challenge_id, is_active=True).first()
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Get or create progress entry
        progress = UserProgress.get_user_challenge_progress(current_user_id, challenge_id)
        
        if not progress:
            progress = UserProgress(
                user_id=current_user_id,
                challenge_id=challenge_id
            )
            db.session.add(progress)
        
        # Update progress fields
        if 'time_spent' in data:
            progress.add_time_spent(data['time_spent'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progress updated successfully',
            'progress': progress.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update progress'}), 500 