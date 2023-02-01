from typing import Tuple

from graph.graph import Graph


def random_coloring(graph: Graph) -> int:
    total_colors = 0
    color_dict = dict()
    for node in graph.get_nodes():
        # node is not colored yet
        if node not in color_dict:
            # the first node encountered
            if total_colors == 0:
                color_dict[node] = total_colors
                total_colors += 1
            else:
                neighbors = graph.get_neighborhood(node)
                neighbor_colors = {color_dict[i] for i in neighbors if i in color_dict}
                if len(neighbor_colors) == total_colors:
                    color_dict[node] = total_colors
                    total_colors += 1
                else:
                    set_colors = set(range(total_colors))
                    random_available_color = set_colors.difference(neighbor_colors).pop()
                    color_dict[node] = random_available_color
    return total_colors


def find_clique(graph: Graph) -> Tuple[int, list]:
    """
    A greedy method to find a clique (which is unlikely to be the max clique).
    :param graph:
    :return:
    """
    clique = list()
    clique_set = set()
    node = graph.get_node_with_max_degree()
    _add_node_to_clique(clique, clique_set, node)
    while True:
        tmp_max_degree = 0
        tmp_node = None
        for next_node in graph.get_neighborhood(node):
            node_degree = graph.degree(next_node)
            if _node_filter(graph, next_node, node_degree, clique, clique_set):
                if node_degree > tmp_max_degree:
                    tmp_max_degree = node_degree
                    tmp_node = next_node
        if tmp_node:
            _add_node_to_clique(clique, clique_set, tmp_node)
            node = tmp_node
        else:
            break
    return len(clique), clique


def _add_node_to_clique(clique: list, clique_set: set, node):
    clique.append(node)
    clique_set.add(node)
    return


def _node_filter(graph: Graph, next_node, node_degree: int, clique: list, clique_set: set) -> bool:
    if node_degree < len(clique):
        return False
    if next_node in clique_set:
        return False
    return all(graph.has_edge(next_node, tmp_node) for tmp_node in clique_set)
