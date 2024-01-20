import heapq
import sys
import random
from copy import deepcopy
from Source_Sink_Graph_Generator import generate_source_sink_graph

def ford_fulkerson(graph, source, sink, augmenting_path_algorithm):
    graph = deepcopy(graph)
    rows = len(graph)
    parent = [-1] * rows
    max_flow = 0
    aug_paths = []
    while True:
        aug_path = augmenting_path_algorithm(graph, source, sink)
        if not aug_path:
            break
        aug_paths.append(aug_path)
        total_cap = 500000
        for (u, v, cap) in aug_path:
            total_cap = min(total_cap, graph[u][v])
        if (total_cap <= 0):
            break
        max_flow += total_cap
        for (u, v, cap) in aug_path:
            graph[u][v] = graph[u][v] - total_cap
            graph[v][u] = graph[v][u] + total_cap

    paths = len(aug_paths)
    if paths == 0:
        return max_flow, paths, 0, 0

    total_length = sum(len(path) for path in aug_paths)
    mean_length = total_length / paths
    max_length = max(len(path) for path in aug_paths)
    total_length = sum(len(path) / max_length for path in aug_paths)
    mean_length_proportional = total_length / paths

    return max_flow, paths, mean_length, mean_length_proportional


def get_path(current_vertex, parents, path):
        if current_vertex == -1:
                return path
        path = get_path(parents[current_vertex], parents, path)
        path.append(current_vertex)
        return path

def dijkstra(graph, source, s):
        v = len(graph[0])
        dist = [sys.maxsize] * v
        added = [False] * v
        for v in range(v):
                dist[v] = sys.maxsize
                added[v] = False
        dist[source] = 0
        parents = [-1] * v
        parents[source] = -1
        for i in range(1, v):
                nearest_vertex = -1
                min_dist = sys.maxsize
                for v in range(v):
                        if not added[v] and dist[v] < min_dist:
                                nearest_vertex = v
                                min_dist = dist[v]
                added[nearest_vertex] = True
                for v in range(v):
                        edge = 1 if graph[nearest_vertex][v]>0 else 0
                        if edge > 0 and min_dist + edge < dist[v]:
                                parents[v] = nearest_vertex
                                dist[v] = min_dist + edge
        return get_path(s, parents, [])

def shortest_augmenting_path(graph, source, sink):
    path = dijkstra(graph, source, sink)
    augument_path = []
    for i in range(1, len(path)):
        u, v = path[i-1], path[i]
        augument_path.append((u, v, graph[u][v]))
    return augument_path

def shortest_augmenting_path_old(graph, source, sink):
    priority_queue = [(0, source, [])]
    heapq.heapify(priority_queue)
    visited = set()
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current == sink:
            return path
        visited.add(current)
        for neighbor, capacity in enumerate(graph[current]):
            if neighbor not in visited and capacity > 0:
                heapq.heappush(priority_queue, (0, neighbor, path + [(current, neighbor, 1)]))
    return []

def dfs_like(graph, source, sink):
    priority_queue = [(float('inf'), source, [])]
    heapq.heapify(priority_queue)
    visited = set()

    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current == sink:
            return path
        visited.add(current)
        for neighbor, capacity in enumerate(graph[current]):
            if neighbor not in visited and capacity > 0:
                heapq.heappush(priority_queue, ((-1) * len(path), neighbor, path + [(current, neighbor, capacity)]))
    return []

def max_capacity(graph, source, sink):
    priority_queue = [(-float('inf'), source, [])]
    heapq.heapify(priority_queue)
    visited = set()
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current == sink:
            return path
        visited.add(current)
        for neighbor, capacity in enumerate(graph[current]):
            if neighbor not in visited:
                cap = (min(-capacity, len(path)), neighbor, path + [(current, neighbor, capacity)])
                heapq.heappush(priority_queue, cap )
    return []

def Random_DFS_Like(graph, source, sink):
    priority_queue = [(random.random(), source, [])]
    heapq.heapify(priority_queue)
    visited = set()
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current == sink:
            return path
        visited.add(current)
        for neighbor, capacity in enumerate(graph[current]):
            if neighbor not in visited and capacity > 0:
                heapq.heappush(priority_queue, (random.random(), neighbor, path + [(current, neighbor, capacity)]))
    return []

def load_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    header = lines[0].strip().split(',')
    n, r, upperCap, source, sink, total_edges = header
    adjacency_matrix = [list(map(int, line.strip().split(','))) for line in lines[1:]]
    return adjacency_matrix, int(n), float(r), int(upperCap), int(source), int(sink), int(total_edges)