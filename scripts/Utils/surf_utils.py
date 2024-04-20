import numpy as np
import pygame
import os
from numba import njit
from functools import cache


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


def load_image(path: os.PathLike, colourKey: tuple[int, int, int] = (0, 0, 0), new_size: tuple[int, int] = None) -> pygame.Surface:
    if new_size is None:
        img = pygame.image.load(name).convert_alpha()
    else:
        img = pygame.transform.scale(pygame.image.load(name).convert_alpha(), new_size)
    img.set_colorkey(colourKey)
    return img


def load_images(path: os.PathLike, colourKey: tuple[int, int, int] = (0, 0, 0), size: tuple[int, int] = (24, 24)) -> tuple[pygame.Surface]:
    return tuple(get_image(path + "/" + name, colourKey, size) for name in os.listdir(path))
