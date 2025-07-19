from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Challenge(db.Model):
    """CTF Challenge model"""
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Web, Crypto, Forensics, etc.
    difficulty = db.Column(db.String(20), default='Easy')  # Easy, Medium, Hard
    points = db.Column(db.Integer, default=10)
    hints = db.Column(db.JSON)  # List of hints
    files = db.Column(db.JSON)  # List of file URLs
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # Relationships
    flags = db.relationship('Flag', backref='challenge', lazy='dynamic', cascade='all, delete-orphan')
    progress = db.relationship('UserProgress', backref='challenge', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert challenge to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'points': self.points,
            'hints': self.hints,
            'files': self.files,
            'is_active': self.is_active,
            'module_id': self.module_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'flag_count': self.flags.count()
        }
    
    def to_dict_with_flags(self):
        """Convert challenge to dictionary including flags (admin only)"""
        challenge_dict = self.to_dict()
        challenge_dict['flags'] = [flag.to_dict() for flag in self.flags.all()]
        return challenge_dict
    
    @classmethod
    def get_by_category(cls, category):
        """Get all challenges by category"""
        return cls.query.filter_by(category=category, is_active=True).all()
    
    @classmethod
    def get_by_difficulty(cls, difficulty):
        """Get all challenges by difficulty"""
        return cls.query.filter_by(difficulty=difficulty, is_active=True).all()
    
    @classmethod
    def get_by_module(cls, module_id):
        """Get all challenges for a specific module"""
        return cls.query.filter_by(module_id=module_id, is_active=True).all()
    
    def __repr__(self):
        return f'<Challenge {self.title}>'

class Flag(db.Model):
    """Flag model for challenge solutions"""
    __tablename__ = 'flags'
    
    id = db.Column(db.Integer, primary_key=True)
    flag_value = db.Column(db.String(255), nullable=False)
    flag_type = db.Column(db.String(20), default='exact')  # exact, regex, contains
    points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    
    def to_dict(self):
        """Convert flag to dictionary for API responses"""
        return {
            'id': self.id,
            'flag_type': self.flag_type,
            'points': self.points,
            'is_active': self.is_active,
            'challenge_id': self.challenge_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def check_flag(self, submitted_flag):
        """Check if submitted flag matches"""
        if not self.is_active:
            return False
            
        if self.flag_type == 'exact':
            return submitted_flag.strip() == self.flag_value.strip()
        elif self.flag_type == 'regex':
            import re
            try:
                return bool(re.match(self.flag_value, submitted_flag.strip()))
            except re.error:
                return False
        elif self.flag_type == 'contains':
            return self.flag_value.lower() in submitted_flag.lower()
        
        return False
    
    def __repr__(self):
        return f'<Flag {self.id} for Challenge {self.challenge_id}>' 