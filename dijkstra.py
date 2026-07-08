# dijkstra.py
# This file contains the Dijkstra shortest-path algorithm.
# Dijkstra's algorithm finds the shortest total distance between
# a start location and an end location, even if there are many
# possible paths to choose from.

import heapq


def find_shortest_path(graph, start, end):
    """
    graph: dictionary from build_graph(), e.g. {"gate": [("library", 150), ...]}
    start: id of the starting location, e.g. "gate"
    end: id of the destination location, e.g. "sports"

    Returns a tuple: (path, total_distance)
    - path is a list of location ids in order, e.g. ["gate", "library", "admin"]
    - total_distance is the total distance in meters
    If there is no path, returns (None, None)
    """

    # distances holds the shortest known distance from start to every location.
    # We begin by assuming every location is "infinitely far away".
    distances = {}
    for location_id in graph:
        distances[location_id] = float("inf")
    distances[start] = 0

    # previous_location remembers which location we came from,
    # so we can rebuild the full path at the end.
    previous_location = {}

    # visited keeps track of locations we have already finished checking.
    visited = set()

    # priority_queue always gives us the closest unvisited location next.
    # Each item is (distance_so_far, location_id).
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)

        if current_location in visited:
            continue
        visited.add(current_location)

        # If we reached the destination, we can stop early.
        if current_location == end:
            break

        # Check every neighbor of the current location.
        for neighbor, edge_distance in graph[current_location]:
            if neighbor in visited:
                continue

            new_distance = current_distance + edge_distance

            # If we found a shorter way to reach this neighbor, remember it.
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_location[neighbor] = current_location
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # If the end location was never reached, there is no path.
    if distances[end] == float("inf"):
        return None, None

    # Rebuild the path by walking backwards from "end" to "start".
    path = [end]
    while path[-1] != start:
        path.append(previous_location[path[-1]])
    path.reverse()

    return path, distances[end]