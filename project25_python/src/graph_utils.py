# graph_utils.py
from collections import deque

def build_graph(vertices, edges, undirected=True):
    """Builds an adjacency list representation of the graph."""
    vertex_set = set(vertices)
    graph = {vertex: [] for vertex in vertices}

    for u, v in edges:
        if u not in vertex_set:
            raise ValueError(f"Edge contains unknown vertex: '{u}'")

        if v not in vertex_set:
            raise ValueError(f"Edge contains unknown vertex: '{v}'")

        if u == v:
            continue

        graph[u].append(v)
        if undirected:
            graph[v].append(u)

    return graph


def find_reachable_stations(graph, start, max_distance, forbidden):
    """Finds stations reachable from the start station using modified BFS."""
    if start not in graph:
        raise ValueError(f"Start station '{start}' does not exist in graph.")

    if start in forbidden:
        return set(), {}

    visited = set()
    distance = {}
    queue = deque()

    visited.add(start)
    distance[start] = 0
    queue.append(start)

    while queue:
        current = queue.popleft()

        if distance[current] == max_distance:
            continue

        for neighbor in graph[current]:
            if neighbor in forbidden or neighbor in visited:
                continue

            new_distance = distance[current] + 1
            if new_distance <= max_distance:
                visited.add(neighbor)
                distance[neighbor] = new_distance
                queue.append(neighbor)

    return visited, distance