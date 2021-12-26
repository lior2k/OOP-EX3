from unittest import TestCase
from src.mynode import MyNode
n = MyNode(0, (0.2, 0.4))
n.add_edge(0, 1, 2.5)  # out edge
n.add_edge(1, 0, 3.5)  # in edge


class TestMyNode(TestCase):
    def test_get_in_edges(self):
        in_edges = n.get_in_edges()
        self.assertEqual(in_edges, {1: 3.5})

    def test_get_out_edges(self):
        out_edges = n.get_out_edges()
        self.assertEqual(out_edges, {1: 2.5})

    def test_get_id(self):
        self.assertEqual(n.get_id(), 0)

    def test_get_tag(self):
        self.assertEqual(n.get_tag(), (255, 255, 255))

    def test_set_tag(self):
        n.set_tag((130, 140, 200))
        self.assertEqual(n.get_tag(), (130, 140, 200))

    def test_get_dist(self):
        self.assertEqual(n.get_dist(), 0)

    def test_set_dist(self):
        n.set_dist(123.123)
        self.assertEqual(n.get_dist(), 123.123)

    def test_get_pos(self):
        self.assertEqual(n.get_pos(), (0.2, 0.4))

    def test_add_edge(self):
        n.add_edge(0, 2, 1)
        self.assertEqual(n.get_out_edges()[2], 1)
        n.remove_edge(0, 2)

    def test_remove_edge(self):
        n.add_edge(0, 2, 1)
        self.assertEqual(n.get_out_edges()[2], n.remove_edge(0, 2))

    def test_copy(self):
        n2 = n.copy()
        self.assertEqual(n, n2)
