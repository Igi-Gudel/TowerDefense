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
        self.screen = pygame.display.set_mode((self.WIDTH + self.OUTLINE*2, self.HEIGHT + self.OUTLINE))
        self.display = pygame.Surface(self.SIZE)
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
        self.enemies: list[Enemy] = []
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.mouse[0] = int(min(max(self.mouse[0] + event.rel[0] * min(max(self.data['sensitivity'][0], 0.4), 1.8), self.OUTLINE), self.screen.get_width() - 2*self.OUTLINE) // 1)
                    self.mouse[1] = int(min(max(self.mouse[1] + event.rel[1] * min(max(self.data['sensitivity'][1], 0.4), 1.8), self.OUTLINE), self.screen.get_height() - self.OUTLINE) // 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tile = self.get_tile(*self.mouse, idx=False)
                    if tile.tower is None:
                        tile.tower = "Test"
                    else:
                        tile.tower = None

            for pos in self.tiles:
                self.tiles[pos].render(self.display)

            pygame.draw.circle(self.display, 'white', self.mouse, 4, 2)
            self.screen.blit(self.display, (self.OUTLINE, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    App().run()
