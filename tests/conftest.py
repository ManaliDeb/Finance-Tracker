# tests/conftest.py
import pytest
from app.app import app as flask_app  # <-- uses app/app.py's "app" object


@pytest.fixture
def client():
    """
    Simple Flask test client for making requests to the app.
    """
    # Put Flask into testing mode
    flask_app.config["TESTING"] = True

    # Create a test client and yield it to the tests
    with flask_app.test_client() as client:
        yield client
