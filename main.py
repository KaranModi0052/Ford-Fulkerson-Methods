from Aug_Path import *
from Source_Sink_Graph_Generator import generate_source_sink_graph

def print_table_header():
    header_format = "{:<15}\t{:<5}\t{:<5}\t{:<10}\t{:<6}\t{:<20}\t{:<24}\t{:<12}"
    header = header_format.format("Algorithm", "n", "r", "upperCap", "paths", "mean_length", "mean_proportional_length", "total_edges")
    print(header)
    print("-" * (len(header)+ 30))

def print_table_row(algorithm, n, r, upperCap, paths, mean_length, mean_proportional_length, total_edges):
    row_format = "{:<15}\t{:<5}\t{:<5}\t{:<10}\t{:<6}\t{:<20}\t{:<24}\t{:<12}"
    row = row_format.format(algorithm, n, r, upperCap, paths, mean_length, mean_proportional_length, total_edges)
    print(row)

def run_simulations(graph, n, r, upperCap, source, sink, total_edges):
    sap_flow, sap_paths, sap_mean_length, sap_mean_length_proportional = ford_fulkerson(graph, source, sink, shortest_augmenting_path_old)
    dfs_flow, dfs_paths, dfs_mean_length, dfs_mean_length_proportional = ford_fulkerson(graph, source, sink, dfs_like)
    maxcap_flow, maxcap_paths, maxcap_mean_length, maxcap_mean_length_proportional = ford_fulkerson(graph, source, sink, max_capacity)
    rand_flow, rand_paths, rand_mean_length, rand_mean_length_proportional = ford_fulkerson(graph, source, sink, Random_DFS_Like)

    print()
    print_table_header()
    print_table_row("SAP", n, r, upperCap, sap_paths, sap_mean_length, sap_mean_length_proportional, total_edges)
    print_table_row("DFS_Like", n, r, upperCap, dfs_paths, dfs_mean_length, dfs_mean_length_proportional, total_edges)
    print_table_row("Max_Capacity", n, r, upperCap, maxcap_paths, maxcap_mean_length, maxcap_mean_length_proportional, total_edges)
    print_table_row("Random_DFS_Like", n, r, upperCap, rand_paths, rand_mean_length, rand_mean_length_proportional, total_edges)
    print()


data = [
        [8,0.2,2],
        [40,0.2,2],
        [100,0.2,2],
        # [150,0.2,2],
        # [200,0.2,2],
        [100,0.3,2],
        # [200,0.3,2],
        [100,0.2,50],
        # [200,0.2,50],
        [100,0.3,50],
        # [200,0.3,50],
        ]

for i, (n, r, upperCap) in enumerate(data):
    # print(n, r, upperCap)
    generate_source_sink_graph(n, r, upperCap, i)
    adjacency_matrix, n, r, upperCap, source, sink, total_edges = load_graph('Generated_Source_Sink_Graph{}.txt'.format(i))
    run_simulations(adjacency_matrix, n, r, upperCap, source, sink, total_edges)