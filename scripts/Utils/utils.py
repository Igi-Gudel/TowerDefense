import pygame
import numpy as np
from numba import njit
from functools import cache


@njit
def get_distance(pos1, pos2) -> float:
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


@cache
def get_pos(tile) -> tuple[int, int]:
    return tile.get_rect().center


@cache
def get_closest_side(pos: tuple[int, int], tile: object) -> tuple[int, int]:
    points = tile.get_points()
    closest: tuple[int, int, float] = ()
    for x, y in points[1:]:
        distance = get_distance((x, y), pos)
        if not closest:
            closest = (x, y, distance)
            continue
        if distance < closest[-1]:
            closest = (x, y, distance)
    return closest[:2], closest[-1]


@cache
def find_closest(path_points: list[tuple[int, int]], point: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    path_points = np.array(path_points)
    point = np.array(point)
    distances = np.linalg.norm(path_points - point, axis=1)
    closest_index = np.argmin(distances)
    closest_point = path_points[closest_index]
    return closest_point[0], closest_point[1]
