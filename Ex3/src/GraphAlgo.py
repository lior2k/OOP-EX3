import json
import traceback
from typing import List

import pygame

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import *
Black = 0
White = 255
Gray = 153
Max_Val = 10000000


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = None):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'r') as f:
                data_dict = json.load(f)
        except FileNotFoundError:
            traceback.print_exc()
            print('graph was not loaded')
            return False
        di_graph = DiGraph()
        nodes = data_dict['Nodes']
        edges = data_dict['Edges']
        for nodes_dict in nodes:
            if nodes_dict.keys().__contains__('pos'):
                di_graph.add_node(nodes_dict['id'], nodes_dict['pos'])
            else:
                di_graph.add_node(nodes_dict['id'])
        for edges_dict in edges:
            di_graph.add_edge(edges_dict['src'], edges_dict['dest'], edges_dict['w'])
        self.__init__(di_graph)
        return True

    def save_to_json(self, file_name: str) -> bool:
        edges_list = []
        nodes_list = []
        for node in self.graph.nodes_dict.values():
            key = node.get_id()
            out_edges = node.get_out_edges()
            nodes_list.append({'pos': node.get_pos(), 'id': key})
            for dest in out_edges:
                edges_list.append({'src': key, 'w': out_edges[dest], 'dest': dest})

        data_dict = {'Edges': edges_list, 'Nodes': nodes_list}
        try:
            with open(file_name, 'w') as f:
                json.dump(data_dict, f, indent=2)
        except FileNotFoundError:
            traceback.print_exc()
            print('graph was not saved')
            return False
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        path = []
        src = self.graph.nodes_dict[id1]
        dest = self.graph.nodes_dict[id2]
        self.dijkstra(src)
        if dest.get_dist() == Max_Val:
            return Max_Val, []
        while dest is not None:
            path.append(dest.get_id())
            dest = dest.get_prev()
        path.reverse()
        return self.graph.nodes_dict[id2].get_dist(), path

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        global White, Gray, Black, Max_Val
        total_dist = 0
        for node in self.graph.nodes_dict.values():
            node.set_tag(White)
        ans = []
        while len(node_lst) > 0:
            if len(node_lst) == 1:
                ans.append(node_lst[0])
                break
            for node_index in node_lst:
                n = self.graph.nodes_dict[node_index]
                if n.get_tag() == Black:
                    node_lst.remove(node_index)
            n1 = self.graph.nodes_dict[node_lst.pop(0)]
            if len(node_lst) == 0:
                break
            n2 = self.graph.nodes_dict[node_lst[0]]
            dist, path = self.shortest_path(n1.get_id(), n2.get_id())
            total_dist += dist
            for intersection in path:
                if ans.__contains__(intersection) and intersection is not n2.get_id():
                    self.graph.nodes_dict[intersection].set_tag(Black)
                if intersection is not n2.get_id():
                    ans.append(intersection)
        return ans, total_dist

    def centerPoint(self) -> (int, float):
        global Max_Val
        if not self.is_connected():
            return -1, Max_Val
        shortest_dist = Max_Val
        node_id = -1
        for node in self.graph.nodes_dict.values():
            self.dijkstra(node)
            max_dist = -1
            for vertice in self.graph.nodes_dict.values():
                if vertice.get_dist() > max_dist:
                    max_dist = vertice.get_dist()
            if max_dist < shortest_dist:
                shortest_dist = max_dist
                node_id = node.get_id()
        return node_id, shortest_dist

    def plot_graph(self) -> None:
        WIDTH, HEIGHT = 600, 600
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()


    def dijkstra(self, src_node: MyNode):
        global Max_Val
        queue = []
        for node in self.graph.nodes_dict.values():
            node.set_prev(None)
            node.set_dist(Max_Val)
            queue.append(node)
        src_node.set_dist(0)
        while len(queue) > 0:
            min_dist = Max_Val
            key = -1
            for node in queue:
                if node.get_dist() < min_dist:
                    min_dist = node.get_dist()
                    key = node.get_id()
            if key == -1:
                break
            u = self.graph.nodes_dict[key]
            queue.remove(u)
            for neighbour_index in u.get_out_edges():
                v = self.graph.nodes_dict[neighbour_index]
                distance = u.get_dist() + u.get_out_edges()[neighbour_index]
                if distance < v.get_dist():
                    v.set_dist(distance)
                    v.set_prev(u)

    def is_connected(self) -> bool:
        n = None
        for node in self.graph.nodes_dict.values():
            n = node
            break
        if n is None:
            return False
        self.bfs(n)
        for node in self.graph.nodes_dict.values():
            if node.get_dist() == Max_Val:
                return False
        return True

    def bfs(self, s: MyNode):
        global White, Black, Gray, Max_Val
        for node in self.graph.nodes_dict.values():
            node.set_tag(White)
            node.set_dist(Max_Val)
        s.set_tag(Gray)
        s.set_dist(0)
        queue = [s]
        while len(queue) > 0:
            u = queue.pop(0)
            for neighbour_index in u.get_out_edges():
                v = self.graph.nodes_dict[neighbour_index]
                if v.get_tag() == White:
                    v.set_tag(Gray)
                    v.set_dist(u.get_dist()+1)
                    queue.append(v)
            u.set_tag(Black)
