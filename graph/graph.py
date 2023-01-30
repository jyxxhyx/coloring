import networkx as nx


class Graph(object):
    def __init__(self):
        self.g = nx.Graph()
        # Precompute and store the node with max degree
        self._max_degree_node = None
        self.get_node_with_max_degree()
        return

    def add_nodes(self, node_list: list):
        for node in node_list:
            self.g.add_node(node)
        return

    def add_edge(self, from_node, to_node):
        self.g.add_edge(from_node, to_node)
        return

    def get_neighborhood(self, node):
        return self.g.neighbors(node)

    def get_connected_edges(self, node):
        # TODO Special treatment due to the undirected graph nature.
        #    The edges connected to node 4 might be (4, 2), (4, 6), (4, 8).
        #    However, the edges we use to define variables are (2, 4), (4, 6), (4, 8),
        #    where the first one is flipped.
        # TODO Thinking it again, we do not have variables based on edges.
        edges = self.g.edges(node)
        edges = [_flip_edge(u, v) for (u, v) in edges]
        return edges

    def get_nodes(self) -> list:
        return list(self.g.nodes)

    def get_edges(self) -> list:
        return list(self.g.edges)

    def get_node_with_max_degree(self):
        if self._max_degree_node is None:
            self._max_degree_node = self._get_node_with_max_degree()
        return self._max_degree_node

    def _get_node_with_max_degree(self):
        max_degree = 0
        max_node = None
        for node in self.get_nodes():
            degree = self.g.degree[node]
            if degree > max_degree:
                max_node = node
                max_degree = degree
        return max_node


def _flip_edge(u, v):
    return (u, v) if u <= v else (v, u)

