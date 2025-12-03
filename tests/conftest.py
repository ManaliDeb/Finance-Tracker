# tests/conftest.py
import pytest
from app.main import create_app


@pytest.fixture
def app():
    #Create a Flask app instance for testing using the refactored create_app.
    app = create_app()           
    app.config["TESTING"] = True # put Flask in testing mode
    return app


@pytest.fixture
def client(app):
    #Simple test client for making HTTP requests.
    
    return app.test_client()
