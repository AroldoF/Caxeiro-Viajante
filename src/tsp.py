"""Modelos, conversões e algoritmos para o Problema do Caixeiro Viajante."""
from __future__ import annotations
import itertools
import heapq
import time
from dataclasses import dataclass
import networkx as nx
from graph_list import edges_grafo_1, edges_grafo_2

@dataclass
class TSPResult:
    route: list[int]
    cost: float
    steps: list[list[int]]
    elapsed: float

def graph_from_edges(vertex_count, edges):
    graph = nx.Graph()
    graph.add_nodes_from(range(1, vertex_count + 1))
    graph.add_weighted_edges_from(edges)
    return graph

def selected_graph(number):
    return graph_from_edges(5, edges_grafo_1) if number == 5 else graph_from_edges(18, edges_grafo_2)

def shortest_path_metric(graph):
    """Cria a matriz completa de menores caminhos para um grafo não completo."""
    nodes = list(graph.nodes)
    distances = {source: dijkstra(graph, source) for source in nodes}
    return nodes, [[distances[a][b] for b in nodes] for a in nodes]

def dijkstra(graph, source):
    distances = {node: float("inf") for node in graph.nodes}
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        current_distance, current = heapq.heappop(queue)
        if current_distance > distances[current]:
            continue
        for neighbor, data in graph[current].items():
            candidate = current_distance + data.get("weight", 1)
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(queue, (candidate, neighbor))
    return distances

def route_cost(route, matrix):
    return sum(matrix[a][b] for a, b in zip(route, route[1:]))

def expand_route(graph, route):
    """Expande trechos da rota métrica para caminhos reais do grafo."""
    expanded = []
    for origin, destination in zip(route, route[1:]):
        segment = nx.shortest_path(graph, origin, destination, weight="weight")
        if expanded:
            expanded.extend(segment[1:])
        else:
            expanded.extend(segment)
    return expanded

def brute_force(matrix):
    """Testa todas as permutações e retorna o ciclo de menor custo."""
    n, best_route, best_cost = len(matrix), [], float("inf")
    for permutation in itertools.permutations(range(1, n)):
        route = [0, *permutation, 0]
        cost = route_cost(route, matrix)
        if cost < best_cost:
            best_route, best_cost = route, cost
    return best_route, best_cost, [best_route]

def held_karp(matrix):
    """Resolve o TSP com programação dinâmica em subconjuntos (Held-Karp)."""
    n, dp = len(matrix), {}
    for city in range(1, n): dp[(1 << city, city)] = (matrix[0][city], 0)
    for size in range(2, n):
        for subset in itertools.combinations(range(1, n), size):
            mask = sum(1 << city for city in subset)
            for last in subset:
                previous = mask ^ (1 << last)
                dp[(mask, last)] = min((dp[(previous, city)][0] + matrix[city][last], city) for city in subset if city != last)
    full = (1 << n) - 2
    cost, last = min((dp[(full, city)][0] + matrix[city][0], city) for city in range(1, n))
    reversed_route, mask = [last], full
    while mask:
        _, previous = dp[(mask, reversed_route[-1])]
        mask ^= 1 << reversed_route[-1]
        if previous == 0: break
        reversed_route.append(previous)
    route = [0, *reversed(reversed_route), 0]
    return route, cost, [route]

def nearest_neighbor(matrix):
    """Constrói uma rota gulosa escolhendo sempre a cidade não visitada mais próxima."""
    n, route, remaining, steps = len(matrix), [0], set(range(1, len(matrix))), []
    while remaining:
        nxt = min(remaining, key=lambda city: matrix[route[-1]][city])
        route.append(nxt); remaining.remove(nxt); steps.append(route.copy())
    route.append(0); steps.append(route.copy())
    return route, route_cost(route, matrix), steps

def two_opt(matrix):
    """Melhora a rota do vizinho mais próximo invertendo segmentos com ganho."""
    route, _, steps = nearest_neighbor(matrix)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                candidate = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if route_cost(candidate, matrix) < route_cost(route, matrix):
                    route, improved = candidate, True; steps.append(route.copy()); break
            if improved: break
    return route, route_cost(route, matrix), steps

ALGORITHMS = {"Força Bruta": brute_force, "Held-Karp / PD": held_karp, "Vizinho Mais Próximo": nearest_neighbor, "2-opt": two_opt}

def solve(graph, algorithm):
    start = time.perf_counter(); nodes, matrix = shortest_path_metric(graph)
    route, cost, steps = ALGORITHMS[algorithm](matrix)
    # Mantém a animação útil também para algoritmos que retornam apenas a solução final.
    # A animação representa a solução final, e não as tentativas intermediárias
    # do algoritmo (especialmente importante no 2-opt).
    steps = [route[:index + 1] for index in range(1, len(route))]
    named_steps = [[nodes[i] for i in s] for s in steps]
    expanded_steps = [expand_route(graph, step) for step in named_steps]
    return TSPResult([nodes[i] for i in route], cost, expanded_steps, time.perf_counter() - start)
