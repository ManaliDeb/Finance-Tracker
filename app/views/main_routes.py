"""
Main application routes for dashboard and core functionality.
"""
from flask import Blueprint, render_template, session, redirect, url_for, jsonify

from app.services.user_service import UserService
from app.services.transaction_service import TransactionService
from app.services.budget_service import BudgetService

main_bp = Blueprint('main', __name__)
user_service = UserService()
transaction_service = TransactionService()
budget_service = BudgetService()


def login_required(func):
    """Decorator to require login for protected routes."""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@main_bp.route('/')
@login_required
def index():
    """Dashboard home page."""
    user_id = session['user_id']
    username = session['username']
    
    # Get financial summary
    financial_summary = transaction_service.get_financial_summary(user_id)
    
    # Get budget warnings
    budget_warnings = budget_service.get_budget_warnings(user_id)
    
    return render_template('index.html',
                         username=username,
                         total_income=financial_summary.total_income,
                         total_expense=financial_summary.total_expense,
                         net_balance=financial_summary.net_balance,
                         total_upi=financial_summary.expense_by_payment_method.get('UPI', 0),
                         total_cash=financial_summary.expense_by_payment_method.get('Cash', 0),
                         budget_warnings=budget_warnings)


@main_bp.route('/statistics')
@login_required
def statistics():
    """Statistics and analytics page."""
    user_id = session['user_id']
    
    # Get financial summary
    financial_summary = transaction_service.get_financial_summary(user_id)
    
    # Get top spending categories (limit to 5)
    expense_categories = financial_summary.expense_by_category
    top_spending_categories = dict(
        sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:5]
    )
    
    return render_template('statistics.html',
                         total_expenses=financial_summary.total_expense,
                         total_income=financial_summary.total_income,
                         net_balance=financial_summary.net_balance,
                         expense_by_category=financial_summary.expense_by_category,
                         income_by_category=financial_summary.income_by_category,
                         top_spending_categories=top_spending_categories)


@main_bp.route('/daily_spending_data')
@login_required
def daily_spending_data():
    """API endpoint for daily spending chart data."""
    user_id = session['user_id']
    data = transaction_service.get_daily_spending_data(user_id)
    return jsonify(data)


@main_bp.route('/monthly_spending_data')
@login_required
def monthly_spending_data():
    """API endpoint for monthly spending chart data."""
    user_id = session['user_id']
    data = transaction_service.get_monthly_spending_data(user_id)
    return jsonify(data)


@main_bp.route('/budget_warnings')
@login_required
def budget_warnings_api():
    """API endpoint for budget warnings."""
    user_id = session['user_id']
    warnings = budget_service.get_budget_warnings(user_id)
    return jsonify({'warnings': warnings})