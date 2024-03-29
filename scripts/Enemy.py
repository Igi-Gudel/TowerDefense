import pygame
from scripts.Entity import Entity


class Enemy(Entity):
    def __init__(self, app, img: pygame.SurfaceType, pos: pygame.Vector2 | list[int, int] | tuple[int, int]):
        super().__init__(app)
        self.pos = pygame.Vector2(pos)
        self.img = img

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.img.get_size())

    def update(self) -> None:
        self.__move()

    def __move(self) -> None:
        pass
