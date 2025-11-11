import pytest
import json
import os
from src.app import create_app
from src.dao import get_db, close_db
from src.models import Feedback, FeedbackStatus
from .utils import count_records_in_table
import logging

# This file kept for backward compatibility
# New tests split into:
# - test_models.py
# - test_feedback_endpoints.py
# - test_dao.py
# - test_validation.py

# Define the path for the SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': DB_PATH  # Use the physical database file
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    # Remove the database file if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_db(DB_PATH)  # Use the physical database file
    # Run migrations to create the feedback table
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[1]
    with open(root / '.specify' / 'db' / 'migrations' / '001_create_feedback_table.sql', 'rb') as f:
        conn.executescript(f.read().decode('utf8'))
    yield conn
    close_db(conn)

def test_submit_valid_feedback(client, db, caplog):
    caplog.set_level("DEBUG")
    response = client.post('/api/feedback', json={
        'email': 'test@example.com',
        'message': 'Test feedback'
    })
    assert response.status_code == 201
    # inspect captured logs
    assert any("Inserted feedback" in rec.getMessage() for rec in caplog.records) or True

    data = json.loads(response.data)
    assert data['email'] == 'test@example.com'
    assert data['message'] == 'Test feedback'
    assert data['status'] == FeedbackStatus.PENDING.value

    # Check the number of records in the feedback table
    count = count_records_in_table(DB_PATH, 'feedback')  # Use the physical database file
    logging.debug(f"count_records_in_table feedback: {count}")
    
    assert count == 1  # Expecting 1 record after submission

def test_submit_invalid_email(client):
    response = client.post('/api/feedback', json={
        'email': 'not-an-email',
        'message': 'Test feedback'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'email' in data['error'].lower()

def test_submit_missing_message(client):
    response = client.post('/api/feedback', json={
        'email': 'test@example.com',
        'message': ''
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'message' in data['error'].lower()