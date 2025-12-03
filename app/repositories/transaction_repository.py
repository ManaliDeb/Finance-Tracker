"""
Transaction repository implementation.
"""
from typing import Optional, List
from datetime import datetime

from app.models import Transaction, TransactionType
from app.repositories.base import Repository


class TransactionRepository(Repository[Transaction]):
    """Repository for transaction operations."""
    
    def create(self, transaction: Transaction) -> Transaction:
        """Create a new transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO transactions 
                   (user_id, amount, category, date, description, payment_method, transaction_type) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (transaction.user_id, transaction.amount, transaction.category,
                 transaction.date, transaction.description, transaction.payment_method,
                 transaction.transaction_type.value)
            )
            conn.commit()
            transaction.id = cursor.lastrowid
            return transaction
    
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_transaction(row)
            return None
    
    def get_all(self) -> List[Transaction]:
        """Get all transactions."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    def get_by_user_id(self, user_id: int) -> List[Transaction]:
        """Get all transactions for a specific user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    def get_by_user_and_type(self, user_id: int, transaction_type: TransactionType) -> List[Transaction]:
        """Get transactions by user and type."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM transactions WHERE user_id = ? AND transaction_type = ? ORDER BY date DESC",
                (user_id, transaction_type.value)
            )
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    def get_by_category(self, user_id: int, category: str) -> List[Transaction]:
        """Get transactions by category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM transactions WHERE user_id = ? AND category = ? ORDER BY date DESC",
                (user_id, category)
            )
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    def get_by_date_range(self, user_id: int, start_date: str, end_date: str = None) -> List[Transaction]:
        """Get transactions within date range."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if end_date:
                cursor.execute(
                    "SELECT * FROM transactions WHERE user_id = ? AND date >= ? AND date <= ? ORDER BY date DESC",
                    (user_id, start_date, end_date)
                )
            else:
                cursor.execute(
                    "SELECT * FROM transactions WHERE user_id = ? AND date >= ? ORDER BY date DESC",
                    (user_id, start_date)
                )
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    def update(self, transaction: Transaction) -> Transaction:
        """Update transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE transactions SET amount = ?, category = ?, date = ?, 
                   description = ?, payment_method = ?, transaction_type = ? 
                   WHERE id = ?""",
                (transaction.amount, transaction.category, transaction.date,
                 transaction.description, transaction.payment_method,
                 transaction.transaction_type.value, transaction.id)
            )
            conn.commit()
            return transaction
    
    def delete(self, transaction_id: int) -> bool:
        """Delete transaction by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_total_by_type(self, user_id: int, transaction_type: TransactionType) -> float:
        """Get total amount by transaction type."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = ?",
                (user_id, transaction_type.value)
            )
            result = cursor.fetchone()
            return result[0] if result[0] else 0.0
    
    def get_category_totals(self, user_id: int, transaction_type: TransactionType) -> dict:
        """Get total amounts grouped by category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = ? GROUP BY category",
                (user_id, transaction_type.value)
            )
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows}
    
    def _row_to_transaction(self, row) -> Transaction:
        """Convert database row to Transaction object."""
        # Handle cases where transaction_type might be None for old records
        try:
            transaction_type = row['transaction_type'] if row['transaction_type'] else 'expense'
        except (KeyError, IndexError):
            transaction_type = 'expense'
        
        return Transaction(
            id=row['id'],
            user_id=row['user_id'],
            amount=row['amount'],
            category=row['category'],
            date=row['date'],
            description=row['description'],
            payment_method=row['payment_method'],
            transaction_type=TransactionType(transaction_type)
        )