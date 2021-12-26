Black = (0, 0, 0)
White = (255, 255, 255)
Gray = (112, 128, 144)


class MyNode:

    def __init__(self, node_id: int, pos: tuple = None):
        self.id: int = node_id
        self.in_edges: {int, float} = {}
        self.out_edges: {int, float} = {}
        self.tag = White
        self.dist = 0
        self.pos = pos
        self.prev = None

    def get_in_edges(self) -> dict:
        return self.in_edges

    def get_out_edges(self) -> dict:
        return self.out_edges

    def get_id(self) -> int:
        return self.id

    def get_tag(self):
        return self.tag

    def set_tag(self, color: tuple):
        self.tag = color

    def get_dist(self):
        return self.dist

    def set_dist(self, dist: float):
        self.dist = dist

    def get_pos(self):
        return self.pos

    def get_prev(self):
        return self.prev

    def set_prev(self, node):
        self.prev = node

    def add_edge(self, src: int, dest: int, weight: float):
        if src == self.id:
            self.out_edges[dest] = weight
        else:
            self.in_edges[src] = weight

    def remove_edge(self, src: int, dest: int) -> float:
        if self.id == src:
            return self.out_edges.pop(dest)
        else:
            return self.in_edges.pop(src)

    def copy(self):
        n = MyNode(self.get_id(), self.pos)
        n.out_edges = self.out_edges.copy()
        n.in_edges = self.in_edges.copy()
        return n

    def reverse(self):
        dict_copy = self.out_edges.copy()
        self.out_edges = self.in_edges
        self.in_edges = dict_copy

    # def __str__(self):
    #     return f"out edges: {self.out_edges} in edges: {self.in_edges}"
    #
    # def __repr__(self):
    #     return f"out edges: {self.out_edges} in edges: {self.in_edges}"

    def __str__(self):
        return f"{self.id}: |edges_out| {len(self.out_edges)} |edges_in| {len(self.in_edges)}"

    def __repr__(self):
        return f"{self.id}: |edges_out| {len(self.out_edges)} |edges_in| {len(self.in_edges)}"

    def __eq__(self, other):
        if isinstance(other, MyNode):
            if other.get_id() == self.get_id():
                return True
        return False
