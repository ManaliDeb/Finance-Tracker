"""
Budget service for handling budget-related business logic.
"""
from typing import List, Optional, Dict
from datetime import datetime

from app.models import Budget, BudgetAnalytics, BudgetPeriod, TransactionType
from app.repositories.budget_repository import BudgetRepository
from app.repositories.transaction_repository import TransactionRepository


class BudgetService:
    """Service for budget-related operations."""
    
    def __init__(self, budget_repository: BudgetRepository = None, transaction_repository: TransactionRepository = None):
        self.budget_repository = budget_repository or BudgetRepository()
        self.transaction_repository = transaction_repository or TransactionRepository()
    
    def create_budget(self, user_id: int, category: str, allocated_amount: float,
                     period: str, start_date: str, end_date: str = None) -> tuple[bool, str, Optional[Budget]]:
        """
        Create a new budget.
        
        Returns:
            tuple: (success, message, budget_object)
        """
        try:
            # Validate inputs
            if not category or allocated_amount <= 0:
                return False, "Category and valid allocated amount are required", None
            
            # Check if budget already exists for this category
            existing_budget = self.budget_repository.get_by_category(user_id, category)
            if existing_budget:
                return False, "Budget already exists for this category. Use update instead.", None
            
            # Validate date format
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                if end_date:
                    datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return False, "Dates must be in YYYY-MM-DD format", None
            
            # Create budget object
            budget = Budget(
                user_id=user_id,
                category=category,
                allocated_amount=allocated_amount,
                period=BudgetPeriod(period),
                start_date=start_date,
                end_date=end_date
            )
            
            # Save to database
            created_budget = self.budget_repository.create(budget)
            return True, "Budget created successfully!", created_budget
            
        except Exception as e:
            return False, f"Failed to create budget: {str(e)}", None
    
    def get_user_budgets(self, user_id: int) -> List[Budget]:
        """Get all budgets for a user."""
        return self.budget_repository.get_by_user_id(user_id)
    
    def get_budget_analytics(self, user_id: int) -> List[BudgetAnalytics]:
        """Get budget analytics with spending tracking."""
        budgets = self.budget_repository.get_by_user_id(user_id)
        analytics = []
        
        for budget in budgets:
            spent_amount = self._calculate_spent_amount(user_id, budget)
            analytics.append(BudgetAnalytics(
                budget=budget,
                spent_amount=spent_amount
            ))
        
        return analytics
    
    def get_budget_warnings(self, user_id: int) -> List[Dict]:
        """Get budget warnings for overspent or near-limit categories."""
        analytics = self.get_budget_analytics(user_id)
        warnings = []
        
        for analytic in analytics:
            budget = analytic.budget
            
            if analytic.is_overspent:
                warnings.append({
                    'type': 'overspent',
                    'category': budget.category,
                    'allocated': budget.allocated_amount,
                    'spent': analytic.spent_amount,
                    'overage': analytic.spent_amount - budget.allocated_amount
                })
            elif analytic.percentage_used > 80:  # 80% threshold warning
                warnings.append({
                    'type': 'approaching_limit',
                    'category': budget.category,
                    'allocated': budget.allocated_amount,
                    'spent': analytic.spent_amount,
                    'percentage': analytic.percentage_used
                })
        
        return warnings
    
    def update_budget_allocation(self, budget_id: int, allocated_amount: float, user_id: int) -> tuple[bool, str]:
        """
        Update budget allocation amount.
        
        Returns:
            tuple: (success, message)
        """
        try:
            # Verify ownership
            budget = self.budget_repository.get_by_id(budget_id)
            if not budget or budget.user_id != user_id:
                return False, "Budget not found or unauthorized"
            
            if allocated_amount <= 0:
                return False, "Valid allocated amount is required"
            
            success = self.budget_repository.update_allocation(budget_id, allocated_amount)
            if success:
                return True, "Budget updated successfully!"
            else:
                return False, "Failed to update budget"
                
        except Exception as e:
            return False, f"Error updating budget: {str(e)}"
    
    def delete_budget(self, budget_id: int, user_id: int) -> tuple[bool, str]:
        """
        Delete a budget (with ownership validation).
        
        Returns:
            tuple: (success, message)
        """
        try:
            # Verify ownership
            budget = self.budget_repository.get_by_id(budget_id)
            if not budget or budget.user_id != user_id:
                return False, "Budget not found or unauthorized"
            
            success = self.budget_repository.delete(budget_id)
            if success:
                return True, "Budget deleted successfully!"
            else:
                return False, "Failed to delete budget"
                
        except Exception as e:
            return False, f"Error deleting budget: {str(e)}"
    
    def get_overspent_categories(self, user_id: int) -> List[Dict]:
        """Get list of overspent categories."""
        analytics = self.get_budget_analytics(user_id)
        overspent = []
        
        for analytic in analytics:
            if analytic.is_overspent:
                overspent.append({
                    'category': analytic.budget.category,
                    'allocated': analytic.budget.allocated_amount,
                    'spent': analytic.spent_amount,
                    'overage': analytic.spent_amount - analytic.budget.allocated_amount
                })
        
        return overspent
    
    def get_spending_breakdown_by_category(self, user_id: int) -> Dict[str, Dict]:
        """Get spending breakdown by category with budget comparison."""
        budgets = {b.category: b for b in self.budget_repository.get_by_user_id(user_id)}
        expense_totals = self.transaction_repository.get_category_totals(user_id, TransactionType.EXPENSE)
        
        breakdown = {}
        
        # Include budgeted categories
        for category, budget in budgets.items():
            spent = expense_totals.get(category, 0)
            breakdown[category] = {
                'budgeted': budget.allocated_amount,
                'spent': spent,
                'remaining': budget.allocated_amount - spent,
                'percentage': (spent / budget.allocated_amount * 100) if budget.allocated_amount > 0 else 0
            }
        
        # Include non-budgeted spending categories
        for category, spent in expense_totals.items():
            if category not in breakdown:
                breakdown[category] = {
                    'budgeted': 0,
                    'spent': spent,
                    'remaining': -spent,  # Negative because no budget
                    'percentage': 100  # Over 100% since no budget
                }
        
        return breakdown
    
    def _calculate_spent_amount(self, user_id: int, budget: Budget) -> float:
        """Calculate amount spent for a specific budget."""
        # Get transactions within the budget period
        transactions = self.transaction_repository.get_by_date_range(
            user_id, budget.start_date, budget.end_date
        )
        
        # Filter by category and expense type
        spent = 0
        for transaction in transactions:
            if (transaction.category == budget.category and 
                transaction.transaction_type == TransactionType.EXPENSE):
                spent += transaction.amount
        
        return spent