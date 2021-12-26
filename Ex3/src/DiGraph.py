import random

from mynode import MyNode
from GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes_dict = {}
        self.node_size = 0
        self.edge_size = 0
        self.mc = 0

    def v_size(self):
        return self.node_size

    def e_size(self):
        return self.edge_size

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 == id2:
            return False
        if self.nodes_dict.keys().__contains__(id1) and self.nodes_dict.keys().__contains__(id2):
            self.nodes_dict[id1].add_edge(id1, id2, weight)
            self.nodes_dict[id2].add_edge(id1, id2, weight)
            self.mc += 1
            self.edge_size += 1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.nodes_dict.keys().__contains__(node_id):
            return False
        if pos is None:
            x = random.random() * 800
            y = random.random() * 600
            pos = (x, y, 0)
        n = MyNode(node_id, pos)
        self.nodes_dict[node_id] = n
        self.mc += 1
        self.node_size += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if self.nodes_dict.keys().__contains__(node_id):
            for dest in self.nodes_dict.get(node_id).get_out_edges():
                temp = self.nodes_dict[dest]
                temp.get_in_edges().pop(node_id)
            self.nodes_dict.pop(node_id)
            self.mc += 1
            self.node_size -= 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.nodes_dict.keys().__contains__(node_id1) and self.nodes_dict.keys().__contains__(node_id2):
            if self.nodes_dict.get(node_id1).get_out_edges().__contains__(node_id2) and self.nodes_dict.get(node_id2).get_in_edges().__contains__(node_id1):
                self.nodes_dict.get(node_id1).get_out_edges().pop(node_id2)
                self.nodes_dict.get(node_id2).get_in_edges().pop(node_id1)
                self.mc += 1
                self.edge_size -= 1
                return True
        return False

    def get_all_v(self) -> dict:
        return self.nodes_dict

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes_dict[id1].get_in_edges()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes_dict[id1].get_out_edges()

    def __str__(self):
        return f"|V|={self.node_size} |E|={self.edge_size}"
