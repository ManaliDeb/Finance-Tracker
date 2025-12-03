"""
Budget management routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services.budget_service import BudgetService
from app.views.main_routes import login_required

budget_bp = Blueprint('budgets', __name__)
budget_service = BudgetService()


@budget_bp.route('/budgets')
@login_required
def budgets():
    """Budget management page."""
    user_id = session['user_id']
    username = session['username']
    
    # Get budget analytics
    budget_analytics = budget_service.get_budget_analytics(user_id)
    
    # Convert to dictionary format for template
    budgets_data = []
    for analytic in budget_analytics:
        budget = analytic.budget
        budgets_data.append({
            'id': budget.id,
            'category': budget.category,
            'allocated_amount': budget.allocated_amount,
            'spent_amount': analytic.spent_amount,
            'remaining': analytic.remaining_amount,
            'percentage_used': analytic.percentage_used,
            'period': budget.period.value,
            'start_date': budget.start_date,
            'end_date': budget.end_date,
            'is_overspent': analytic.is_overspent
        })
    
    return render_template('budgets.html',
                         budgets=budgets_data,
                         username=username)


@budget_bp.route('/add_budget', methods=['POST'])
@login_required
def add_budget():
    """Add a new budget."""
    user_id = session['user_id']
    
    # Extract form data
    category = request.form.get('category', '').strip()
    allocated_amount = float(request.form.get('allocated_amount', 0))
    period = request.form.get('period', 'monthly').strip()
    start_date = request.form.get('start_date', '').strip()
    end_date = request.form.get('end_date', '').strip()
    
    # Use service to create budget
    success, message, budget = budget_service.create_budget(
        user_id=user_id,
        category=category,
        allocated_amount=allocated_amount,
        period=period,
        start_date=start_date,
        end_date=end_date or None
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('budgets.budgets'))


@budget_bp.route('/update_budget/<int:budget_id>', methods=['POST'])
@login_required
def update_budget(budget_id):
    """Update budget allocation."""
    user_id = session['user_id']
    allocated_amount = float(request.form.get('allocated_amount', 0))
    
    success, message = budget_service.update_budget_allocation(
        budget_id, allocated_amount, user_id
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('budgets.budgets'))


@budget_bp.route('/delete_budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    """Delete a budget."""
    user_id = session['user_id']
    
    success, message = budget_service.delete_budget(budget_id, user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('budgets.budgets'))