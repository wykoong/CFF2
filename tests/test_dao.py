import pytest
import os
from src.dao import get_db, close_db

class TestDAO:
    """Test database access functions"""
    
    def test_get_db_with_path(self, db):
        """Test get_db returns connection"""
        assert db is not None
        assert db.execute("SELECT 1") is not None
    
    def test_get_db_creates_connection(self, app):
        """Test get_db creates valid SQLite connection"""
        conn = get_db(app.config['DATABASE'])
        assert conn is not None
        cursor = conn.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        assert version is not None
        close_db(conn)
    
    def test_close_db(self, app):
        """Test close_db closes connection"""
        conn = get_db(app.config['DATABASE'])
        close_db(conn)
        # Should not raise exception
        assert True
    
    def test_feedback_table_exists(self, db):
        """Test feedback table exists after migration"""
        cursor = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'"
        )
        assert cursor.fetchone() is not None
    
    def test_feedback_table_schema(self, db):
        """Test feedback table has required columns"""
        cursor = db.execute("PRAGMA table_info(feedback)")
        columns = {row[1] for row in cursor.fetchall()}
        required = {'id', 'email', 'phone', 'message', 'status', 'metadata', 'created_at'}
        assert required.issubset(columns)