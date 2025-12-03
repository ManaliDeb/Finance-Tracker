"""
Transaction service for handling transaction-related business logic.
"""
from typing import List, Optional, Dict
from datetime import datetime

from app.models import Transaction, TransactionType, FinancialSummary
from app.repositories.transaction_repository import TransactionRepository


class TransactionService:
    """Service for transaction-related operations."""
    
    def __init__(self, transaction_repository: TransactionRepository = None):
        self.transaction_repository = transaction_repository or TransactionRepository()
    
    def create_transaction(self, user_id: int, amount: float, category: str, date: str,
                          description: str, payment_method: str, transaction_type: str) -> tuple[bool, str, Optional[Transaction]]:
        """
        Create a new transaction.
        
        Returns:
            tuple: (success, message, transaction_object)
        """
        try:
            # Validate inputs
            if not category or amount is None:
                return False, "Category and amount are required", None
            
            if amount <= 0:
                return False, "Amount must be greater than zero", None
            
            # Validate date format
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return False, "Date must be in YYYY-MM-DD format", None
            
            # Create transaction object
            transaction = Transaction(
                user_id=user_id,
                amount=amount,
                category=category,
                date=date,
                description=description,
                payment_method=payment_method,
                transaction_type=TransactionType(transaction_type)
            )
            
            # Save to database
            created_transaction = self.transaction_repository.create(transaction)
            return True, "Transaction added successfully", created_transaction
            
        except Exception as e:
            return False, f"Failed to create transaction: {str(e)}", None
    
    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        """Get all transactions for a user."""
        return self.transaction_repository.get_by_user_id(user_id)
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        return self.transaction_repository.get_by_id(transaction_id)
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> tuple[bool, str]:
        """
        Delete a transaction (with ownership validation).
        
        Returns:
            tuple: (success, message)
        """
        # Verify ownership
        transaction = self.transaction_repository.get_by_id(transaction_id)
        if not transaction:
            return False, "Transaction not found"
        
        if transaction.user_id != user_id:
            return False, "Unauthorized to delete this transaction"
        
        try:
            success = self.transaction_repository.delete(transaction_id)
            if success:
                return True, "Transaction deleted successfully"
            else:
                return False, "Failed to delete transaction"
        except Exception as e:
            return False, f"Error deleting transaction: {str(e)}"
    
    def update_transaction(self, transaction: Transaction, user_id: int) -> tuple[bool, str]:
        """
        Update a transaction (with ownership validation).
        
        Returns:
            tuple: (success, message)
        """
        # Verify ownership
        existing_transaction = self.transaction_repository.get_by_id(transaction.id)
        if not existing_transaction or existing_transaction.user_id != user_id:
            return False, "Unauthorized to update this transaction"
        
        try:
            self.transaction_repository.update(transaction)
            return True, "Transaction updated successfully"
        except Exception as e:
            return False, f"Error updating transaction: {str(e)}"
    
    def get_financial_summary(self, user_id: int) -> FinancialSummary:
        """Get comprehensive financial summary for a user."""
        # Get totals by type
        total_income = self.transaction_repository.get_total_by_type(user_id, TransactionType.INCOME)
        total_expense = self.transaction_repository.get_total_by_type(user_id, TransactionType.EXPENSE)
        
        # Get category breakdowns
        income_by_category = self.transaction_repository.get_category_totals(user_id, TransactionType.INCOME)
        expense_by_category = self.transaction_repository.get_category_totals(user_id, TransactionType.EXPENSE)
        
        # Get payment method breakdown (for expenses only)
        expense_transactions = self.transaction_repository.get_by_user_and_type(user_id, TransactionType.EXPENSE)
        expense_by_payment_method = {}
        for transaction in expense_transactions:
            method = transaction.payment_method
            expense_by_payment_method[method] = expense_by_payment_method.get(method, 0) + transaction.amount
        
        return FinancialSummary(
            total_income=total_income,
            total_expense=total_expense,
            income_by_category=income_by_category,
            expense_by_category=expense_by_category,
            expense_by_payment_method=expense_by_payment_method
        )
    
    def get_daily_spending_data(self, user_id: int) -> Dict:
        """Get daily spending data for charts."""
        expense_transactions = self.transaction_repository.get_by_user_and_type(user_id, TransactionType.EXPENSE)
        
        daily_totals = {}
        for transaction in expense_transactions:
            date = transaction.date
            daily_totals[date] = daily_totals.get(date, 0) + transaction.amount
        
        # Sort by date
        sorted_data = sorted(daily_totals.items())
        
        return {
            'labels': [item[0] for item in sorted_data],
            'amounts': [item[1] for item in sorted_data]
        }
    
    def get_monthly_spending_data(self, user_id: int) -> Dict:
        """Get monthly spending data for charts."""
        expense_transactions = self.transaction_repository.get_by_user_and_type(user_id, TransactionType.EXPENSE)
        
        monthly_totals = {}
        for transaction in expense_transactions:
            # Extract year-month from date
            date_parts = transaction.date.split('-')
            if len(date_parts) >= 2:
                year_month = f"{date_parts[0]}-{date_parts[1]}"
                monthly_totals[year_month] = monthly_totals.get(year_month, 0) + transaction.amount
        
        # Sort by date and format labels
        sorted_data = sorted(monthly_totals.items())
        
        # Format month labels
        formatted_labels = []
        for year_month, amount in sorted_data:
            try:
                date_obj = datetime.strptime(year_month, '%Y-%m')
                formatted_labels.append(date_obj.strftime('%b %Y'))
            except ValueError:
                formatted_labels.append(year_month)
        
        return {
            'labels': formatted_labels,
            'amounts': [item[1] for item in sorted_data]
        }