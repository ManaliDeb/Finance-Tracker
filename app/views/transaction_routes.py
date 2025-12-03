"""
Transaction management routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services.transaction_service import TransactionService
from app.views.main_routes import login_required

transaction_bp = Blueprint('transactions', __name__)
transaction_service = TransactionService()


@transaction_bp.route('/transactions')
@login_required
def transactions():
    """Transaction management page."""
    user_id = session['user_id']
    username = session['username']
    
    # Get all transactions for the user
    user_transactions = transaction_service.get_user_transactions(user_id)
    
    # Convert to list of tuples for template compatibility
    transactions_data = []
    for transaction in user_transactions:
        transactions_data.append((
            transaction.id,                    # 0
            transaction.user_id,               # 1
            transaction.amount,                # 2
            transaction.category,              # 3
            transaction.date,                  # 4
            transaction.description,           # 5
            transaction.payment_method,        # 6
            transaction.transaction_type.value # 7
        ))
    
    return render_template('transaction.html',
                         transactions=transactions_data,
                         username=username)


@transaction_bp.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    """Add a new transaction."""
    user_id = session['user_id']
    
    # Extract form data
    category = request.form.get('category', '').strip()
    payment_method = request.form.get('payment_method', '').strip()
    description = request.form.get('notes', '').strip()
    transaction_type = request.form.get('transaction_type', 'expense').strip()
    date = request.form.get('date', '').strip()
    
    try:
        amount = float(request.form['amount'])
    except (KeyError, TypeError, ValueError):
        flash('Amount must be a valid number.', 'error')
        return redirect(url_for('transactions.transactions'))
    
    # Use service to create transaction
    success, message, transaction = transaction_service.create_transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        date=date,
        description=description,
        payment_method=payment_method,
        transaction_type=transaction_type
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('transactions.transactions'))


@transaction_bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Delete a transaction."""
    user_id = session['user_id']
    
    success, message = transaction_service.delete_transaction(transaction_id, user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('transactions.transactions'))