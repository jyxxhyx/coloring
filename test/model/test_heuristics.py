from unittest import TestCase

from graph.graph import Graph
from input_handler.reader import read_graph_from_file
from model.heuristics import find_clique, random_coloring
from util.util import add_input_cwd


class Test(TestCase):
    def setUp(self):
        self.graph = read_graph_from_file(add_input_cwd('jean.col'))

    def test_find_large_clique(self):
        clique_size, clique = find_clique(self.graph)
        print(f'Clique found with size {clique_size}: {clique}')
        print(f'Max clique found with size {self.graph.max_clique()}')
        self.assertEqual(self.graph.max_clique(), 10)

    def test_random_coloring(self):
        num_color = random_coloring(self.graph)
        print(f'Coloring is: {num_color}')
        self.assertEqual(num_color, 10)

    def test_random_coloring_with_capacity(self):
        capacity = 3
        num_color = random_coloring(self.graph, capacity)
        print(f'Coloring with capacity {capacity} is: {num_color}')
