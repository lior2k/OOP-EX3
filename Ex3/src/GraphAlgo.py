import json
import math
import traceback
from math import sqrt
from typing import List
import pygame
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import *
Black = (0, 0, 0)
White = (255, 255, 255)
Gray = (112, 128, 144)
Max_Value = math.inf


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
        for node in self.graph.get_all_v().values():
            key = node.get_id()
            out_edges = node.get_out_edges()
            if node.get_pos() is not None:
                nodes_list.append({"pos": f"{node.get_pos()[0]},{node.get_pos()[1]},{node.get_pos()[2]}", "id": key})
            else:
                nodes_list.append({"id": key})
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
        src = self.graph.get_all_v()[id1]
        dest = self.graph.get_all_v()[id2]
        self.dijkstra(src)
        if dest.get_dist() == Max_Value:
            return Max_Value, []
        while dest is not None:
            path.append(dest.get_id())
            dest = dest.get_prev()
        path.reverse()
        return self.graph.get_all_v()[id2].get_dist(), path

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        global White, Gray, Black, Max_Value
        total_dist = 0
        for node_index in node_lst:
            self.graph.get_all_v()[node_index].set_tag(White)
        ans = []
        while len(node_lst) > 0:
            if len(node_lst) == 1:
                ans.append(node_lst[0])
                break
            for node_index in node_lst:
                n = self.graph.get_all_v()[node_index]
                if n.get_tag() == Black:
                    node_lst.remove(node_index)
            flag = 0
            for node_index in node_lst:
                n = self.graph.get_all_v()[node_index]
                if n.get_tag() == Gray:
                    flag += 1
            if flag == len(node_lst):
                return [], Max_Value
            n1 = self.graph.get_all_v()[node_lst.pop(0)]
            if len(node_lst) == 0:
                break
            n2 = self.graph.get_all_v()[node_lst[0]]
            dist, path = self.shortest_path(n1.get_id(), n2.get_id())
            if dist == Max_Value:
                node_lst.append(n1.get_id())
                n1.set_tag(Gray)
                continue
            total_dist += dist
            for intersection in path:
                if ans.__contains__(intersection) and intersection is not n2.get_id():
                    self.graph.get_all_v()[intersection].set_tag(Black)
                if intersection is not n2.get_id():
                    ans.append(intersection)
        return ans, total_dist

    def centerPoint(self) -> (int, float):
        global Max_Value
        if not self.is_connected():
            return None, Max_Value
        shortest_dist = Max_Value
        node_id = -1
        for node in self.graph.get_all_v().values():
            self.dijkstra(node)
            max_dist = -1
            for vertice in self.graph.get_all_v().values():
                if vertice.get_dist() > max_dist:
                    max_dist = vertice.get_dist()
            if max_dist < shortest_dist:
                shortest_dist = max_dist
                node_id = node.get_id()
        return node_id, shortest_dist

    def plot_graph(self) -> None:
        width, height = 800, 600
        win = pygame.display.set_mode((width, height))
        win.fill(Gray)
        pygame.display.set_caption("Directed Weighted Graph")
        pygame.font.init()
        self.draw_graph(win)
        run = True
        while run:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()

    def dijkstra(self, src_node: MyNode):
        global Max_Value
        queue = {}
        for node in self.graph.get_all_v().values():
            node.set_prev(None)
            node.set_dist(Max_Value)
            queue[node.get_id()] = node
        src_node.set_dist(0)
        while len(queue) > 0:
            min_dist = Max_Value
            key = -1
            for node in queue.values():
                if node.get_dist() < min_dist:
                    min_dist = node.get_dist()
                    key = node.get_id()
            if key == -1:
                break
            u = self.graph.get_all_v()[key]
            queue.pop(u.get_id())
            for neighbour_index in u.get_out_edges():
                v = self.graph.get_all_v()[neighbour_index]
                distance = u.get_dist() + u.get_out_edges()[neighbour_index]
                if distance < v.get_dist():
                    v.set_dist(distance)
                    v.set_prev(u)

    def is_connected(self) -> bool:
        n = None
        for node in self.graph.get_all_v().values():
            n = node
            break
        if n is None:
            return False
        self.bfs(n)
        for node in self.graph.get_all_v().values():
            if node.get_tag() == White:
                return False
        self.reverse_graph()
        self.bfs(n)
        self.reverse_graph()
        for node in self.graph.get_all_v().values():
            if node.get_tag() == White:
                return False
        return True

    def bfs(self, s: MyNode):
        global White, Black, Gray, Max_Value
        for node in self.graph.get_all_v().values():
            node.set_tag(White)
            node.set_dist(Max_Value)
        s.set_tag(Gray)
        s.set_dist(0)
        queue = [s]
        while len(queue) > 0:
            u = queue.pop(0)
            for neighbour_index in u.get_out_edges():
                v = self.graph.get_all_v()[neighbour_index]
                if v.get_tag() == White:
                    v.set_tag(Gray)
                    v.set_dist(u.get_dist()+1)
                    queue.append(v)
            u.set_tag(Black)

    def reverse_graph(self):
        for node in self.graph.get_all_v().values():
            node.reverse()

    def draw_graph(self, win: pygame.Surface):
        radius = 5
        max_xy = self.get_max_xy()
        min_xy = self.get_min_xy()
        for node in self.graph.get_all_v().values():
            xy = self.get_scaled_xy(win, node.get_pos(), max_xy, min_xy)
            x = xy[0]
            y = xy[1]
            pygame.draw.circle(win, node.get_tag(), (x, y), radius)
            pos = str(node.get_id())
            font = pygame.font.SysFont('Ariel', 20)
            text = font.render(pos, True, (255, 0, 0))
            win.blit(text, (x - 15, y - 15, 100, 100))
            for dest_index in node.get_out_edges():
                dest_node = self.graph.get_all_v()[dest_index]
                dest_xy = self.get_scaled_xy(win, dest_node.get_pos(), max_xy, min_xy)
                dest_x = dest_xy[0]
                dest_y = dest_xy[1]
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
        pygame.draw.line(win, (0, 0, 139), (x1, y1), (x2, y2))
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
        x = Max_Value
        y = Max_Value
        for node in self.graph.get_all_v().values():
            if node.get_pos() is None:
                continue
            else:
                if node.get_pos()[0] < x:
                    x = node.get_pos()[0]
                if node.get_pos()[1] < y:
                    y = node.get_pos()[1]
        return x, y

    def get_scaled_xy(self, win: pygame.Surface, coordinates: (), max_xy: (), min_xy: ()) -> ():
        wide_factor_x = win.get_width() / (max_xy[0] - min_xy[0])
        wide_factor_y = win.get_height() / (max_xy[1] - min_xy[1])
        x = (((coordinates[0] - min_xy[0]) * wide_factor_x)*0.65)+150
        y = (((coordinates[1] - min_xy[1]) * wide_factor_y)*0.65)+100
        return x, y

    def init_random_graph(self, nodes_amount: int, out_edges_per_node: int):
        graph = DiGraph()
        i = 0
        while i < nodes_amount:
            graph.add_node(i)
            i += 1
        i = 0
        while i < nodes_amount:
            k = 0
            while k < out_edges_per_node:
                graph.add_edge(i, random.randrange(0, nodes_amount), random.randrange(1, 10))
                k += 1
            i += 1
        self.__init__(graph)
