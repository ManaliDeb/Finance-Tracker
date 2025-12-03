"""
Authentication routes for user registration and login.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)
user_service = UserService()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        success, message, user = user_service.authenticate_user(username, password)
        
        if success:
            # Reset session to avoid fixation, then store identity
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main.index'))
        else:
            flash(message, 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        success, message, user = user_service.register_user(username, email, phone, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('auth.login'))