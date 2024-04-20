import pygame
from .Entity import Entity
from scripts.Utils.utils import get_distance, find_closest, get_closest_side


class Enemy(Entity):
    def __init__(self, app, name: str, pathID: int, *, uncertainty=6):
        super().__init__(app)
        self.name = name
        self.img = app.enemyManager.imgs[self.name]
        self.data = app.enemyManager.data[self.name]
        self.pathID = pathID
        self.pos = pygame.Vector2(self.app.tileManager.get_start(pathID=self.pathID))
        self.last_movement = pygame.Vector2(0)
        self.UNCERTAINTY = uncertainty

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.img.get_size())

    def render(self, surf: pygame.SurfaceType) -> None:
        surf.blit(self.img, self.get_rect())


class Enemy(Entity):
    def __init__(self, app, eManager, img: pygame.SurfaceType, pathID: int, data: dict[str: int | float], uncertainty=8):
        super().__init__(app)
        self.UNCERTAINTY = uncertainty
        self.manager = eManager
        self.pathID = pathID
        self.pos = pygame.Vector2(self.app.tileManager.get_start(pathID=self.pathID))
        self.path = self.manager.paths[self.pathID].copy()
        self.last_movement = pygame.Vector2(0)
        self.img = img
        self.data = data
        self.off_path = False
        self.next_target = self.path[0]
        self.next_index = 1

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.img.get_size())

    def render(self, surf: pygame.SurfaceType) -> None:
        surf.blit(self.img, self.get_rect())

    def update(self) -> bool:
        center = self.get_rect().center

        if self.off_path:
            point = find_closest(tuple(self.path), center)
            if get_distance(center, point) <= self.UNCERTAINTY:
                self.off_path = False
            self.last_movement = pygame.Vector2(self.off_path.pop(0)) - pygame.Vector2(center)
        else:
            if get_distance(center, self.next_target) <= self.UNCERTAINTY:
                if len(self.path) - 1 <= self.next_index:
                    return True
                self.next_index += 1
                self.next_target = self.path[self.next_index]
            self.last_movement = pygame.Vector2(self.next_target) - pygame.Vector2(center)
        self.__move(self.last_movement)
        return False

    def update_path(self) -> None:
        self.path: list[tuple[int, int]] = self.manager.paths[self.pathID].copy()
        point = find_closest(tuple(self.path), self.get_rect().center)
        self.next_index = self.path.index(point) - 1
        self.next_target = point
        # end = self.app.tileManager.get_tile(*point, idx=False)
        # self.off_path = astar(self.app.tileManager.make_graph(), get_closest_side(tuple(self.pos), start), get_closest_side(point, end))

    def set_center(self, new_pos: tuple[int, int]) -> None:
        self.pos = (new_pos[0]-self.img.get_width()//2, new_pos[1] - self.img.get_height()//2)

    def __move(self, direction: pygame.Vector2) -> None:
        if direction != pygame.Vector2(0, 0):
            direction.normalize_ip()
        vel = direction * self.data['speed'] * self.app.FPS // self.app.dt
        self.pos.x += vel.x
        if self.app.tileManager.collide_with(self.get_rect().center):
            self.pos.x -= vel.x

        self.pos.y += vel.y
        if self.app.tileManager.collide_with(self.get_rect().center):
            self.pos.y -= vel.y
