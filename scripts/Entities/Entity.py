import pygame


class Entity:
    def __init__(self, app) -> None:
        self.app = app

    def update(self) -> None:
        pass

    def render(self, surf: pygame.SurfaceType) -> None:
        pass

    def get_rect(self) -> pygame.Rect:
        pass
