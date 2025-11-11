import pytest
from src.api.feedback import validate_email

class TestValidation:
    """Test validation functions"""
    
    def test_validate_email_valid(self):
        """Test validate_email with valid emails"""
        valid_emails = [
            'test@example.com',
            'user.name@example.co.uk',
            'user+tag@example.com',
            'test123@example-domain.com'
        ]
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test validate_email with invalid emails"""
        invalid_emails = [
            'not-an-email',
            'test@',
            '@example.com',
            'test@example',
            'test @example.com',
            'test@exam ple.com',
            ''
        ]
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_validate_email_edge_cases(self):
        """Test validate_email edge cases"""
        assert validate_email('a@b.co') is True
        assert validate_email('test+test@example.com') is True
        assert validate_email('123@456.com') is True