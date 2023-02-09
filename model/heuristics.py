from typing import Tuple

from graph.graph import Graph


def random_coloring(graph: Graph) -> int:
    color_count = 0
    color_dict = dict()
    for node in graph.get_nodes():
        # only process node that is not colored yet
        if node in color_dict:
            continue
        neighbors = graph.get_neighborhood(node)
        neighbor_colors = {color_dict[v] for v in neighbors if v in color_dict}
        if len(neighbor_colors) == color_count:
            # Case 1. Need a new color.
            color_dict[node] = color_count
            color_count += 1
        else:
            # Case 2. Use an existing color (randomly pop one).
            color_set = set(range(color_count))
            available_color = color_set.difference(neighbor_colors).pop()
            color_dict[node] = available_color
    return color_count


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
                # 多个点可以加入完全子图时，选择度最大的点加入
                if node_degree > tmp_max_degree:
                    tmp_max_degree = node_degree
                    tmp_node = next_node
        if tmp_node:
            _add_node_to_clique(clique, clique_set, tmp_node)
            node = tmp_node
        else:
            # 没有点可以加，则退出循环
            break
    return len(clique), clique


def _add_node_to_clique(clique: list, clique_set: set, node):
    clique.append(node)
    clique_set.add(node)
    return


def _node_filter(graph: Graph, next_node, node_degree: int, clique: list, clique_set: set) -> bool:
    """
    判断一个点是否可以加入完全子图集合中。
    情况1. 点的度小于完全子图的点数量，不可以加入（short-cut)
    情况2. 点已经出现在完全子图中，不可以加入（short-cut）
    情况3. 如果点和完全子图中每个点都相连，可以加入
    :param graph: 图
    :param next_node: 待判断点
    :param node_degree: 点对应的度
    :param clique: 当前的完全子图list
    :param clique_set: 当前的完全子图set
    :return:
    """
    if node_degree < len(clique):
        return False
    if next_node in clique_set:
        return False
    return all(graph.has_edge(next_node, tmp_node) for tmp_node in clique_set)
