import numpy as np
from numba import njit
from functools import lru_cache
import pygame


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
