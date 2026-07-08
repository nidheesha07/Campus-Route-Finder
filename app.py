# app.py
# This is the main Flask application. It controls:
# 1. The login page
# 2. The location selection page
# 3. The map page that shows the shortest route

from flask import Flask, render_template, request, redirect, session, url_for

from graph import CAMPUS_LOCATIONS, CAMPUS_EDGES, build_graph
from dijkstra import find_shortest_path

app = Flask(__name__)

# Flask needs a secret key to keep login sessions secure.
# For a real project you would keep this private, but for a learning
# project this is fine.
app.secret_key = "campus-route-finder-secret-key"


@app.route("/")
def home():
    # When someone visits the homepage, send them to the login page.
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "" or password == "":
            error = "Please enter both a username and a password."
        else:
            # This is a simple "demo" login: any non-empty username
            # and password is accepted. We just remember the username.
            session["username"] = username
            return redirect(url_for("locations"))

    return render_template("login.html", error=error)


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
        start_name=CAMPUS_LOCATIONS[start]["name"],
        end_name=CAMPUS_LOCATIONS[end]["name"],
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)