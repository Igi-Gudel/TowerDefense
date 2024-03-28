import pygame
from scripts.Entity import Entity


class Enemy(Entity):
    def __init__(self, app, img: pygame.SurfaceType, pos: pygame.Vector2):
        super().__init__(app)
        self.pos = pygame.Vector2(pos)
        self.img = img

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.img.get_size())
