from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LeaderboardEntry(db.Model):
    """Leaderboard entry model for user rankings"""
    __tablename__ = 'leaderboard_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    total_score = db.Column(db.Integer, default=0)
    modules_completed = db.Column(db.Integer, default=0)
    challenges_completed = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update_score(self, score):
        """Update total score"""
        self.total_score = score
        self.last_updated = datetime.utcnow()
        db.session.commit()
    
    def update_completed_counts(self, modules_count, challenges_count):
        """Update completed counts"""
        self.modules_completed = modules_count
        self.challenges_completed = challenges_count
        self.last_updated = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert leaderboard entry to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_score': self.total_score,
            'modules_completed': self.modules_completed,
            'challenges_completed': self.challenges_completed,
            'rank': self.rank,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    def to_dict_with_user(self):
        """Convert leaderboard entry to dictionary including user info"""
        entry_dict = self.to_dict()
        if hasattr(self, 'user') and self.user:
            entry_dict['user'] = {
                'username': self.user.username,
                'level': self.user.level,
                'rank': self.user.rank,
                'avatar_url': self.user.avatar_url
            }
        return entry_dict
    
    @classmethod
    def get_top_players(cls, limit=10):
        """Get top players by score"""
        return cls.query.order_by(cls.total_score.desc()).limit(limit).all()
    
    @classmethod
    def get_user_rank(cls, user_id):
        """Get user's current rank"""
        entry = cls.query.filter_by(user_id=user_id).first()
        if entry:
            # Calculate rank based on total score
            higher_scores = cls.query.filter(cls.total_score > entry.total_score).count()
            return higher_scores + 1
        return None
    
    @classmethod
    def update_all_ranks(cls):
        """Update ranks for all entries based on total score"""
        entries = cls.query.order_by(cls.total_score.desc()).all()
        for i, entry in enumerate(entries):
            entry.rank = i + 1
        db.session.commit()
    
    @classmethod
    def get_leaderboard(cls, limit=50):
        """Get leaderboard with user information"""
        return cls.query.order_by(cls.total_score.desc()).limit(limit).all()
    
    def __repr__(self):
        return f'<LeaderboardEntry {self.id} for User {self.user_id}>' 