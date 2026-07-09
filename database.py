# database.py
# This file sets up our SQLite database: a single, self-contained
# database file (campus.db) that Python can read and write directly,
# with no separate database server required.

import sqlite3

DB_FILE = "campus.db"


def get_connection():
    """
    Opens a connection to the database file. Every function that
    needs to read or write data calls this first.
    """
    return sqlite3.connect(DB_FILE)


def init_db():
    """
    Creates the database tables if they don't already exist yet.
    This is safe to run every time the app starts — it will never
    overwrite or delete existing data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            start_name TEXT NOT NULL,
            end_name TEXT NOT NULL,
            distance INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()