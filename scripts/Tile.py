import pygame
from scripts.Entity import Entity


class Tile(Entity):
    def __init__(self, app, idx: int, idy: int):
        super().__init__(app)
        self.idx, self.idy = idx, idy
        self.tower = False

    def __str__(self):
        return f"({self.idx}, {self.idy})"

    def get_closest_side(self, pos: tuple[int, int]) -> tuple[int, int]:
        points = self.get_points()
        closest = ()
        for x, y in points[1:]:
            distance = (pos[0]-x)**2 + (pos[1]-y)**2
            if not closest:
                closest = (x, y, distance)
                continue
            if distance <= closest[-1]:
                closest = (x, y, distance)
        return closest[:2], closest[-1]**0.5

    def render(self, surf: pygame.SurfaceType) -> None:
        width = 0
        if self.idx not in [0, self.app.TILES_X-1] and self.idy not in [0, self.app.TILES_Y-1]:
            width = 1
        if self.tower:
            width = 8
        colour = 5*self.idx, 5*self.idy, 2.5*(self.app.TILES_X-self.idx+self.app.TILES_Y-self.idy)
        pygame.draw.rect(surf, colour, self.get_rect(), width)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.idx*self.app.TILE_SIZE, self.idy*self.app.TILE_SIZE, self.app.TILE_SIZE, self.app.TILE_SIZE)

    def get_points(self) -> list[tuple[int, int]]:
        rect = self.get_rect()
        return [rect.topleft, rect.midtop, rect.topright, rect.midleft, rect.center, rect.midright, rect.bottomleft, rect.midbottom, rect.bottomright]
