import functools
from random import random
import pygame
import sys
import json
from scripts import *
from functools import cache


class App:
    def __init__(self) -> None:
        self.SIZE = self.WIDTH, self.HEIGHT = 1536, 864
        self.FPS = 60

        self.OUTLINE = 5
        self.dt = 0

        self.screen = pygame.display.set_mode((self.WIDTH + self.OUTLINE * 2, self.HEIGHT + self.OUTLINE))
        self.screens = {
            'background': pygame.Surface(self.SIZE),
            'foreground': pygame.Surface(self.SIZE, pygame.SRCALPHA),
            'gui': pygame.Surface(self.SIZE, pygame.SRCALPHA),
        }
        
        self.clock = pygame.time.Clock()
        self.mouse = list(pygame.mouse.get_pos())
        self.__get_data()
        self.__setup()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

    def __get_data(self) -> None:
        with open("data/data.json") as fp:
            data = json.load(fp)
        self.data = data

    def __setup(self) -> None:
        self.images = {}
        self.enemies: list[Enemy] = []

        self.tileManager: TileManager = TileManager(self)
        self.tileManager.add_path((1, 1), (40, 20))

        self.pathing: dict[tuple[int, int], int] = {}
        self.new_graph: bool = False
        self.towers: list[Tower] = []

    def handle_enemies(self):
        for enemy in self.enemies.copy():
            enemy.update_path()
            if enemy.update():
                self.enemies.remove(enemy)
            enemy.render(self.screens['gui'])

    def run(self) -> None:
        while True:
            self.screen.fill('white')
            self.screens['background'].fill('black')
            self.screens['foreground'].fill((0, 0, 0, 0))
            self.screens['gui'].fill((0, 0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.enemies.append(Enemy(self, pygame.Surface((10, 10)), (256, 128), {'speed': 3}))
                if event.type == pygame.MOUSEMOTION:
                    self.mouse[0] = int(min(max(self.mouse[0] + event.rel[0] * min(max(self.data['sensitivity'][0], 0.4), 2.0), self.OUTLINE), self.screen.get_width() - 2 * self.OUTLINE) // 1)
                    self.mouse[1] = int(min(max(self.mouse[1] + event.rel[1] * min(max(self.data['sensitivity'][1], 0.4), 2.0), self.OUTLINE), self.screen.get_height() - self.OUTLINE) // 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tile = self.tileManager.get_tile(*self.mouse, idx=False)
                    tile.tower = not tile.tower

            self.handle_enemies()
            self.tileManager.render_all(self.screens['background'])

            self.screens['background'] = warp(self.screens['background'], tuple(self.mouse), 40)
            pygame.draw.circle(self.screens['gui'], 'white', self.mouse, 5, 3)

            self.screen.blit(self.screens['background'], (self.OUTLINE, 0))
            self.screen.blit(self.screens['foreground'], (self.OUTLINE, 0))
            self.screen.blit(self.screens['gui'], (self.OUTLINE, 0))
            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
            self.dt = self.clock.tick(self.FPS)


if __name__ == '__main__':
    App().run()
