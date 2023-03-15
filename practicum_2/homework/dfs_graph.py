import queue
from typing import Any

import networkx as nx

from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


# I think here you can easily understand all code without many comments, just by reading variable names
def dfs_iterative(G: nx.Graph, node: Any) -> None:
    visited = {n: False for n in G}
    ways_q = queue.LifoQueue()

    ways_q.put(node)
    while not ways_q.empty():
        current_node = ways_q.get()
        if visited[current_node]:
            continue

        visit(current_node)
        visited[current_node] = True

        # Appending not visited nodes to lifoQ
        not_visited_nodes_list = list(filter(lambda neighbor: not visited[neighbor], G.neighbors(current_node)))
        [ways_q.put(neighbor_node) for neighbor_node in not_visited_nodes_list]


# Pretty same as previous: variables have easy-to-understand names and there are not many comments
def topological_sort(G: nx.DiGraph, node: Any) -> None:
    visited = {n: False for n in G}
    ways_q = queue.LifoQueue()

    ways_q.put(node)
    while not ways_q.empty():
        current_node = ways_q.get()
        if visited[current_node]:
            continue

        unvisited_ancestors = list(filter(lambda ancestor: not visited[ancestor], nx.ancestors(G, current_node)))
        if len(unvisited_ancestors) > 0:  # This guard statement catches nodes with unvisited ancestors
            continue

        visit(current_node)
        visited[current_node] = True

        # Adding successors into a LIFO queue.
        [ways_q.put(successor) for successor in G.successors(current_node)]


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("graph_2.edgelist", create_using=nx.Graph) # Changed because of "FileNotFoundError"
    # plot_graph(G)

    print("Iterative DFS")
    print("-" * 32)
    dfs_iterative(G, node="0")
    print()

    G = nx.read_edgelist(
        "graph_2.edgelist", create_using=nx.DiGraph
    )
    plot_graph(G)
    print("Topological sort")
    print("-" * 32)
    topological_sort(G, node="0")
