import numpy as np
from numba import njit, jit, typed
from functools import lru_cache
import pygame


def dijkstra(graph: typed.Dict[tuple[int, int], typed.Dict[tuple[int, int], tuple[int, int]]],
             start: tuple[int, int],
             end: tuple[int, int]) -> list[tuple[int, int]]:
    previous_node: typed.Dict = {}
    distances: typed.Dict = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        min_distance_node = min(priority_queue, key=lambda x: x[0])
        current_distance, current_node = min_distance_node
        priority_queue.remove(min_distance_node)

        if current_node == end:
            path = []
            while current_node != start:
                path.append(current_node)
                current_node = previous_node[current_node]
            path.append(start)
            return path[::-1]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                priority_queue.append((distance, neighbor))
                previous_node[neighbor] = current_node
    return None


if __name__ == '__main__':
    graph = {
        'A': {'B': 1, 'C': 4, 'D': 1},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }

    start_node = 'A'
    end_node = 'D'
    previous_node = {}  # To store previous nodes for backtracking
    print(dijkstra(graph, start_node, end_node))


@lru_cache
def warp(surface: pygame.SurfaceType, position: tuple[int], radius: int) -> pygame.Surface:
    surf_array = np.array(pygame.surfarray.array3d(surface))
    array = warp_surface(surf_array, *surface.get_size(), *position, radius=radius)
    return pygame.surfarray.make_surface(array)


@njit
def warp_surface(surface: np.array, width: int, height: int, px: int, py: int, radius: int) -> np.array:
    warped_surface = surface.copy()
    for y in range(radius // 2, height - radius // 2):
        for x in range(radius // 2, width - radius // 2):
            warp_amount = max(0.5 * (radius - ((x - px) ** 2 + (y - py) ** 2) ** 0.5) / radius, 0.02)
            warped_surface[x, y] = surface[int(x + (px - x) * warp_amount), int(y + (py - y) * warp_amount)]
    return warped_surface
