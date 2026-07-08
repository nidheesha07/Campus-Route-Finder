# graph.py
# This file stores the campus map data:
# - Where each location is (for drawing on screen)
# - Which locations are connected to each other, and the distance between them

# Each location has a name and an (x, y) position for drawing on the map.
# The map area is 700 pixels wide and 500 pixels tall.
CAMPUS_LOCATIONS = {
    "gate": {"name": "Main Gate", "x": 50, "y": 250},
    "parking": {"name": "Parking", "x": 50, "y": 100},
    "library": {"name": "Library", "x": 250, "y": 100},
    "cafeteria": {"name": "Cafeteria", "x": 250, "y": 400},
    "admin": {"name": "Admin Block", "x": 450, "y": 100},
    "hostel": {"name": "Hostel", "x": 450, "y": 400},
    "auditorium": {"name": "Auditorium", "x": 450, "y": 250},
    "sports": {"name": "Sports Complex", "x": 650, "y": 250},
}

# Each connection (edge) is: (location_1, location_2, distance_in_meters)
CAMPUS_EDGES = [
    ("gate", "parking", 80),
    ("gate", "library", 150),
    ("gate", "cafeteria", 180),
    ("library", "admin", 120),
    ("library", "auditorium", 200),
    ("cafeteria", "hostel", 150),
    ("cafeteria", "auditorium", 220),
    ("admin", "auditorium", 100),
    ("hostel", "auditorium", 130),
    ("auditorium", "sports", 150),
    ("admin", "sports", 250),
    ("hostel", "sports", 180),
]


def build_graph():
    """
    Turns the simple list of edges (CAMPUS_EDGES) into a dictionary
    that tells us, for each location, which locations it connects to
    and how far away they are.

    Example result:
    {
        "gate": [("parking", 80), ("library", 150), ("cafeteria", 180)],
        "parking": [("gate", 80)],
        ...
    }
    """
    graph = {}

    # First, make sure every location has an empty list to start with
    for location_id in CAMPUS_LOCATIONS:
        graph[location_id] = []

    # Now fill in the connections. Since paths work both ways,
    # we add the connection in both directions.
    for point_a, point_b, distance in CAMPUS_EDGES:
        graph[point_a].append((point_b, distance))
        graph[point_b].append((point_a, distance))

    return graph