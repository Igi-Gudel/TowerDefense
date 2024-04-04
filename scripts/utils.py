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


def astar(graph: dict[tuple[int, int]: dict[tuple[int, int]: int]], start: tuple[int, int], goal: tuple[int, int]):
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


@cache
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


def load_image():
    pass


def load_images():
    pass
