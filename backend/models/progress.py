from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserProgress(db.Model):
    """User progress tracking model"""
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)
    
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def mark_completed(self, score=0):
        """Mark progress as completed"""
        self.completed = True
        self.completed_at = datetime.utcnow()
        self.score = score
        db.session.commit()
    
    def increment_attempts(self):
        """Increment attempt counter"""
        self.attempts += 1
        db.session.commit()
    
    def add_time_spent(self, seconds):
        """Add time spent on this item"""
        self.time_spent += seconds
        db.session.commit()
    
    def to_dict(self):
        """Convert progress to dictionary for API responses"""
        return {
            'id': self.id,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'score': self.score,
            'attempts': self.attempts,
            'time_spent': self.time_spent,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'challenge_id': self.challenge_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_user_module_progress(cls, user_id, module_id):
        """Get user progress for a specific module"""
        return cls.query.filter_by(user_id=user_id, module_id=module_id).first()
    
    @classmethod
    def get_user_challenge_progress(cls, user_id, challenge_id):
        """Get user progress for a specific challenge"""
        return cls.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    
    @classmethod
    def get_user_all_progress(cls, user_id):
        """Get all progress for a user"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_completed_modules(cls, user_id):
        """Get all completed modules for a user"""
        return cls.query.filter_by(user_id=user_id, completed=True).filter(cls.module_id.isnot(None)).all()
    
    @classmethod
    def get_completed_challenges(cls, user_id):
        """Get all completed challenges for a user"""
        return cls.query.filter_by(user_id=user_id, completed=True).filter(cls.challenge_id.isnot(None)).all()
    
    def __repr__(self):
        return f'<UserProgress {self.id} for User {self.user_id}>' 