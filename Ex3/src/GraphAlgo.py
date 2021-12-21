import json
import random
import traceback
from math import sqrt
from typing import List
import pygame

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import *
Black = (0, 0, 0)
White = (255, 255, 255)
Gray = (112, 128, 144)
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
                pos = nodes_dict['pos']
                poslist = pos.split(',')
                x = float(poslist[0])
                y = float(poslist[1])
                z = float(poslist[2])
                di_graph.add_node(nodes_dict['id'], (x, y, z))
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
        self.dijkstra_sp(src, dest)
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
        width, height = 1024, 800
        win = pygame.display.set_mode((width, height))
        win.fill((135, 206, 250))
        pygame.display.set_caption("Directed Weighted Graph")
        self.draw_graph(win)

        run = True
        while run:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()

    def dijkstra_sp(self, src_node: MyNode, dest_node: MyNode):
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
            if u == dest_node:
                break
            queue.remove(u)
            for neighbour_index in u.get_out_edges():
                v = self.graph.nodes_dict[neighbour_index]
                distance = u.get_dist() + u.get_out_edges()[neighbour_index]
                if distance < v.get_dist():
                    v.set_dist(distance)
                    v.set_prev(u)

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

    def draw_graph(self, win: pygame.Surface):
        max_xy = self.get_max_xy()
        radius = 5
        if max_xy == (-1, -1):
            for node in self.graph.get_all_v().values():
                pygame.draw.circle(win, node.get_tag(), (random.randrange(1, win.get_width()), random.randrange(1, win.get_height())), 5)
        else:
            for node in self.graph.get_all_v().values():
                if node.get_pos() is not None:
                    xy = self.get_scaled_xy(win, node.get_pos())
                    x = xy[0]
                    y = xy[1]
                else:
                    x = random.randrange(0, max_xy[0])
                    y = random.randrange(0, max_xy[1])

                pygame.draw.circle(win, node.get_tag(), (x, y), radius)

                for dest_index in node.get_out_edges():
                    dest_node = self.graph.nodes_dict[dest_index]
                    if dest_node.get_pos() is not None:
                        dest_xy = self.get_scaled_xy(win, dest_node.get_pos())
                        dest_x = dest_xy[0]
                        dest_y = dest_xy[1]
                    else:
                        dest_x = random.randrange(0, max_xy[0])
                        dest_y = random.randrange(0, max_xy[1])
                    pygame.draw.line(win, (0, 0, 139), (x, y), (dest_x, dest_y))
                    self.draw_arrow_head(win, x, y, dest_x, dest_y)
        pygame.display.update()

    def draw_arrow_head(self, win: pygame.surface, x1: float, y1: float, x2: float, y2: float) -> None:
        arrow_width = 15
        arrow_height = 2
        diff_x = x2 - x1
        diff_y = y2 - y1
        D = sqrt(diff_x*diff_x + diff_y*diff_y)
        xm = D - arrow_width
        xn = xm
        ym = arrow_height
        yn = -arrow_height

        sin = diff_y / D
        cos = diff_x / D

        x = xm*cos - ym*sin + x1
        ym = xm*sin + ym*cos + y1
        xm = x

        x = xn*cos - yn*sin + x1
        yn = xn*sin + yn*cos + y1
        xn = x

        points = ((x2, y2), (xm, ym), (xn, yn))

        pygame.draw.line(win,(0, 0, 139), (x1, y1), (x2, y2))
        pygame.draw.polygon(win, (0, 0, 139), points)

    def get_max_xy(self) -> ():
        x = -1
        y = -1
        for node in self.graph.get_all_v().values():
            if node.get_pos() is None:
                continue
            else:
                if node.get_pos()[0] > x:
                    x = node.get_pos()[0]
                if node.get_pos()[1] > y:
                    y = node.get_pos()[1]
        return x, y

    def get_min_xy(self):
        x = Max_Val
        y = Max_Val
        for node in self.graph.get_all_v().values():
            if node.get_pos() is None:
                continue
            else:
                if node.get_pos()[0] < x:
                    x = node.get_pos()[0]
                if node.get_pos()[1] < y:
                    y = node.get_pos()[1]
        return x, y

    def get_scaled_xy(self, win: pygame.Surface, coordinates : ()) -> ():
        max_xy = self.get_max_xy()
        min_xy = self.get_min_xy()
        wide_factor_x = win.get_width() / (max_xy[0] - min_xy[0])
        wide_factor_y = win.get_height() / (max_xy[1] - min_xy[1])
        x = (((coordinates[0] - min_xy[0]) * wide_factor_x)*0.65)+150
        y = (((coordinates[1] - min_xy[1]) * wide_factor_y)*0.65)+100
        return x, y


