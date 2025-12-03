"""
Main application factory and configuration.
"""
from flask import Flask

from config.settings import config
from app.repositories.base import DatabaseInitializer
from app.views.auth_routes import auth_bp
from app.views.main_routes import main_bp
from app.views.transaction_routes import transaction_bp
from app.views.budget_routes import budget_bp


def create_app():
    """Application factory pattern."""
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configure app
    app.secret_key = config.secret_key
    app.config['DEBUG'] = config.debug
    
    # Initialize database
    db_initializer = DatabaseInitializer()
    db_initializer.initialize_database()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(budget_bp)
    
    return app


def run_app():
    """Run the Flask application."""
    app = create_app()
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )


if __name__ == '__main__':
    run_app()