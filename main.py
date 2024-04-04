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
        self.TILES_X, self.TILES_Y = 48, 27
        self.TILE_SIZE = 32
        self.FPS = 60

        self.OUTLINE = 5
        self.dt = 0
        self.screen = pygame.display.set_mode((self.WIDTH + self.OUTLINE * 2, self.HEIGHT + self.OUTLINE))
        self.display = pygame.Surface(self.SIZE)
        self.gui = pygame.Surface(self.SIZE, pygame.SRCALPHA)
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
        self.images = {

        }

        self.tiles: dict[tuple[int, int], Tile] = {(x, y): Tile(self, x, y) for x in range(self.TILES_X) for y in range(self.TILES_Y)}
        self.tiles['Start'] = None
        self.tiles['End'] = None
        self.enemies: list[Enemy] = []
        self.pathing: dict[tuple[int, int], int] = {}
        self.new_graph: bool = False
        self.towers: list[Tower] = []

    @cache
    def get_tile(self, x: int, y: int, idx=True) -> Tile:
        if idx:
            return self.tiles[(x, y)]
        try:
            pos = int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)
            return self.tiles[pos]
        except KeyError:
            return self.tiles[(0, 0)]

    def get_next_pos(self, start: tuple, end: tuple, tiles=self.tiles) -> list[tuple] | None:
        try:
            next_points = astar(self.graph, start, end)
            return next_points
        except KeyError:
            return None
        except TypeError:
            return None

    def get_target(self) -> Tile:
        if (tile := self.tiles["End"]) is not None:
            return tile
        else:
            return self.tiles[(1, 1)]

    def make_pathing(self) -> None:
        self.pathing: dict[tuple[int, int], tuple[int, int]] = {}
        point_removal = set()
        for pos in self.tiles:
            if isinstance(pos, tuple):
                (tile := self.tiles[pos]).render(self.display)
                if pos[0] in [0, self.TILES_X - 1] or pos[1] in [0, self.TILES_Y - 1] or tile.tower:
                    point_removal.update(tile.get_points())
                for point in tile.get_points():
                    self.pathing[point] = pos

        for point in self.pathing.copy():
            if point in point_removal:
                # pygame.draw.circle(self.gui, 'red', point, 2)
                del self.pathing[point]
            else:
                pass
                # pygame.draw.circle(self.gui, 'white', point, 2)

    def make_graph(self) -> dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]]:
        self.graph = {}
        for point in self.pathing:
            self.graph[point] = {}
            for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                adjacent = point[0] + 16 * direction[0], point[1] + 16 * direction[1]
                if adjacent in self.pathing:
                    weight = 3 if abs(direction[0]) + abs(direction[1]) == 2 else 2
                    self.graph[point][adjacent] = weight
        return self.graph

    def run(self) -> None:
        while True:
            self.screen.fill('white')
            self.display.fill('black')
            self.gui.fill((0, 0, 0, 0))

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
                    self.new_graph = False
                    tile = self.get_tile(*self.mouse, idx=False)
                    tile.tower = not tile.tower

            self.make_pathing()
            self.make_graph()
            for enemy in self.enemies.copy():
                if enemy.update():
                    self.enemies.remove(enemy)
                enemy.render(self.gui)

            # self.display = warp(self.display, tuple(self.mouse), 40)
            pygame.draw.circle(self.display, 'white', self.mouse, 5, 3)

            self.screen.blit(self.display, (self.OUTLINE, 0))
            self.screen.blit(self.gui, (self.OUTLINE, 0))
            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.3f}")
            self.dt = self.clock.tick(self.FPS)


if __name__ == '__main__':
    App().run()
