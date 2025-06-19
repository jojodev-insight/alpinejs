"""
API routes for AJAX requests and data operations
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense, Category
from app.utils.validators import validate_expense
from datetime import datetime, date
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
# import pandas as pd  # Not needed for current functionality

api_bp = Blueprint('api', __name__)


@api_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    """Get expenses with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '').strip()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build query
    query = Expense.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            Expense.title.contains(search) |
            Expense.description.contains(search)
        )
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= start_date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid start date format'}), 400
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= end_date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid end date format'}), 400
    
    # Order by date (newest first)
    query = query.order_by(Expense.date.desc(), Expense.created_at.desc())
    
    # Paginate
    expenses = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'expenses': [expense.to_dict() for expense in expenses.items],
        'pagination': {
            'page': expenses.page,
            'pages': expenses.pages,
            'per_page': expenses.per_page,
            'total': expenses.total,
            'has_next': expenses.has_next,
            'has_prev': expenses.has_prev
        }
    })


@api_bp.route('/expenses', methods=['POST'])
@login_required
def create_expense():
    """Create a new expense"""
    data = request.get_json()
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    amount = data.get('amount')
    category_id = data.get('category_id')
    date_str = data.get('date')
    
    # Validate input
    errors = validate_expense(title, amount, category_id, date_str)
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        # Parse date
        expense_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
        
        # Create expense
        expense = Expense(
            title=title,
            description=description,
            amount=float(amount),
            date=expense_date,
            user_id=current_user.id,
            category_id=int(category_id)
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': 'Expense created successfully',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create expense'}), 500


@api_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    """Update an existing expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    data = request.get_json()
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    amount = data.get('amount')
    category_id = data.get('category_id')
    date_str = data.get('date')
    
    # Validate input
    errors = validate_expense(title, amount, category_id, date_str)
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        # Update expense
        expense.title = title
        expense.description = description
        expense.amount = float(amount)
        expense.category_id = int(category_id)
        
        if date_str:
            expense.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': expense.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update expense'}), 500


@api_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    try:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete expense'}), 500


@api_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    })


@api_bp.route('/categories', methods=['POST'])
@login_required
def create_category():
    """Create a new category"""
    data = request.get_json()
    
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    color = data.get('color', '#007bff').strip()
    
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    
    # Check if category already exists
    existing = Category.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Category already exists'}), 400
    
    try:
        category = Category(
            name=name,
            description=description,
            color=color
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create category'}), 500


@api_bp.route('/export/csv')
@login_required
def export_csv():
    """Export expenses to CSV"""
    expenses = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Date', 'Title', 'Description', 'Amount', 'Category'])
    
    # Write data
    for expense in expenses:
        writer.writerow([
            expense.date.strftime('%Y-%m-%d'),
            expense.title,
            expense.description or '',
            float(expense.amount),
            expense.category.name if expense.category else ''
        ])
    
    output.seek(0)
    
    return jsonify({
        'csv_data': output.getvalue(),
        'filename': f'expenses_{datetime.now().strftime("%Y%m%d")}.csv'
    })


@api_bp.route('/stats/summary')
@login_required
def get_summary_stats():
    """Get summary statistics"""
    from sqlalchemy import func, extract
    
    # Current month stats
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    monthly_total = db.session.query(func.sum(Expense.amount))\
        .filter(
            Expense.user_id == current_user.id,
            extract('year', Expense.date) == current_year,
            extract('month', Expense.date) == current_month
        ).scalar() or 0
    
    # Total expenses
    total_expenses = Expense.query.filter_by(user_id=current_user.id).count()
    
    # Average expense
    avg_expense = db.session.query(func.avg(Expense.amount))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    # Top category this month
    top_category = db.session.query(
        Category.name,
        func.sum(Expense.amount).label('total')
    ).join(Category).filter(
        Expense.user_id == current_user.id,
        extract('year', Expense.date) == current_year,
        extract('month', Expense.date) == current_month
    ).group_by(Category.name)\
     .order_by(func.sum(Expense.amount).desc()).first()
    
    return jsonify({
        'monthly_total': float(monthly_total),
        'total_expenses': total_expenses,
        'average_expense': float(avg_expense),
        'top_category': top_category.name if top_category else 'None',
        'current_month': now.strftime('%B %Y')
    })
