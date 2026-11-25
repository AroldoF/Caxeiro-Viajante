from dataclasses import dataclass, field


@dataclass
class Vertex:
    name: str
    edges: list["Edge"] = field(default_factory=list)


@dataclass
class Edge:
    destination: Vertex
    weight: float


@dataclass
class Graph:
    vertices: list[Vertex] = field(default_factory=list)


def create_graph(
    vertex_count: int,
    connections: list[tuple[int, int, float]]
) -> Graph:
    vertices = [
        Vertex(str(i))
        for i in range(1, vertex_count + 1)
    ]

    for origin, destination, weight in connections:
        v1 = vertices[origin - 1]
        v2 = vertices[destination - 1]

        v1.edges.append(Edge(v2, weight))
        v2.edges.append(Edge(v1, weight))

    return Graph(vertices)


# Grafo 1 — 5 vértices
edges_grafo_1 = [
    (1, 2, 2),
    (1, 4, 3),
    (1, 5, 6),
    (2, 3, 4),
    (2, 4, 3),
    (3, 4, 7),
    (3, 5, 3),
    (4, 5, 3),
]

# Grafo 2 — 18 vértices
edges_grafo_2 = [
    (1, 2, 20),
    (1, 8, 29),
    (1, 12, 29),
    (1, 13, 37),
    (2, 3, 25),
    (2, 8, 28),
    (2, 12, 39),
    (3, 4, 25),
    (3, 8, 30),
    (3, 13, 54),
    (4, 5, 39),
    (4, 6, 32),
    (4, 7, 42),
    (4, 9, 23),
    (4, 10, 33),
    (4, 14, 56),
    (5, 6, 12),
    (5, 7, 26),
    (5, 10, 19),
    (6, 7, 17),
    (6, 10, 35),
    (6, 11, 30),
    (7, 11, 38),
    (8, 12, 25),
    (8, 13, 22),
    (9, 10, 26),
    (9, 13, 34),
    (9, 16, 43),
    (10, 11, 24),
    (10, 14, 30),
    (10, 15, 19),
    (11, 15, 26),
    (11, 18, 36),
    (12, 13, 27),
    (12, 16, 43),
    (13, 14, 24),
    (13, 16, 19),
    (14, 15, 20),
    (14, 16, 19),
    (14, 17, 17),
    (15, 17, 18),
    (15, 18, 21),
    (16, 17, 26),
    (17, 18, 15),
]


graph = create_graph(5, edges_grafo_1)
graph2 = create_graph(18, edges_grafo_2)