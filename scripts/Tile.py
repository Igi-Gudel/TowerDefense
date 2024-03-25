import pygame
from scripts.Entity import Entity


class Tile(Entity):
    def __init__(self, app, idx: int, idy: int):
        super().__init__(app)
        self.idx, self.idy = idx, idy
        self.tower = None

    def get_points(self):
        pass

    def render(self, surf: pygame.SurfaceType):
        pygame.draw.rect(surf, (2*self.idx, 2*self.idy, self.app.TILES_X-self.idx+self.app.TILES_Y-self.idy), self.get_rect(), 1)

    def get_rect(self):
        return pygame.Rect(self.idx*self.app.TILE_SIZE, self.idy*self.app.TILE_SIZE, self.app.TILE_SIZE, self.app.TILE_SIZE)
