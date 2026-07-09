# 🎓 Campus Route Finder

A web app that helps you find the shortest walking route between buildings on campus. Built as a beginner-friendly learning project using **Flask (Python)** on the backend and **HTML/CSS/JavaScript** on the frontend — no database required, just simple JSON files.

---

## Features

- 📝 **Account Registration** — create a username and password before logging in
- 🔐 **Real Login System** — credentials are checked against saved accounts, with error messages for wrong logins or duplicate usernames
- 📍 **Location Picker** — choose a starting point and a destination from campus buildings
- 🗺️ **Interactive Campus Map** — an SVG diagram of campus with your shortest route highlighted, complete with a flowing animated route line and glowing route markers
- 📏 **Distance Labels** — every connection on the map shows its distance in meters, with the ones on your route highlighted
- 🏷️ **Distance Badge & Route Chips** — the total route distance and full step-by-step path are shown clearly at the top of the map page
- 🧮 **Dijkstra's Algorithm** — calculates the true shortest-distance path, not just the fewest stops
- 🕑 **Route History** — every route you search is saved automatically, viewable newest-first, with a delete (🗑️) button on each entry
- 🎨 **Branded Header** — a shared navigation bar (project name, History, account badge, Logout) with a custom display font and hover animations, shown on every logged-in page

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, JavaScript |
| Templating | Jinja2 (built into Flask) |
| Data storage | Plain JSON files (`users.json`, `history.json`) — no database required |
| Fonts | Google Fonts — Poppins (body text) and Baloo 2 (header title) |

---

## Project Structure

```
campus-route-finder/
├── app.py                  # Main Flask app — all routes/pages
├── graph.py                # Campus building data + connections
├── dijkstra.py              # Shortest-path algorithm
├── users.py                 # Account creation & login checking
├── history.py                # Route search history: save, load, delete
├── users.json                # Auto-created — stores registered accounts
├── history.json               # Auto-created — stores each user's route history
├── templates/
│   ├── header.html            # Shared top navigation bar (included in other pages)
│   ├── login.html             # Login page
│   ├── register.html          # Account creation page
│   ├── locations.html         # Start/destination picker page
│   ├── map.html                # Campus map with highlighted route
│   └── history.html            # Past route searches, with delete option
└── static/
    ├── style.css                # All page styling
    └── script.js                 # Fade-in animation + form validation
```

---

## How It Works

### Accounts
`users.py` stores registered accounts in `users.json` as simple `username: password` pairs. Registration checks that the username isn't taken and both passwords match; login checks the entered credentials against what's saved.

### Route Finding
- `graph.py` stores every campus building as a node (with x/y coordinates for drawing) and every walkable connection as an edge with a real-world distance in meters.
- `dijkstra.py` implements **Dijkstra's algorithm**: it always explores the closest unvisited building next, keeping track of the shortest known distance to every other building, until it reaches the destination.
- The result — the ordered list of buildings to pass through and the total distance — is sent to `map.html`, which draws the whole campus and highlights only the buildings, connections, and distance labels that are part of that route.

### History
Every time a route is successfully found, `history.py` saves it to `history.json` under the logged-in user's name, with a unique id, a timestamp, and the total distance. The History page lists these newest-first, and each one can be deleted individually.

---

## Setup & Installation

### 1. Prerequisites
- Python 3.8 or later installed ([python.org](https://www.python.org/downloads/))

### 2. Set up a virtual environment
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install dependencies
```bash
pip install flask
```

### 4. Run the app
```bash
python app.py
```

### 5. Open it in your browser
```
http://127.0.0.1:5000
```

---

## Usage

1. **Register** — create a username and password on the sign-up page.
2. **Log In** — use the account you just created.
3. **Choose Locations** — pick a starting building and a destination from the dropdowns.
4. **View Route** — see the shortest path drawn on the campus map, with the total distance, a step-by-step route list, and per-segment distances.
5. **Check History** — click **🕑 History** in the header any time to see past searches, and delete any entry you no longer need.
6. **Log Out** — click **🚪 Logout** in the header when you're done.

---

## Customizing the Campus

To add or change a building, open `graph.py`:

```python
CAMPUS_LOCATIONS = {
    "your_id": {"name": "Building Name", "x": 300, "y": 200},
}

CAMPUS_EDGES = [
    ("your_id", "another_id", 150),  # distance in meters
]
```
The map, dropdowns, and route calculations automatically pick up any changes — no other file needs editing.

---

## Notes & Limitations

- This is a **learning project**, not a production app. Passwords are stored in plain text in `users.json` for simplicity — a real app would use secure password hashing (e.g. with a library like `werkzeug.security` or `bcrypt`).
- `users.json` and `history.json` are created automatically the first time they're needed — you don't need to create them manually.
- Data is stored in local JSON files, so it will reset if those files are deleted, and won't sync across different computers or devices.
- The campus map is a simplified dots-and-lines diagram, not a to-scale real map — coordinates in `graph.py` are just for layout, not GPS positions.

---

## Credits

Built step by step as a guided learning project — combining a real graph algorithm (Dijkstra), a Flask backend with sessions and simple file-based storage, and a hand-styled frontend, all in beginner-readable code.