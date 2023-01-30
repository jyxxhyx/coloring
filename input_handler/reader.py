from graph.graph import Graph


def read_graph_from_file(file_name):
    num_nodes, num_edges = 0, 0
    graph = Graph()
    with open(file_name, mode='r', encoding='utf-8') as r:
        line = r.readline()
        while line:
            if line[0] == 'c':
                pass
            elif line[0] == 'p':
                temp_list = line.split(' ')
                num_nodes = int(temp_list[-2])
                num_edges = int(temp_list[-1])
                node_list = [i for i in range(1, num_nodes + 1)]
                graph.add_nodes(node_list)
            else:
                temp_list = line.split(' ')
                from_node = int(temp_list[1])
                to_node = int(temp_list[2])
                graph.add_edge(from_node, to_node)
            line = r.readline()
    # assert len(graph.get_edges()) == num_edges / 2
    return graph
