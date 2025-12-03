"""
User service for handling user-related business logic.
"""
from typing import Optional

from app.models import User
from app.repositories.user_repository import UserRepository


class UserService:
    """Service for user-related operations."""
    
    def __init__(self, user_repository: UserRepository = None):
        self.user_repository = user_repository or UserRepository()
    
    def register_user(self, username: str, email: str, phone: str, password: str) -> tuple[bool, str, Optional[User]]:
        """
        Register a new user.
        
        Returns:
            tuple: (success, message, user_object)
        """
        # Check if user already exists
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            return False, "Username already exists. Please choose a different one.", None
        
        try:
            # Create new user with hashed password
            user = self.user_repository.create_user_with_hashed_password(
                username=username,
                email=email,
                phone=phone,
                password=password
            )
            return True, "Registration successful! Please log in.", user
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None
    
    def authenticate_user(self, username: str, password: str) -> tuple[bool, str, Optional[User]]:
        """
        Authenticate user credentials.
        
        Returns:
            tuple: (success, message, user_object)
        """
        user = self.user_repository.authenticate(username, password)
        if user:
            return True, "Authentication successful", user
        else:
            return False, "Invalid username or password. Please try again.", None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.user_repository.get_by_id(user_id)
    
    def update_user_profile(self, user: User) -> tuple[bool, str]:
        """
        Update user profile.
        
        Returns:
            tuple: (success, message)
        """
        try:
            self.user_repository.update(user)
            return True, "Profile updated successfully"
        except Exception as e:
            return False, f"Failed to update profile: {str(e)}"