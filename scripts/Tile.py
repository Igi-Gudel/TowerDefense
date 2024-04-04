import pygame
from scripts.Entity import Entity
from scripts.utils import get_distance


class Tile(Entity):
    def __init__(self, app, idx: int, idy: int):
        super().__init__(app)
        self.idx, self.idy = idx, idy
        self.tower = False

    def __str__(self):
        return f"({self.idx}, {self.idy})"

    def valid(self) -> bool:
        return not (self.idx in [0, self.app.TILES_X - 1] or self.idy in [0, self.app.TILES_Y - 1] or self.tower)

    def render(self, surf: pygame.SurfaceType) -> None:
        width = 0
        if self.idx not in [0, self.app.TILES_X-1] and self.idy not in [0, self.app.TILES_Y-1]:
            width = 1
        if self.tower:
            width = 8
        colour = 4*self.idx, 4*self.idy, 2*(self.app.TILES_X-self.idx+self.app.TILES_Y-self.idy)
        pygame.draw.rect(surf, colour, self.get_rect(), width)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.idx*self.app.TILE_SIZE, self.idy*self.app.TILE_SIZE, self.app.TILE_SIZE, self.app.TILE_SIZE)

    def get_points(self) -> list[tuple[int, int]]:
        rect = self.get_rect()
        return [rect.topleft, rect.midtop, rect.topright, rect.midleft, rect.center, rect.midright, rect.bottomleft, rect.midbottom, rect.bottomright]
