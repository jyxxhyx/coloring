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
