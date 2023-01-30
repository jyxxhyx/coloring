import networkx as nx


class Graph(object):
    def __init__(self):
        self.g = nx.Graph()
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


def _flip_edge(u, v):
    return (u, v) if u <= v else (v, u)

