import pygame
from random import random
from scripts.Entity import Entity


class Enemy(Entity):
    def __init__(self, app, img: pygame.SurfaceType, pos: pygame.Vector2 | list[int, int] | tuple[int, int], data: dict[str: int | float]):
        super().__init__(app)
        self.pos = pygame.Vector2(pos)
        self.last_movement = pygame.Vector2(0)
        self.img = img
        self.data = data
        self.directions = []

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.img.get_size())

    def render(self, surf: pygame.SurfaceType) -> None:
        pygame.draw.rect(surf, 'white', self.get_rect())

    def update_path(self):
        start, end, _ = self.get_self_target_distance()
        self.directions = self.app.get_next_pos(start, end)

    def get_self_target_distance(self) -> tuple[tuple[int, int], tuple[int, int], float]:
        start, distance = self.app.get_tile(*self.pos, idx=False).get_closest_side(self.pos)
        end = self.app.get_target().get_rect().center
        return start, end, distance

    def update(self) -> bool:
        start, end, distance = self.get_self_target_distance()
        if start == end and distance <= 8:
            self.set_center(end)
            return True
        else:
            if self.directions and self.directions is not None:
                self.last_movement = pygame.Vector2(self.directions[0]) - pygame.Vector2(self.get_rect().center)
            self.__move(self.last_movement)
        return False

    def set_center(self, new_pos: tuple[int, int]) -> None:
        self.pos = (new_pos[0]-self.img.get_width()//2, new_pos[1] - self.img.get_height()//2)

    def __move(self, direction: pygame.Vector2) -> None:
        try:
            direction.normalize_ip()
        except ValueError:
            pass
        self.pos += direction * self.data['speed'] * self.app.FPS // self.app.dt
        self.pos.x = self.pos.x
        self.pos.y = self.pos.y
