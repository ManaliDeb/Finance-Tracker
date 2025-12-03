"""
User repository implementation.
"""
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    """Repository for user operations."""
    
    def create(self, user: User) -> User:
        """Create a new user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (username, email, phone, password) 
                   VALUES (?, ?, ?, ?)""",
                (user.username, user.email, user.phone, user.password_hash)
            )
            conn.commit()
            user.id = cursor.lastrowid
            return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row['phone'],
                    password_hash=row['password']
                )
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row['phone'],
                    password_hash=row['password']
                )
            return None
    
    def get_all(self) -> List[User]:
        """Get all users."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            
            return [
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row['phone'],
                    password_hash=row['password']
                )
                for row in rows
            ]
    
    def update(self, user: User) -> User:
        """Update user information."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE users SET username = ?, email = ?, phone = ? 
                   WHERE id = ?""",
                (user.username, user.email, user.phone, user.id)
            )
            conn.commit()
            return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username and password."""
        user = self.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    def create_user_with_hashed_password(self, username: str, email: str, phone: str, password: str) -> User:
        """Create a new user with hashed password."""
        user = User(
            username=username,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        return self.create(user)