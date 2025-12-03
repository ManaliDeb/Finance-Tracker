import os
import pytest
from app import create_app
from db import init_db

@pytest.fixture
def app(tmp_path):
    # Each test run gets its own temporary SQLite database
    db_path = tmp_path / "test_finance_tracker.db"

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(db_path),
            "SECRET_KEY": "test-secret-key",
        }
    )

    # Initialize the schema
    with app.app_context():
        init_db()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()
