"""
Configuration settings for the Finance Tracker application.
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    name: str
    path: Optional[str] = None
    
    @property
    def connection_string(self) -> str:
        """Get the database connection string."""
        if self.path:
            return os.path.join(self.path, self.name)
        return self.name


@dataclass
class AppConfig:
    """Application configuration settings."""
    secret_key: str
    debug: bool = False
    host: str = '127.0.0.1'
    port: int = 5000
    database: DatabaseConfig = None
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig(name='finance_tracker.db')


class Config:
    """Main configuration class."""
    
    @staticmethod
    def get_config() -> AppConfig:
        """Get application configuration based on environment."""
        return AppConfig(
            secret_key=os.getenv('SECRET_KEY', 'your_secret_key_change_in_production'),
            debug=os.getenv('DEBUG', 'True').lower() == 'true',
            host=os.getenv('HOST', '127.0.0.1'),
            port=int(os.getenv('PORT', '5000')),
            database=DatabaseConfig(
                name=os.getenv('DATABASE_NAME', 'finance_tracker.db'),
                path=os.getenv('DATABASE_PATH')
            )
        )


# Global configuration instance
config = Config.get_config()