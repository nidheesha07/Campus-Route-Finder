# history.py
# This file saves and loads each user's route search history.
# History is stored in a simple file called history.json,
# using the same simple approach as users.py.

import json
import os
import uuid
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
    Each entry gets its own unique "id" so it can be deleted later.
    """
    history = load_history()

    if username not in history:
        history[username] = []

    entry = {
        "id": uuid.uuid4().hex,
        "start_name": start_name,
        "end_name": end_name,
        "distance": distance,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }

    history[username].insert(0, entry)
    save_history(history)


def get_history(username):
    """
    Returns the list of past routes for one user, newest first.

    Older entries that were saved before the delete feature existed
    won't have an "id" yet. This function checks for that and gives
    them one automatically, so every entry can always be deleted.
    """
    history = load_history()
    entries = history.get(username, [])

    needs_saving = False
    for entry in entries:
        if "id" not in entry:
            entry["id"] = uuid.uuid4().hex
            needs_saving = True

    if needs_saving:
        history[username] = entries
        save_history(history)

    return entries


def delete_history(username, entry_id):
    """
    Removes one specific route from a user's history by its id.
    If the id isn't found, nothing happens.
    """
    history = load_history()

    if username not in history:
        return

    history[username] = [
        entry for entry in history[username] if entry["id"] != entry_id
    ]
    save_history(history)