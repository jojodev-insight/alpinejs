"""
Authentication routes for user login, registration, and logout
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.utils.validators import validate_registration, validate_login

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        if request.is_json:
            # Handle JSON API request
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '')
            remember = data.get('remember', False)
        else:
            # Handle form request
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            remember = bool(request.form.get('remember'))
        
        # Validate input
        errors = validate_login(username, password)
        if errors:
            if request.is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            for error in errors:
                flash(error, 'error')
            return render_template('auth/login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': user.to_dict()
                })
            
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            error_msg = 'Invalid username/email or password'
            if request.is_json:
                return jsonify({'success': False, 'errors': [error_msg]}), 401
            flash(error_msg, 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        if request.is_json:
            # Handle JSON API request
            data = request.get_json()
        else:
            # Handle form request
            data = request.form.to_dict()
        
        # Extract and validate data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        # Validate input
        errors = validate_registration(
            username, email, password, confirm_password, first_name, last_name
        )
        
        if errors:
            if request.is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        try:
            # Create new user
            user = User(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Log in the new user
            login_user(user)
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Registration successful',
                    'user': user.to_dict()
                })
            
            flash('Registration successful! Welcome to Expense Tracker!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Registration failed. Please try again.'
            
            if request.is_json:
                return jsonify({'success': False, 'errors': [error_msg]}), 500
            flash(error_msg, 'error')
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout endpoint"""
    logout_user()
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)
