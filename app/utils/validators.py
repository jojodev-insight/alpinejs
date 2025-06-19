"""
Validation utilities for forms and API requests
"""
import re
from app.models.user import User


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'\d', password):
        return False
    
    return True


def validate_username(username):
    """
    Validate username format
    - 3-20 characters
    - Only alphanumeric and underscore
    - Must start with letter
    """
    if len(username) < 3 or len(username) > 20:
        return False
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False
    
    return True


def validate_login(username, password):
    """Validate login form data"""
    errors = []
    
    if not username:
        errors.append('Username or email is required')
    
    if not password:
        errors.append('Password is required')
    
    return errors


def validate_registration(username, email, password, confirm_password, first_name, last_name):
    """Validate registration form data"""
    errors = []
    
    # Required fields
    if not username:
        errors.append('Username is required')
    elif not validate_username(username):
        errors.append('Username must be 3-20 characters, start with a letter, and contain only letters, numbers, and underscores')
    elif User.query.filter_by(username=username).first():
        errors.append('Username already exists')
    
    if not email:
        errors.append('Email is required')
    elif not validate_email(email):
        errors.append('Please enter a valid email address')
    elif User.query.filter_by(email=email).first():
        errors.append('Email already registered')
    
    if not password:
        errors.append('Password is required')
    elif not validate_password(password):
        errors.append('Password must be at least 8 characters with uppercase, lowercase, and number')
    
    if password != confirm_password:
        errors.append('Passwords do not match')
    
    if not first_name:
        errors.append('First name is required')
    elif len(first_name) > 50:
        errors.append('First name must be less than 50 characters')
    
    if not last_name:
        errors.append('Last name is required')
    elif len(last_name) > 50:
        errors.append('Last name must be less than 50 characters')
    
    return errors


def validate_expense(title, amount, category_id, date_str=None):
    """Validate expense form data"""
    from datetime import datetime
    errors = []
    
    if not title:
        errors.append('Title is required')
    elif len(title) > 100:
        errors.append('Title must be less than 100 characters')
    
    if not amount:
        errors.append('Amount is required')
    else:
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                errors.append('Amount must be greater than 0')
            elif amount_float > 999999.99:
                errors.append('Amount must be less than $1,000,000')
        except (ValueError, TypeError):
            errors.append('Amount must be a valid number')
    
    if not category_id:
        errors.append('Category is required')
    else:
        try:
            int(category_id)
        except (ValueError, TypeError):
            errors.append('Invalid category selected')
    
    if date_str:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            errors.append('Invalid date format')
    
    return errors
