# app.py
# This is the main Flask application. It controls:
# 1. The registration page (create account)
# 2. The login page
# 3. The location selection page
# 4. The map page that shows the shortest route
# 5. The history page that shows past route searches

from flask import Flask, render_template, request, redirect, session, url_for

from graph import CAMPUS_LOCATIONS, CAMPUS_EDGES, build_graph
from dijkstra import find_shortest_path
from users import username_exists, create_user, check_login
from history import add_history, get_history, delete_history

app = Flask(__name__)

# Flask needs a secret key to keep login sessions secure.
# For a real project you would keep this private, but for a learning
# project this is fine.
app.secret_key = "campus-route-finder-secret-key"


@app.route("/")
def home():
    # When someone visits the homepage, send them to the login page.
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if username == "" or password == "":
            error = "Please fill in every field."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif username_exists(username):
            error = "That username is already taken. Try another one."
        else:
            create_user(username, password)
            # Send them to the login page with a success message,
            # so they log in with the account they just created.
            return redirect(url_for("login", registered="1"))

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    success = None

    # If we just arrived here after registering, show a success message.
    if request.args.get("registered") == "1":
        success = "Account created! Please log in below."

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "" or password == "":
            error = "Please enter both a username and a password."
        elif check_login(username, password):
            session["username"] = username
            return redirect(url_for("locations"))
        else:
            error = "Incorrect username or password. Please try again, or create an account."

    return render_template("login.html", error=error, success=success)


@app.route("/locations", methods=["GET", "POST"])
def locations():
    # If the user is not logged in, send them back to the login page.
    if "username" not in session:
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        if start == end:
            error = "Please choose two different locations."
        else:
            return redirect(url_for("map_page", start=start, end=end))

    return render_template(
        "locations.html",
        username=session["username"],
        locations=CAMPUS_LOCATIONS,
        error=error,
    )


@app.route("/map")
def map_page():
    if "username" not in session:
        return redirect(url_for("login"))

    start = request.args.get("start")
    end = request.args.get("end")

    # If someone visits /map directly without picking locations first,
    # send them back to the locations page.
    if not start or not end or start not in CAMPUS_LOCATIONS or end not in CAMPUS_LOCATIONS:
        return redirect(url_for("locations"))

    graph = build_graph()
    path, total_distance = find_shortest_path(graph, start, end)

    start_name = CAMPUS_LOCATIONS[start]["name"]
    end_name = CAMPUS_LOCATIONS[end]["name"]

    # If a path was found, save this search to the user's history.
    if path:
        add_history(session["username"], start_name, end_name, total_distance)

    # Build a list of "point_a-point_b" strings for every step of the path.
    # We add both directions because a connection can be drawn either way.
    path_edges = []
    if path:
        for i in range(len(path) - 1):
            point_a = path[i]
            point_b = path[i + 1]
            path_edges.append(point_a + "-" + point_b)
            path_edges.append(point_b + "-" + point_a)

    return render_template(
        "map.html",
        username=session["username"],
        locations=CAMPUS_LOCATIONS,
        edges=CAMPUS_EDGES,
        path=path or [],
        path_edges=path_edges,
        total_distance=total_distance,
        start_name=start_name,
        end_name=end_name,
    )


@app.route("/history")
def history_page():
    if "username" not in session:
        return redirect(url_for("login"))

    entries = get_history(session["username"])

    return render_template(
        "history.html",
        username=session["username"],
        entries=entries,
    )


@app.route("/history/delete/<entry_id>", methods=["POST"])
def delete_history_entry(entry_id):
    if "username" not in session:
        return redirect(url_for("login"))

    delete_history(session["username"], entry_id)
    return redirect(url_for("history_page"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)