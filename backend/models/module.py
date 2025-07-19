from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Module(db.Model):
    """Learning module model"""
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='Beginner')  # Beginner, Intermediate, Advanced
    category = db.Column(db.String(50), nullable=False)  # Cryptography, Web Security, etc.
    order = db.Column(db.Integer, default=0)
    estimated_time = db.Column(db.Integer)  # in minutes
    points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    challenges = db.relationship('Challenge', backref='module', lazy='dynamic', cascade='all, delete-orphan')
    progress = db.relationship('UserProgress', backref='module', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert module to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'difficulty': self.difficulty,
            'category': self.category,
            'order': self.order,
            'estimated_time': self.estimated_time,
            'points': self.points,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'challenge_count': self.challenges.count()
        }
    
    def to_dict_with_challenges(self):
        """Convert module to dictionary including challenges"""
        module_dict = self.to_dict()
        module_dict['challenges'] = [challenge.to_dict() for challenge in self.challenges.all()]
        return module_dict
    
    @classmethod
    def get_by_category(cls, category):
        """Get all modules by category"""
        return cls.query.filter_by(category=category, is_active=True).order_by(cls.order).all()
    
    @classmethod
    def get_by_difficulty(cls, difficulty):
        """Get all modules by difficulty"""
        return cls.query.filter_by(difficulty=difficulty, is_active=True).order_by(cls.order).all()
    
    def __repr__(self):
        return f'<Module {self.title}>' 