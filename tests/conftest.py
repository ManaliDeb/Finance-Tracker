# flask app + test client 

# tests/conftest.py
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    """
    Simple test client for the Flask app.
    """
    # Put Flask into testing mode
    flask_app.config["TESTING"] = True

    # Create a test client and use it for the test
    with flask_app.test_client() as client:
        yield client
