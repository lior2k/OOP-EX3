from unittest import TestCase
from src.GraphAlgo import GraphAlgo
Algo = GraphAlgo()
Algo.load_from_json('../data/1000Nodes.json')


class TestGraphAlgo(TestCase):
    # def test_get_graph(self):
    #     self.assertEqual(Algo.get_graph().v_size(), 48)
    #     self.assertEqual(Algo.get_graph().e_size(), 166)
    #
    # def test_load_from_json(self):
    #     self.assertEqual(Algo.load_from_json('../data/A5.json'), True)
    #
    # def test_save_to_json(self):
    #     self.assertEqual(Algo.save_to_json('A5.json'), True)
    #
    # def test_shortest_path(self):
    #     dist, path = Algo.shortest_path(13, 20)
    #     print(Algo.is_connected())
    #     self.assertEqual(dist, 8.144672229691459)
    #     self.assertEqual(path, [13, 14, 29, 30, 31, 32, 21, 20])
    #
    # def test_plot_graph(self):
    #     self.fail()
    #
    # def test_center_point(self):
    #     node_id, dist = Algo.centerPoint()
    #     self.assertEqual(node_id, 40)
    #     self.assertEqual(dist, 9.291743173960954)
    #
    # def test_TSP(self):
    #     path, dist = Algo.TSP([5, 11, 27, 33, 40])
    #     self.assertEqual(path, [5, 13, 11, 13, 14, 29, 27, 29, 30, 31, 32, 21, 33, 21, 32, 31, 36, 37, 38, 39, 40])
    #     self.assertEqual(dist, 22.180370618918296)


    def test_shortest_path_1k_nodes(self):
        dist, path = Algo.shortest_path(25, 32)
        self.assertEqual(dist, 235)

    def test_center_point_1k_nodes(self):
        id, dist = Algo.centerPoint()
        self.assertEqual(id, 362)

    def test_TSP_1k_nodes(self):
        self.fail()


    # def test_shortest_path_10k_nodes(self):
    #     self.fail()
    #
    # def test_center_point_10k_nodes(self):
    #     self.fail()
    #
    # def test_TSP_10k_nodes(self):
    #     self.fail()


    # def test_shortest_path_100k_nodes(self):
    #     self.fail()
    #
    # def test_center_point_100k_nodes(self):
    #     self.fail()
    #
    # def test_TSP_100k_nodes(self):
    #     self.fail()


    # def test_shortest_path_1M_nodes(self):
    #     self.fail()
    #
    # def test_center_point_1M_nodes(self):
    #     self.fail()
    #
    # def test_TSP_1M_nodes(self):
    #     self.fail()