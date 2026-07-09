# history.py
# This file saves and loads each user's route search history, using
# the SQLite database (see database.py) instead of a JSON file.

import uuid
import sqlite3
from datetime import datetime

from database import get_connection


def add_history(username, start_name, end_name, distance):
    """
    Adds one route search to the history table.
    Each entry gets its own unique id, so it can be deleted later.
    """
    conn = get_connection()
    cursor = conn.cursor()

    entry_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

    cursor.execute(
        """
        INSERT INTO history (id, username, start_name, end_name, distance, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (entry_id, username, start_name, end_name, distance, timestamp),
    )

    conn.commit()
    conn.close()


def get_history(username):
    """
    Returns the list of past routes for one user, newest first.
    Each entry is returned as a dictionary, the same shape the
    HTML templates already expect.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, start_name, end_name, distance, timestamp
        FROM history
        WHERE username = ?
        ORDER BY rowid DESC
        """,
        (username,),
    )
    rows = cursor.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            "id": row["id"],
            "start_name": row["start_name"],
            "end_name": row["end_name"],
            "distance": row["distance"],
            "timestamp": row["timestamp"],
        })

    return entries


def delete_history(username, entry_id):
    """Removes one specific route from the database by its id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM history WHERE id = ? AND username = ?",
        (entry_id, username),
    )
    conn.commit()
    conn.close()