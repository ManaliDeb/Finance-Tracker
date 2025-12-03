"""
Budget repository implementation.
"""
from typing import Optional, List

from app.models import Budget, BudgetPeriod
from app.repositories.base import Repository


class BudgetRepository(Repository[Budget]):
    """Repository for budget operations."""
    
    def create(self, budget: Budget) -> Budget:
        """Create a new budget."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO budgets 
                   (user_id, category, allocated_amount, period, start_date, end_date) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (budget.user_id, budget.category, budget.allocated_amount,
                 budget.period.value, budget.start_date, budget.end_date)
            )
            conn.commit()
            budget.id = cursor.lastrowid
            return budget
    
    def get_by_id(self, budget_id: int) -> Optional[Budget]:
        """Get budget by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM budgets WHERE id = ?", (budget_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_budget(row)
            return None
    
    def get_all(self) -> List[Budget]:
        """Get all budgets."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM budgets ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [self._row_to_budget(row) for row in rows]
    
    def get_by_user_id(self, user_id: int) -> List[Budget]:
        """Get all budgets for a specific user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM budgets WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_budget(row) for row in rows]
    
    def get_by_category(self, user_id: int, category: str) -> Optional[Budget]:
        """Get budget by user and category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM budgets WHERE user_id = ? AND category = ?",
                (user_id, category)
            )
            row = cursor.fetchone()
            
            if row:
                return self._row_to_budget(row)
            return None
    
    def update(self, budget: Budget) -> Budget:
        """Update budget."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE budgets SET allocated_amount = ?, period = ?, 
                   start_date = ?, end_date = ? WHERE id = ?""",
                (budget.allocated_amount, budget.period.value,
                 budget.start_date, budget.end_date, budget.id)
            )
            conn.commit()
            return budget
    
    def update_allocation(self, budget_id: int, allocated_amount: float) -> bool:
        """Update budget allocation amount."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE budgets SET allocated_amount = ? WHERE id = ?",
                (allocated_amount, budget_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def delete(self, budget_id: int) -> bool:
        """Delete budget by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_by_user_and_category(self, user_id: int, category: str) -> bool:
        """Delete budget by user and category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM budgets WHERE user_id = ? AND category = ?",
                (user_id, category)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def _row_to_budget(self, row) -> Budget:
        """Convert database row to Budget object."""
        return Budget(
            id=row['id'],
            user_id=row['user_id'],
            category=row['category'],
            allocated_amount=row['allocated_amount'],
            period=BudgetPeriod(row['period']),
            start_date=row['start_date'],
            end_date=row['end_date']
        )