import random
import csv
from collections import deque

def generate_source_sink_graph(n, r, upper_cap, index):
    # Initialize vertices
    vertices = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(n)]

    # Initialize edges
    edges = set()
    
    graph = [[0 for x in range(n)] for y in range(n)] 

    # Create edges based on Euclidean distance
    for u in vertices:
        for v in vertices:
            if u != v and (u[0] - v[0])**2 + (u[1] - v[1])**2 <= r**2:
                rand = random.uniform(0, 1)
                if rand < 0.5:
                    if (u, v) not in edges and (v, u) not in edges:
                        edges.add((u, v))
                else:
                    if (u, v) not in edges and (v, u) not in edges:
                        edges.add((v, u))

    # Assign random capacities to edges
    edges_with_capacities = [{'edge': edge, 'cap': random.randint(1, upper_cap)} for edge in edges]
    
    for i, edge_info in enumerate(edges_with_capacities):
        edge = edge_info['edge']
        u=vertices.index(edge[0])
        v=vertices.index(edge[1])
        graph[u][v] = edge_info['cap']
    is_s_t_same = True
    
    while is_s_t_same:
        s = random.randint(0, n - 1)
        t = cyclic_path(graph, s)
        is_s_t_same = s==t
    
    write_to_file(graph, n, r, upper_cap, s, t, len(edges_with_capacities),  'Generated_Source_Sink_Graph{}.txt'.format(index))
    return graph, s, t

def cyclic_path(E, s):
    visited = [0] * len(E)
    length = [0] * len(E)
    queue = deque([s])
    visited[s] = 1
    while queue:
        u = queue.popleft()
        for v, capacity in enumerate(E[u]):
            if capacity > 0 and not visited[v]:
                queue.append(v)
                visited[v] = 1
                length[v] = length[u] + 1
    t = length.index(max(length))
    return t

def write_to_file(graph, n, r, upper_cap, source, sink, total_edges, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, r, upper_cap, source, sink, total_edges])
        for row in graph:
            writer.writerow(row)

