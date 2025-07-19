from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.leaderboard import LeaderboardEntry, db
from models.user import User

leaderboard_bp = Blueprint('leaderboard', __name__)
limiter = Limiter(key_func=get_remote_address)

@leaderboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """Get leaderboard rankings"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get leaderboard entries with user information
        entries = LeaderboardEntry.query.order_by(LeaderboardEntry.total_score.desc()).offset(offset).limit(limit).all()
        
        # Convert to dictionary with user info
        leaderboard_data = []
        for entry in entries:
            entry_dict = entry.to_dict_with_user()
            leaderboard_data.append(entry_dict)
        
        return jsonify({
            'leaderboard': leaderboard_data,
            'total': LeaderboardEntry.query.count(),
            'limit': limit,
            'offset': offset
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch leaderboard'}), 500

@leaderboard_bp.route('/top', methods=['GET'])
@jwt_required()
def get_top_players():
    """Get top players"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get top players
        top_entries = LeaderboardEntry.get_top_players(limit)
        
        # Convert to dictionary with user info
        top_players = []
        for entry in top_entries:
            entry_dict = entry.to_dict_with_user()
            top_players.append(entry_dict)
        
        return jsonify({
            'top_players': top_players
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch top players'}), 500

@leaderboard_bp.route('/my-rank', methods=['GET'])
@jwt_required()
def get_my_rank():
    """Get current user's rank"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's leaderboard entry
        entry = LeaderboardEntry.query.filter_by(user_id=current_user_id).first()
        
        if not entry:
            return jsonify({
                'rank': None,
                'message': 'No ranking data available'
            }), 200
        
        # Get user info
        user = User.query.get(current_user_id)
        
        rank_data = {
            'rank': entry.rank,
            'total_score': entry.total_score,
            'modules_completed': entry.modules_completed,
            'challenges_completed': entry.challenges_completed,
            'user': {
                'username': user.username,
                'level': user.level,
                'rank': user.rank,
                'avatar_url': user.avatar_url
            }
        }
        
        return jsonify({
            'rank_data': rank_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get rank'}), 500

@leaderboard_bp.route('/around-me', methods=['GET'])
@jwt_required()
def get_around_me():
    """Get players around current user's rank"""
    try:
        current_user_id = get_jwt_identity()
        range_size = request.args.get('range', 5, type=int)
        
        # Get user's leaderboard entry
        user_entry = LeaderboardEntry.query.filter_by(user_id=current_user_id).first()
        
        if not user_entry:
            return jsonify({
                'around_me': [],
                'message': 'No ranking data available'
            }), 200
        
        # Calculate range
        start_rank = max(1, user_entry.rank - range_size)
        end_rank = user_entry.rank + range_size
        
        # Get entries in range
        entries = LeaderboardEntry.query.filter(
            LeaderboardEntry.rank >= start_rank,
            LeaderboardEntry.rank <= end_rank
        ).order_by(LeaderboardEntry.rank).all()
        
        # Convert to dictionary with user info
        around_me = []
        for entry in entries:
            entry_dict = entry.to_dict_with_user()
            around_me.append(entry_dict)
        
        return jsonify({
            'around_me': around_me,
            'my_rank': user_entry.rank,
            'range': range_size
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get players around you'}), 500

@leaderboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_leaderboard_stats():
    """Get leaderboard statistics"""
    try:
        # Get total number of players
        total_players = LeaderboardEntry.query.count()
        
        # Get average score
        avg_score = db.session.query(db.func.avg(LeaderboardEntry.total_score)).scalar() or 0
        
        # Get highest score
        highest_score = db.session.query(db.func.max(LeaderboardEntry.total_score)).scalar() or 0
        
        # Get total modules and challenges completed across all users
        total_modules = db.session.query(db.func.sum(LeaderboardEntry.modules_completed)).scalar() or 0
        total_challenges = db.session.query(db.func.sum(LeaderboardEntry.challenges_completed)).scalar() or 0
        
        stats = {
            'total_players': total_players,
            'average_score': round(avg_score, 2),
            'highest_score': highest_score,
            'total_modules_completed': total_modules,
            'total_challenges_completed': total_challenges
        }
        
        return jsonify({
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get leaderboard stats'}), 500 