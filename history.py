# history.py
# This file saves and loads each user's route search history.
# History is stored in a simple file called history.json,
# using the same simple approach as users.py.

import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


def load_history():
    """
    Reads everyone's history from history.json and returns it as a
    dictionary, e.g. {"student1": [ {...}, {...} ]}
    If the file doesn't exist yet, returns an empty dictionary.
    """
    if not os.path.exists(HISTORY_FILE):
        return {}

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    """Saves the given history dictionary back to history.json."""
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)


def add_history(username, start_name, end_name, distance):
    """
    Adds one route search to a user's history.
    The newest entry is always placed first in the list.
    """
    history = load_history()

    if username not in history:
        history[username] = []

    entry = {
        "start_name": start_name,
        "end_name": end_name,
        "distance": distance,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }

    history[username].insert(0, entry)
    save_history(history)


def get_history(username):
    """Returns the list of past routes for one user, newest first."""
    history = load_history()
    return history.get(username, [])