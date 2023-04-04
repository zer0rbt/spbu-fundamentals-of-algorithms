from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import heapq as hq
from src.plotting import plot_graph


# Sorry for my poor English...
def prim_mst(g: nx.Graph, start_node="0") -> set:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(g.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST
    possible_edges_hq = []
    last_visited_node = start_node

    mst_set.add(start_node)
    rest_set.discard(start_node)
    while len(rest_set) > 1:
        for node in g.neighbors(last_visited_node):  # Here we are adding edges from our last visited node.
            # tuple (weight, edge) in order to use heapq
            new_edge = (g.edges[last_visited_node, node]["weight"], last_visited_node, node)

            # Note: we could also do not include duplicate edges into a possible_edges, by adding this condition:
            # " ...and (reversed_edge[::-1] not in possible_edges) "
            # but tests show that if we do so, speed decreases on 6000%! <2.4s from 0.04s on g=1000, e=10000>
            if node not in mst_set:
                hq.heappush(possible_edges_hq, new_edge)

        possible_edge = hq.heappop(possible_edges_hq)

        # Here we are trying to find edge that would push our "frontline".
        # Note: these two conditions can't be False at the same time,
        #                                           because one of nodes is a last_visited_node and already in mst_set.
        while (possible_edge[1] in mst_set) and (possible_edge[2] in mst_set):
            possible_edge = hq.heappop(possible_edges_hq)

        else:
            mst_edges.add(possible_edge[1:])
            rest_set.discard(last_visited_node)

            # Here we are changing var"last_seen_node" to a new one; We have to use ternary operator because
            # we don't know where is the new node: on [1] or [2].
            # For ex.: l_v_n = 1 and possible_edge could be (1, v, w) as well as (u, 1, w).
            last_visited_node = possible_edge[1] if possible_edge[2] == last_visited_node else possible_edge[2]

            mst_set.add(last_visited_node)

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))
