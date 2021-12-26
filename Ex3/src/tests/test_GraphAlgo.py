from unittest import TestCase
from src.GraphAlgo import GraphAlgo
A5_Algo = GraphAlgo()
A5_Algo.load_from_json('../A5.json')
# Algo1k = GraphAlgo()
# Algo1k.load_from_json('../1k_nodes.json')
# Algo10k = GraphAlgo()
# Algo10k.load_from_json('../10k_nodes.json')
# Algo100k = GraphAlgo()
# Algo100k.load_from_json('../100k_nodes.json')


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        self.assertEqual(A5_Algo.get_graph().v_size(), 48)
        self.assertEqual(A5_Algo.get_graph().e_size(), 166)

    def test_load_from_json(self):
        self.assertEqual(A5_Algo.load_from_json('../tests/A5.json'), True)

    def test_save_to_json(self):
        self.assertEqual(A5_Algo.save_to_json('../A5.json'), True)

    def test_shortest_path(self):
        dist, path = A5_Algo.shortest_path(13, 20)
        print(A5_Algo.is_connected())
        self.assertEqual(dist, 8.144672229691459)
        self.assertEqual(path, [13, 14, 29, 30, 31, 32, 21, 20])

    def test_center_point(self):
        node_id, dist = A5_Algo.centerPoint()
        self.assertEqual(node_id, 40)
        self.assertEqual(dist, 9.291743173960954)

    def test_TSP(self):
        path, dist = A5_Algo.TSP([5, 11, 27, 33, 40])
        self.assertEqual(path, [5, 13, 11, 13, 14, 29, 27, 29, 30, 31, 32, 21, 33, 21, 32, 31, 36, 37, 38, 39, 40])
        self.assertEqual(dist, 22.180370618918296)


    # def test_shortest_path_1k_nodes(self):
    #     Algo1k.shortest_path(312, 579)
    #
    # def test_center_point_1k_nodes(self):
    #     print(Algo1k.centerPoint())
    #
    # def test_TSP_1k_nodes(self):
    #     cities = [44, 384, 495]
    #     Algo1k.TSP(cities)
    #
    # def test_load_1k_nodes(self):
    #     Algo1k.load_from_json('../1k_nodes.json')
    #
    # def test_save_1k_nodes(self):
    #     Algo1k.save_to_json('1k_nodes.json')



    # def test_shortest_path_10k_nodes(self):
    #     Algo10k.shortest_path(3256, 3829)
    #
    # def test_center_point_10k_nodes(self):
    #     print(Algo10k.centerPoint())
    #
    # def test_TSP_10k_nodes(self):
    #     cities = [523, 3945, 6672]
    #     Algo10k.TSP(cities)
    #
    # def test_load_10k_nodes(self):
    #     Algo10k.load_from_json('../10k_nodes.json')
    #
    # def test_save_10k_nodes(self):
    #     Algo10k.load_from_json('../10k_nodes.json')




    # def test_shortest_path_100k_nodes(self):
    #     Algo100k.shortest_path(4857, 39945)
    #
    # def test_center_point_100k_nodes(self):
    #     Algo100k.centerPoint()
    #
    # def test_TSP_100k_nodes(self):
    #     cities = [48, 50285, 92884]
    #     Algo100k.TSP(cities)
    #
    # def test_load_100k_nodes(self):
    #     Algo100k.load_from_json('../100k_nodes.json')
    #
    # def test_save_100k_nodes(self):
    #     Algo100k.load_from_json('../100k_nodes.json')


    # def test_shortest_path_1M_nodes(self):
    #     self.fail()
    #
    # def test_center_point_1M_nodes(self):
    #     self.fail()
    #
    # def test_TSP_1M_nodes(self):
    #     self.fail()