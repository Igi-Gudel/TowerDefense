import numpy as np
from numba import njit
from random import shuffle
from functools import cache


@cache
@njit
def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def reconstruct_path(came_from: dict, current: int) -> list:
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1][1:]


def astar(graph: dict[tuple[int, int]: dict[tuple[int, int]: int]], start: tuple[int, int], goal: tuple[int, int]) -> None | list:
    open_set = {start}
    came_from = {}
    g_score = {point: float('inf') for point in graph}
    g_score[start] = 0
    f_score = {point: float('inf') for point in graph}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        neighbors = list(graph[current].keys())
        shuffle(neighbors)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + graph[current][neighbor]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None  # No path found
