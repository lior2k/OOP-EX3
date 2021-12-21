from unittest import TestCase
from src.DiGraph import *
graph = DiGraph()
graph.add_node(0, (1, 2))
graph.add_node(1, (2, 3))
graph.add_node(2, (3, 3))
graph.add_edge(0, 1, 1.5)
graph.add_edge(1, 2, 2.5)
graph.add_edge(0, 2, 0.5)


class TestDiGraph(TestCase):
    def test_v_size(self):
        self.assertEqual(graph.v_size(), 3)

    def test_e_size(self):
        self.assertEqual(graph.e_size(), 3)

    def test_get_mc(self):
        self.assertEqual(graph.get_mc(), 6)

    def test_add_edge(self):
        self.assertEqual(graph.all_out_edges_of_node(0)[1], 1.5)
        self.assertEqual(graph.all_out_edges_of_node(0)[2], 0.5)

    def test_add_node(self):
        self.assertEqual(graph.get_all_v()[0], MyNode(0, (1, 2)))

    def test_remove_node(self):
        graph.add_node(10, (10, 10))
        self.assertEqual(True, graph.remove_node(10))

    def test_remove_edge(self):
        graph.add_edge(1, 2, 0.5)
        self.assertEqual(True, graph.remove_edge(1, 2))

    def test_get_all_v(self):
        self.assertEqual(graph.get_all_v(), {0: MyNode(0, (1, 2)), 1: MyNode(1, (2, 3)), 2: MyNode(2, (3, 3))})

    def test_all_in_edges_of_node(self):
        self.assertEqual(graph.all_in_edges_of_node(1), {0: 1.5})

    def test_all_out_edges_of_node(self):
        self.assertEqual(graph.all_out_edges_of_node(1), {2: 2.5})
