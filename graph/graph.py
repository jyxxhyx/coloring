import networkx as nx
from networkx import graph_clique_number


class Graph(object):
    def __init__(self):
        self._graph = nx.Graph()
        # Precompute and store the node with max degree
        self._max_degree_node = None
        self.get_node_with_max_degree()
        return

    def add_nodes(self, node_list: list):
        for node in node_list:
            self._graph.add_node(node)
        return

    def add_edge(self, from_node, to_node):
        self._graph.add_edge(from_node, to_node)
        return

    def get_neighborhood(self, node):
        return self._graph.neighbors(node)

    def get_nodes(self) -> list:
        return list(self._graph.nodes)

    def get_edges(self) -> list:
        return list(self._graph.edges)

    def get_node_with_max_degree(self):
        if self._max_degree_node is None:
            self._max_degree_node = self._get_node_with_max_degree()
        return self._max_degree_node

    def _get_node_with_max_degree(self):
        max_degree = 0
        max_node = None
        for node in self.get_nodes():
            degree = self._graph.degree[node]
            if degree > max_degree:
                max_node = node
                max_degree = degree
        return max_node

    def has_edge(self, node1, node2):
        return self._graph.has_edge(node1, node2)

    def degree(self, node):
        return self._graph.degree[node]

    def max_clique(self):
        return graph_clique_number(self._graph)
