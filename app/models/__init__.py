"""
Data models for the Finance Tracker application.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TransactionType(Enum):
    """Enumeration for transaction types."""
    INCOME = "income"
    EXPENSE = "expense"


class BudgetPeriod(Enum):
    """Enumeration for budget periods."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


@dataclass
class User:
    """User model."""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    phone: str = ""
    password_hash: str = ""
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Category:
    """Category model."""
    id: Optional[int] = None
    user_id: int = 0
    name: str = ""
    color: str = "#007bff"
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Transaction:
    """Transaction model."""
    id: Optional[int] = None
    user_id: int = 0
    amount: float = 0.0
    category: str = ""
    date: str = ""
    description: Optional[str] = None
    payment_method: str = ""
    transaction_type: TransactionType = TransactionType.EXPENSE
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if isinstance(self.transaction_type, str):
            self.transaction_type = TransactionType(self.transaction_type)
    
    @property
    def is_income(self) -> bool:
        """Check if transaction is income."""
        return self.transaction_type == TransactionType.INCOME
    
    @property
    def is_expense(self) -> bool:
        """Check if transaction is expense."""
        return self.transaction_type == TransactionType.EXPENSE


@dataclass
class Budget:
    """Budget model."""
    id: Optional[int] = None
    user_id: int = 0
    category: str = ""
    allocated_amount: float = 0.0
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    start_date: str = ""
    end_date: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if isinstance(self.period, str):
            self.period = BudgetPeriod(self.period)


@dataclass
class BudgetAnalytics:
    """Budget analytics model for tracking spending against budgets."""
    budget: Budget
    spent_amount: float = 0.0
    remaining_amount: float = 0.0
    percentage_used: float = 0.0
    is_overspent: bool = False
    
    def __post_init__(self):
        self.remaining_amount = self.budget.allocated_amount - self.spent_amount
        if self.budget.allocated_amount > 0:
            self.percentage_used = (self.spent_amount / self.budget.allocated_amount) * 100
        self.is_overspent = self.spent_amount > self.budget.allocated_amount


@dataclass
class FinancialSummary:
    """Financial summary model."""
    total_income: float = 0.0
    total_expense: float = 0.0
    net_balance: float = 0.0
    income_by_category: dict = field(default_factory=dict)
    expense_by_category: dict = field(default_factory=dict)
    expense_by_payment_method: dict = field(default_factory=dict)
    
    def __post_init__(self):
        self.net_balance = self.total_income - self.total_expense