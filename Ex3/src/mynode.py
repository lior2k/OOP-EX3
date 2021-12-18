
class MyNode:

    def __init__(self, node_id: int):
        self.id = node_id
        self.location = None
        self.in_edges = {}
        self.out_edges = {}

    def get_in_edges(self) -> dict:
        return self.in_edges

    def get_out_edges(self) -> dict:
        return self.out_edges

    def get_id(self) -> int:
        return self.id

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
        n = MyNode(self.get_id())
        n.out_edges = self.out_edges.copy()
        n.in_edges = self.in_edges.copy()
        n.location = self.location
        return n

    def __str__(self):
        return f"out edges: {self.out_edges} in edges: {self.in_edges}"

    def __repr__(self):
        return f"out edges: {self.out_edges} in edges: {self.in_edges}"
