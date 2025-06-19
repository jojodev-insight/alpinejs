"""
Main application routes for dashboard and expense management
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense, Category
from datetime import datetime, timedelta
from sqlalchemy import func, extract

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise show landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with expense overview"""
    # Get current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    # Get this month's expenses
    monthly_expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        extract('year', Expense.date) == current_year,
        extract('month', Expense.date) == current_month
    ).all()
    
    # Calculate monthly total
    monthly_total = sum(float(expense.amount) for expense in monthly_expenses)
    
    # Get recent expenses (last 10)
    recent_expenses = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.created_at.desc()).limit(10).all()
    
    # Get monthly summary by category
    monthly_summary = Expense.get_monthly_summary(current_user.id, current_year, current_month)
    
    # Get expense count
    total_expenses = Expense.query.filter_by(user_id=current_user.id).count()
    
    # Get categories for the form
    categories = Category.query.all()
    
    return render_template('dashboard.html', 
                         monthly_total=monthly_total,
                         monthly_expenses=monthly_expenses,
                         recent_expenses=recent_expenses,
                         monthly_summary=monthly_summary,
                         total_expenses=total_expenses,
                         categories=categories,
                         current_month=now.strftime('%B'),
                         current_year=current_year)


@main_bp.route('/expenses')
@login_required
def expenses():
    """Expenses list page with filtering and search"""
    categories = Category.query.all()
    return render_template('expenses.html', categories=categories)


@main_bp.route('/analytics')
@login_required
def analytics():
    """Analytics page with charts and reports"""
    # Get current year data
    current_year = datetime.now().year
    yearly_summary = Expense.get_yearly_summary(current_user.id, current_year)
    
    # Get top categories
    top_categories = db.session.query(
        Category.name.label('category'),
        Category.color.label('color'),
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('count')
    ).join(Category).filter(
        Expense.user_id == current_user.id
    ).group_by(Category.name, Category.color)\
     .order_by(func.sum(Expense.amount).desc()).limit(10).all()
    
    return render_template('analytics.html',
                         yearly_summary=yearly_summary,
                         top_categories=top_categories,
                         current_year=current_year)


@main_bp.route('/categories')
@login_required
def categories():
    """Categories management page"""
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@main_bp.route('/export')
@login_required
def export():
    """Export data page"""
    return render_template('export.html')
