import pytest
from src.models import Feedback, FeedbackStatus
from datetime import datetime, UTC

class TestFeedbackModel:
    """Test Feedback model"""
    
    def test_feedback_creation_with_all_fields(self):
        """Test creating feedback with all fields"""
        feedback = Feedback(
            email="test@example.com",
            message="Test message",
            phone="1234567890",
            status=FeedbackStatus.PENDING.value,
            metadata={"key": "value"},
            created_at=datetime.now(UTC).isoformat()
        )
        assert feedback.email == "test@example.com"
        assert feedback.message == "Test message"
        assert feedback.phone == "1234567890"
        assert feedback.status == FeedbackStatus.PENDING.value
        assert feedback.metadata == {"key": "value"}
    
    def test_feedback_creation_minimal(self):
        """Test creating feedback with minimal fields"""
        feedback = Feedback(
            email="test@example.com",
            message="Test message"
        )
        assert feedback.email == "test@example.com"
        assert feedback.message == "Test message"
        assert feedback.phone is None
        assert feedback.id is None
        assert feedback.status == FeedbackStatus.PENDING.value
    
    def test_feedback_to_dict(self):
        """Test converting feedback to dictionary"""
        feedback = Feedback(
            email="test@example.com",
            message="Test message",
            phone="1234567890",
            id=1,
            status=FeedbackStatus.PENDING.value
        )
        result = feedback.to_dict()
        assert result['email'] == "test@example.com"
        assert result['message'] == "Test message"
        assert result['phone'] == "1234567890"
        assert result['id'] == 1
        assert result['status'] == FeedbackStatus.PENDING.value
    
    def test_feedback_from_dict(self):
        """Test creating feedback from dictionary"""
        data = {
            'email': 'test@example.com',
            'message': 'Test message',
            'phone': '1234567890',
            'id': 1,
            'status': FeedbackStatus.PENDING.value
        }
        feedback = Feedback.from_dict(data)
        assert feedback.email == data['email']
        assert feedback.message == data['message']
        assert feedback.phone == data['phone']
        assert feedback.id == data['id']
    
    def test_feedback_status_enum(self):
        """Test FeedbackStatus enum values"""
        assert FeedbackStatus.PENDING.value == "Pending"
        assert FeedbackStatus.NEW.value == "New"
        assert FeedbackStatus.IN_PROGRESS.value == "In Progress"
        assert FeedbackStatus.COMPLETED.value == "Completed"
        assert FeedbackStatus.IGNORED.value == "Ignored"