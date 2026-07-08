# users.py
# This file handles saving and checking user accounts.
# Accounts are stored in a simple file called users.json, which acts
# like a tiny database. This is NOT how real websites store passwords
# (real sites use secure hashing) but it's simple and easy to
# understand for a learning project.

import json
import os

USERS_FILE = "users.json"


def load_users():
    """
    Reads all registered users from users.json and returns them as a
    dictionary, e.g. {"student1": "1234", "student2": "abcd"}.
    If the file doesn't exist yet (nobody has registered), returns
    an empty dictionary instead of crashing.
    """
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    """
    Saves the given dictionary of users back to users.json,
    overwriting whatever was there before.
    """
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=2)


def username_exists(username):
    """Returns True if this username has already been registered."""
    users = load_users()
    return username in users


def create_user(username, password):
    """Adds a new user to users.json."""
    users = load_users()
    users[username] = password
    save_users(users)


def check_login(username, password):
    """
    Returns True only if the username exists AND the password
    matches what was saved when they registered.
    """
    users = load_users()
    return username in users and users[username] == password