import pytest
import json
from src.models import FeedbackStatus

class TestFeedbackEndpoints:
    """Test feedback API endpoints"""
    
    def test_get_feedback_form_returns_200(self, client):
        """Test GET /api/feedback returns 200 and HTML"""
        response = client.get('/api/feedback')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_get_feedback_form_contains_form_elements(self, client):
        """Test feedback form contains required form elements"""
        response = client.get('/api/feedback')
        assert b'email' in response.data
        assert b'message' in response.data
        assert b'form' in response.data.lower()
    
    def test_post_valid_feedback(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback with valid data"""
        response = client.post('/api/feedback', json={
            'email': 'test@example.com',
            'message': 'This is a test feedback'
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['email'] == 'test@example.com'
        assert data['message'] == 'This is a test feedback'
        assert data['status'] == FeedbackStatus.PENDING.value
        assert data['id'] is not None
    
    def test_post_feedback_with_phone(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback with phone number"""
        response = client.post('/api/feedback', json={
            'email': 'test@example.com',
            'message': 'Test feedback',
            'phone': '1234567890'
        })
        assert response.status_code == 201
        data = json.loads(response.data) # Added to check response data
        assert data['phone'] == '1234567890' # Added to check response data
    
    def test_post_feedback_missing_email(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback without email"""
        response = client.post('/api/feedback', json={
            'message': 'Test feedback'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email' in data['error'].lower()
    
    def test_post_feedback_invalid_email(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback with invalid email"""
        response = client.post('/api/feedback', json={
            'email': 'not-an-email',
            'message': 'Test feedback'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email' in data['error'].lower()
    
    def test_post_feedback_missing_message(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback without message"""
        response = client.post('/api/feedback', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'message' in data['error'].lower()
    
    def test_post_feedback_empty_message(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback with empty message"""
        response = client.post('/api/feedback', json={
            'email': 'test@example.com',
            'message': ''
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'message' in data['error'].lower()
    
    def test_post_feedback_message_too_long(self, client, db): # <--- ADDED 'db' HERE
        """Test POST /api/feedback with message > 5000 chars"""
        response = client.post('/api/feedback', json={
            'email': 'test@example.com',
            'message': 'x' * 5001
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'too long' in data['error'].lower()
    
    def test_post_feedback_no_data(self, client, db):
        """Test POST /api/feedback with no JSON data"""
        # Send an empty JSON object with the correct Content-Type
        response = client.post('/api/feedback', json={}) 
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'no data provided' in data['error'].lower()
    
    def test_post_feedback_multiple_records(self, client, db):
        """Test creating multiple feedback records"""
        for i in range(3):
            response = client.post('/api/feedback', json={
                'email': f'test{i}@example.com',
                'message': f'Test feedback {i}'
            })
            assert response.status_code == 201
        
        # Verify all records in database
        cur = db.execute("SELECT COUNT(*) FROM feedback")
        count = cur.fetchone()[0]
        assert count == 3
    
    def test_health_endpoint(self, client):
        """Test /health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert 'database' in data
    
    def test_index_redirect(self, client):
        """Test / redirects to /api/feedback"""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/api/feedback' in response.location