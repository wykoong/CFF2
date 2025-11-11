import pytest
import os
import sqlite3
from pathlib import Path
import logging
from src.dao import get_db, close_db, apply_migrations # Import apply_migrations

# Configure logging for tests
# This ensures logs from conftest.py are visible
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__) # Logger for conftest.py

@pytest.fixture(scope="session")
def test_db_path_session():
    """Return path to test database for session scope"""
    db_path = os.path.join(os.path.dirname(__file__), 'test_database.db')
    logger.debug(f"test_db_path_session: Determined path: {db_path}")
    return db_path

@pytest.fixture
def app(test_db_path_session):
    """Create Flask app for testing"""
    from src.app import create_app
    
    # Clean up old test db before creating the app
    if os.path.exists(test_db_path_session):
        os.remove(test_db_path_session)
        logger.debug(f"app fixture: Removed existing database file: {test_db_path_session}")
    
    app = create_app({
        'TESTING': True,
        'DATABASE': test_db_path_session # Use the physical database file path
    })
    logger.debug(f"app fixture: Created app with DATABASE config: {app.config['DATABASE']}")
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def db(app):
    """Initialize test database with schema and verify table creation"""
    
    test_db = app.config['DATABASE']
    logger.debug(f"db fixture: Using database path from app config: {test_db}")
    
    # Ensure the database file is removed before starting (redundant with app fixture, but safe)
    if os.path.exists(test_db):
        os.remove(test_db)
        logger.debug(f"db fixture: Removed existing database file: {test_db}")
    
    # Use the apply_migrations function from src.dao
    # This function will get its own connection, apply migrations, and close it.
    migrations_dir = Path(__file__).resolve().parents[1] / '.specify' / 'db' / 'migrations'
    logger.debug(f"db fixture: Calling apply_migrations for {test_db} from {migrations_dir}")
    
    try:
        apply_migrations(migrations_dir=migrations_dir, db_path=test_db)
        logger.debug(f"db fixture: apply_migrations completed for {test_db}")
    except Exception as e:
        logger.error(f"db fixture: Failed to apply migrations to {test_db}: {e}", exc_info=True)
        raise # Re-raise to fail the test if migrations fail

    # Get a fresh connection to the now-migrated database for the test
    conn = get_db(test_db)
    logger.debug(f"db fixture: Got fresh connection for test: {test_db}")
    
    # Verify that the feedback table was actually created
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
    if cursor.fetchone() is None:
        logger.error(f"db fixture: Feedback table NOT created in {test_db} after migrations!")
        raise RuntimeError(f"Feedback table not created in {test_db} after migrations!")
    else:
        logger.debug(f"db fixture: Feedback table successfully created in {test_db}")
    
    # Verify the database file exists on disk
    if not os.path.exists(test_db):
        logger.error(f"db fixture: Database file {test_db} does not exist after creation!")
        raise RuntimeError(f"Database file {test_db} does not exist after creation!")
    else:
        logger.debug(f"db fixture: Database file {test_db} exists on disk.")

    yield conn # Yield the connection to the test function
    
    close_db(conn)
    logger.debug(f"db fixture: Closed connection and finished for {test_db}")

@pytest.fixture
def runner(app):
    """Create CLI test runner"""
    return app.test_cli_runner()