import sqlite3
import os
import logging

def count_records_in_table(db_path, table_name):
    """Count the number of records in a specified table."""

    logging.debug(f"-----------count_records_in_table")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        logging.debug(f"count_records_in_table: count_records_in_table feedback: {count}")
        
        return count
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()