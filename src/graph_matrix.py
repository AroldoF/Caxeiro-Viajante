from dataclasses import dataclass, field

@dataclass
class Vertex:
    name: str

@dataclass
class Graph:
    vertices: list[Vertex] = field(default_factory=list)
    matrix: list[list[float]] = field(default_factory=list)

    def insert(self, vertex: Vertex, weights: list[float]):
        self.vertices.append(vertex)
        self.matrix.append(weights)

    def neighbors(self, vertex_index: int):
        print(self.matrix[vertex_index])


INF = float("inf")

matrix_grafo_1 = [
    [0,   2,   INF, 3,   6],
    [2,   0,   4,   3,   INF],
    [INF, 4,   0,   7,   3],
    [3,   3,   7,   0,   3],
    [6,   INF, 3,   3,   0],
]

matrix_grafo_2 = [
    [  0,  20, INF, INF, INF, INF, INF,  29, INF, INF, INF,  29,  37, INF, INF, INF, INF, INF],
    [ 20,   0,  25, INF, INF, INF, INF,  28, INF, INF, INF,  39, INF, INF, INF, INF, INF, INF],
    [INF,  25,   0,  25, INF, INF, INF,  30, INF, INF, INF, INF,  54, INF, INF, INF, INF, INF],
    [INF, INF,  25,   0,  39,  32,  42, INF,  23,  33, INF, INF, INF,  56, INF, INF, INF, INF],
    [INF, INF, INF,  39,   0,  12,  26, INF, INF,  19, INF, INF, INF, INF, INF, INF, INF, INF],
    [INF, INF, INF,  32,  12,   0,  17, INF, INF,  35,  30, INF, INF, INF, INF, INF, INF, INF],
    [INF, INF, INF,  42,  26,  17,   0, INF, INF, INF,  38, INF, INF, INF, INF, INF, INF, INF],
    [ 29,  28,  30, INF, INF, INF, INF,   0, INF, INF, INF,  25,  22, INF, INF, INF, INF, INF],
    [INF, INF, INF,  23, INF, INF, INF, INF,   0,  26, INF, INF,  34, INF, INF,  43, INF, INF],
    [INF, INF, INF,  33,  19,  35, INF, INF,  26,   0,  24, INF, INF,  30,  19, INF, INF, INF],
    [INF, INF, INF, INF, INF,  30,  38, INF, INF,  24,   0, INF, INF, INF,  26, INF, INF,  36],
    [ 29,  39, INF, INF, INF, INF, INF,  25, INF, INF, INF,   0,  27, INF, INF,  43, INF, INF],
    [ 37, INF,  54, INF, INF, INF, INF,  22,  34, INF, INF,  27,   0,  24, INF,  19, INF, INF],
    [INF, INF, INF,  56, INF, INF, INF, INF, INF,  30, INF, INF,  24,   0,  20,  19,  17, INF],
    [INF, INF, INF, INF, INF, INF, INF, INF, INF,  19,  26, INF, INF,  20,   0, INF,  18,  21],
    [INF, INF, INF, INF, INF, INF, INF, INF,  43, INF, INF,  43,  19,  19, INF,   0,  26, INF],
    [INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF,  17,  18,  26,   0,  15],
    [INF, INF, INF, INF, INF, INF, INF, INF, INF, INF,  36, INF, INF, INF,  21, INF,  15,   0],
]

graph = Graph(
    vertices=[Vertex(str(i)) for i in range(1, 6)],
    matrix=matrix_grafo_1
)

graph2 = Graph(
    vertices=[Vertex(str(i)) for i in range(1, 19)],
    matrix=matrix_grafo_2
)
