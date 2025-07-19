from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    rank = db.Column(db.String(50), default='Novice')
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    oauth_provider = db.Column(db.String(20))  # 'google', 'github', etc.
    oauth_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    leaderboard_entries = db.relationship('LeaderboardEntry', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password=None, **kwargs):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'level': self.level,
            'experience': self.experience,
            'rank': self.rank,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'email_verified': self.email_verified,
            'oauth_provider': self.oauth_provider,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def add_experience(self, points):
        """Add experience points and update level"""
        self.experience += points
        self.level = (self.experience // 100) + 1
        
        # Update rank based on level
        if self.level >= 20:
            self.rank = 'Master'
        elif self.level >= 15:
            self.rank = 'Expert'
        elif self.level >= 10:
            self.rank = 'Advanced'
        elif self.level >= 5:
            self.rank = 'Intermediate'
        else:
            self.rank = 'Novice'
        
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>' 