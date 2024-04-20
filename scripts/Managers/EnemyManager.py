import pygame
from scripts.Entities.Enemy import Enemy


class EnemyManager:
    def __init__(self, app, data: dict, imgs: dict):
        self.app = app
        self.enemies: list[Enemy] = []
        self.data = data
        self.imgs = imgs
        self.enemyTypes = {
            "basic": self.data['basic'],
            "speedy": self.data['speedy']
        }
        self.paths = {}
        self.update_path = False

    def add(self, pathID: int, eType: str = "basic") -> None:
        if pathID not in self.paths:
            self.paths[pathID] = self.app.pathManager.get_path(pathID)
        self.enemies.append(Enemy(self.app, self, self.imgs[eType], pathID, self.data[eType]))

    def update_paths(self) -> None:
        self.update_path = True
        for pathID in self.paths:
            self.paths[pathID] = self.app.pathManager.get_path(pathID)

    def render_all(self, surf: pygame.SurfaceType) -> None:
        for enemy in self.enemies:
            enemy.render(surf)

    def update(self) -> None:
        for enemy in self.enemies.copy():
            if self.update_path:
                enemy.update_path()
            if enemy.update():
                self.enemies.remove(enemy)
        if self.update_path:
            self.update_path = False
