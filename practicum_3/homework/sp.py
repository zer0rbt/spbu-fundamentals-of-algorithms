from typing import Any

import networkx as nx
import numpy as np
import heapq as hq

from src.plotting import plot_graph


def dijkstra_sp(G: nx.Graph, source_node="0") -> dict[Any, list[Any]]:
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes
    dist = {n: np.inf for n in G}  # key = destination node, value = length(source_node, node)
    rest_set = set(G.nodes())  # set of nodes not yet included into sp
    possible_edges_hq = []  # priority queue (= heapq), that contains of (path_lenght, (from_node, to_node))

    # Starting node has a path to itself and a zero distance from itself
    shortest_paths[source_node] = [source_node]

    possible_edge = (0, (source_node, source_node))
    dist[source_node] = 0
    hq.heappush(possible_edges_hq, possible_edge)

    while len(rest_set) > 0:
        edge_weight, edge = possible_edge
        cur_node = edge[1]
        rest_set.discard(cur_node)

        # Look for the minimum-weight edge from cur_node to one of its neighbors
        for node in G.neighbors(cur_node):
            new_edge_weight = G.edges[cur_node, node]["weight"] + edge_weight
            if dist[node] > new_edge_weight:
                # Update shortest path and distance to the current neighbor
                shortest_paths[node] = shortest_paths[cur_node] + [node]
                dist[node] = new_edge_weight
                # Push the neighbor's edge to the priority queue
                hq.heappush(possible_edges_hq, (new_edge_weight, (cur_node, node)))

        # Find the minimum-weight edge in the priority queue that leads to a node not included in the shortest path yet
        while possible_edge[1][1] not in rest_set:
            if len(possible_edges_hq) > 0:
                possible_edge = hq.heappop(possible_edges_hq)
            else:
                return shortest_paths

    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    shortest_paths = dijkstra_sp(G, source_node="0")
    test_node = "5"
    shortest_path_edges = [
        (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
        for i in range(len(shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)