import pygame
import sys
import json
from scripts import *


class App:
    def __init__(self) -> None:
        self.SIZE = self.WIDTH, self.HEIGHT = 1536, 864
        self.TILES_X, self.TILES_Y = 48, 27
        self.TILE_SIZE = 32
        self.FPS = 60

        self.OUTLINE = 5
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
        self.tiles: dict[tuple[int, int], Tile] = {(x, y): Tile(self, x, y) for x in range(self.TILES_X) for y in range(self.TILES_Y)}
        self.tiles['Start'] = None
        self.tiles['End'] = None
        self.enemies: list[Enemy] = []
        self.pathing: dict[tuple[int, int], int] = {}
        self.towers: list[Tower] = []

    def get_tile(self, x: int, y: int, idx=True) -> Tile:
        if idx:
            return self.tiles[(x, y)]
        try:
            pos = int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)
            return self.tiles[pos]
        except KeyError:
            return self.tiles[(0, 0)]

    def run(self) -> None:
        while True:
            self.screen.fill('white')
            self.display.fill('black')
            self.gui.fill((0, 0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.mouse[0] = int(min(max(self.mouse[0] + event.rel[0] * min(max(self.data['sensitivity'][0], 0.4), 2.0), self.OUTLINE), self.screen.get_width() - 2 * self.OUTLINE) // 1)
                    self.mouse[1] = int(min(max(self.mouse[1] + event.rel[1] * min(max(self.data['sensitivity'][1], 0.4), 2.0), self.OUTLINE), self.screen.get_height() - self.OUTLINE) // 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tile = self.get_tile(*self.mouse, idx=False)
                    new = "Start" if event.button == 1 else "End"
                    if tile.idx in [0, self.TILES_X - 1] or tile.idy in [0, self.TILES_Y - 1]:
                        continue
                    if tile.tower is None:
                        if self.tiles[new] is not None:
                            self.tiles[new].tower = None
                        self.tiles[new] = tile
                        tile.tower = new
                    else:
                        if new == tile.tower:
                            tile.tower = None
                            self.tiles[new] = None
                        else:
                            if self.tiles[new] is not None:
                                self.tiles[new].tower = None
                            self.tiles[new] = tile
                            tile.tower = new

            self.pathing: dict[tuple[int, int], tuple[int, int]] = {}
            point_removal = set()
            for pos in self.tiles:
                if isinstance(pos, tuple):
                    self.tiles[pos].render(self.display)
                    if pos[0] in [0, self.TILES_X - 1] or pos[1] in [0, self.TILES_Y - 1] or self.tiles[pos].tower not in [None, 'Start', 'End']:
                        point_removal.update(self.tiles[pos].get_points())
                    for point in self.tiles[pos].get_points():
                        self.pathing[point] = pos

            for point in self.pathing.copy():
                if point in point_removal:
                    del self.pathing[point]

            graph = {}
            for point in self.pathing:
                graph[point] = {}
                for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    adjacent = point[0] + 16*direction[0], point[1] + 16*direction[1]
                    if adjacent in self.pathing:
                        graph[point][adjacent] = 3 if abs(direction[0]) + abs(direction[1]) == 2 else 2
            try:
                start_pos = self.tiles['Start'].get_rect().center
                end_pos = self.tiles['End'].get_rect().center
                next_points = dijkstra(graph, start_pos, end_pos)
                pygame.draw.lines(self.gui, 'white', 0, next_points)
            except AttributeError:
                pass
            except ValueError:
                pass

            # self.display = warp(self.display, tuple(self.mouse), 40)
            pygame.draw.circle(self.display, 'white', self.mouse, 5, 3)

            self.screen.blit(self.display, (self.OUTLINE, 0))
            self.screen.blit(self.gui, (self.OUTLINE, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    App().run()
