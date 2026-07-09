# users.py
# This file handles saving and checking user accounts, using the
# SQLite database (see database.py) instead of a JSON file.

from database import get_connection


def username_exists(username):
    """Returns True if this username has already been registered."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def create_user(username, password):
    """Adds a new user to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()


def check_login(username, password):
    """
    Returns True only if the username exists AND the password
    matches what was saved when they registered.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None