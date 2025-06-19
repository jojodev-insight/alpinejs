"""
Expense model for tracking expenses
"""
from app import db
from datetime import datetime
from sqlalchemy import func


class Category(db.Model):
    """Category model for expense categorization"""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    color = db.Column(db.String(7), default='#007bff')  # Hex color code
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship with expenses
    expenses = db.relationship('Expense', backref='category', lazy=True)
    
    def to_dict(self):
        """Convert category object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Expense(db.Model):
    """Expense model for tracking individual expenses"""
    
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Indexes for better performance
    __table_args__ = (
        db.Index('idx_user_date', 'user_id', 'date'),
        db.Index('idx_user_category', 'user_id', 'category_id'),
    )
    
    def to_dict(self):
        """Convert expense object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'amount': float(self.amount),
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None
        }
    
    @staticmethod
    def get_monthly_summary(user_id, year, month):
        """Get monthly expense summary for a user"""
        return db.session.query(
            Category.name.label('category'),
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).join(Category).filter(
            Expense.user_id == user_id,
            func.extract('year', Expense.date) == year,
            func.extract('month', Expense.date) == month
        ).group_by(Category.name).all()
    
    @staticmethod
    def get_yearly_summary(user_id, year):
        """Get yearly expense summary for a user"""
        return db.session.query(
            func.extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).filter(
            Expense.user_id == user_id,
            func.extract('year', Expense.date) == year
        ).group_by(func.extract('month', Expense.date)).all()
    
    def __repr__(self):
        return f'<Expense {self.title}: ${self.amount}>'
