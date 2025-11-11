import sqlite3
import os
import logging
from flask import current_app, has_app_context
from pathlib import Path # <--- ADD THIS LINE

ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger(__name__)

def get_db(path=None):
    """
    Establishes and returns a database connection.
    Prioritizes explicit path, then Flask app config, then environment variable, then default.
    """
    db_path = None

    # 1. Explicit path provided to the function
    if path:
        db_path = path
        logger.debug(f"get_db: Using explicit path: {db_path}")
    # 2. Flask app context available and DATABASE config set
    elif has_app_context():
        db_path = current_app.config.get("DATABASE")
        logger.debug(f"get_db: Using DATABASE from Flask app config: {db_path}")
    # 3. Environment variable set
    elif os.environ.get("DATABASE"):
        db_path = os.environ.get("DATABASE")
        logger.debug(f"get_db: Using DATABASE from environment variable: {db_path}")
    # 4. Default path
    else:
        db_path = str(ROOT / "feedback.db")
        logger.debug(f"get_db: Using default database path: {db_path}")

    if not db_path:
        logger.error("get_db: Database path could not be determined.")
        raise ValueError("Database path could not be determined.")

    logger.debug(f"get_db: Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def close_db(conn):
    """Closes the database connection if it exists."""
    if conn:
        conn.close()
        logger.debug("close_db: Database connection closed.")

def applied_migrations(conn):
    """
    Returns a set of migration filenames that have already been applied to the database.
    Creates the 'migrations' table if it doesn't exist.
    """
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        cursor = conn.execute("SELECT filename FROM migrations")
        applied = {row['filename'] for row in cursor.fetchall()}
        logger.debug(f"applied_migrations: Found {len(applied)} applied migrations.")
        return applied
    except sqlite3.Error as e:
        logger.error(f"applied_migrations: Error accessing migrations table: {e}")
        raise

def apply_migrations(migrations_dir=None, db_path=None):
    """
    Applies SQL migration scripts from a directory to the database.
    Only applies scripts that haven't been applied before.
    """
    if migrations_dir is None:
        migrations_dir = ROOT / '.specify' / 'db' / 'migrations'
    
    if not Path(migrations_dir).is_dir():
        logger.error(f"apply_migrations: Migrations directory not found: {migrations_dir}")
        raise FileNotFoundError(f"Migrations directory not found: {migrations_dir}")

    conn = None
    try:
        conn = get_db(db_path)
        logger.debug(f"apply_migrations: Applying migrations to {db_path}")
        
        applied = applied_migrations(conn)
        
        migration_files = sorted(Path(migrations_dir).glob('*.sql'))
        
        for file_path in migration_files:
            filename = file_path.name
            if filename not in applied:
                logger.info(f"apply_migrations: Applying migration: {filename}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                    conn.executescript(sql_script)
                conn.execute("INSERT INTO migrations (filename) VALUES (?)", (filename,))
                conn.commit()
                logger.debug(f"apply_migrations: Successfully applied {filename}")
            else:
                logger.debug(f"apply_migrations: Skipping already applied migration: {filename}")
        logger.info(f"apply_migrations: All migrations processed for {db_path}.")
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"apply_migrations: Database error during migration: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"apply_migrations: Unexpected error during migration: {e}", exc_info=True)
        raise
    finally:
        close_db(conn)

# Example of how to run migrations from a script (e.g., scripts/run_migrations.py)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        apply_migrations()
        logger.info("Database migrations completed successfully.")
    except Exception as e:
        logger.error(f"Failed to apply database migrations: {e}")