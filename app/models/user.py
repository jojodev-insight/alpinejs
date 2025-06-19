"""
User model for authentication
"""
from flask_sqlalchemy import SQLAlchemy  
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db
from datetime import datetime


class User(db.Model, UserMixin):
    """User model for authentication and user management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationship with expenses
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, first_name, last_name):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password).decode('utf-8')
        self.first_name = first_name
        self.last_name = last_name
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Set new password with hash"""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
