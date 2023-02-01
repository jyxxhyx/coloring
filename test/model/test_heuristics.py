from unittest import TestCase

from graph.graph import Graph
from input_handler.reader import read_graph_from_file
from model.heuristics import find_clique
from util.util import add_input_cwd


class Test(TestCase):
    def test_find_large_clique(self):
        graph = read_graph_from_file(add_input_cwd('jean.col'))
        clique_size, clique = find_clique(graph)
        print(f'Clique found with size {clique_size}: {clique}')
        print(f'Max clique found with size {graph.max_clique()}')
