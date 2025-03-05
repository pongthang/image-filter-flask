import sqlite3

# Define database file

DATABASE = "images.db"


def get_db_connection():
    """Returns a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    return conn
