# tests/conftest.py
import pytest
from app.main import create_app


@pytest.fixture
def app():
    """
    Create a fresh Flask app for each test run.
    """
    app = create_app(
        {
            "TESTING": True,  # tells Flask we're in test mode
        }
    )
    return app


@pytest.fixture
def client(app):
    """
    Simple test client for making HTTP requests.
    """
    return app.test_client()
