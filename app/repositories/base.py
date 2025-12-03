"""
Base repository interface and database initialization.
"""
import sqlite3
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from contextlib import contextmanager

from config.settings import config

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Abstract base repository class."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.database.connection_string
    
    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID."""
        pass


class DatabaseInitializer:
    """Handles database schema initialization."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.database.connection_string
    
    def initialize_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    color TEXT DEFAULT '#007bff',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id, name)
                )
            ''')
            
            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    payment_method TEXT NOT NULL,
                    transaction_type TEXT DEFAULT 'expense',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Budgets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    allocated_amount REAL NOT NULL,
                    period TEXT NOT NULL DEFAULT 'monthly',
                    start_date TEXT NOT NULL,
                    end_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id, category)
                )
            ''')
            
            # Run migrations
            self._run_migrations(cursor)
            
            conn.commit()
    
    def _run_migrations(self, cursor):
        """Run database migrations for schema updates."""
        # Check if transaction_type column exists, if not add it
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'transaction_type' not in columns:
            print("Adding transaction_type column to transactions table...")
            cursor.execute('ALTER TABLE transactions ADD COLUMN transaction_type TEXT DEFAULT "expense"')
            print("Migration completed: Added transaction_type column")
        
        # Check if created_at column exists in transactions, if not add it
        if 'created_at' not in columns:
            print("Adding created_at column to transactions table...")
            cursor.execute('ALTER TABLE transactions ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP')
            print("Migration completed: Added created_at column")


# Initialize database on module import
db_initializer = DatabaseInitializer()
db_initializer.initialize_database()