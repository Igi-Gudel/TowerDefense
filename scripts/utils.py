import numpy as np
from numba import njit, jit
from random import shuffle
from functools import cache
import pygame


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


@njit
def reconstruct_path2(came_from, current):
    total_path = [current]
    while came_from[current][0] != -1:
        current = tuple(came_from[current])
        total_path.append(current)
    return total_path[::-1][1:]


def dict_to_numpy(graph_dict):
    max_x = max(coord[0] for coord in graph_dict.keys())
    max_y = max(coord[1] for coord in graph_dict.keys())

    graph_shape = (max_x + 1, max_y + 1, max_x + 1, max_y + 1)
    graph_array = np.zeros(graph_shape, dtype=np.int64)

    for (x1, y1), neighbors in graph_dict.items():
        for (x2, y2), weight in neighbors.items():
            graph_array[x1, y1, x2, y2] = weight
    return graph_array


def get_path(graph: dict[tuple[int, int]: dict[tuple[int, int]: int]], start: tuple[int, int], goal: tuple[int, int]) -> list:
    return astar2(dict_to_numpy(graph), start, goal)


@njit
def astar2(graph: np.ndarray, start: tuple, goal: tuple):
    graph_shape = graph.shape[0]

    open_set = np.zeros((graph_shape, 2), dtype=np.int64)
    open_set[0] = start
    open_set_length = 1

    came_from = np.zeros((graph_shape, 2), dtype=np.int64)
    came_from[:] = -1

    g_score = np.full(graph_shape, np.inf)
    g_score[start] = 0

    f_score = np.full(graph_shape, np.inf)
    f_score[start] = heuristic(start, goal)

    while open_set_length > 0:
        current_index = np.argmin(f_score[:open_set_length])
        current = tuple(open_set[current_index])
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set[current_index] = open_set[open_set_length - 1]
        open_set_length -= 1

        neighbors = np.argwhere(graph[current[0], current[1]] > 0)
        np.random.shuffle(neighbors)
        for neighbor in neighbors:
            neighbor = tuple(neighbor)
            tentative_g_score = g_score[current] + graph[current[0], current[1], neighbor[0], neighbor[1]]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open_set[:open_set_length]:
                    open_set[open_set_length] = neighbor
                    open_set_length += 1

    return None  # No path found


def astar(graph: dict[tuple[int, int]: dict[tuple[int, int]: int]], start: tuple[int, int], goal: tuple[int, int]) -> None | np.ndarray:
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
