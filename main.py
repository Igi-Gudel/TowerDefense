import pygame
import sys
from scripts import *


class App:
    def __init__(self) -> None:
        self.SIZE = self.WIDTH, self.HEIGHT = 1536, 864
        self.TILES_X, self.TILES_Y = 48, 27
        self.TILE_SIZE = 32
        self.FPS = 60

        self.OUTLINE = 5
        self.screen = pygame.display.set_mode((self.WIDTH + self.OUTLINE*2, self.HEIGHT + self.OUTLINE*2))
        self.display = pygame.Surface(self.SIZE)
        self.clock = pygame.time.Clock()

        self.__setup()

    def __setup(self) -> None:
        self.tiles: dict[tuple[int, int], Tile] = {(x, y): Tile(self, x, y)}
        self.enemies: list[Enemy] = []

    def run(self) -> None:
        while True:
            self.screen.fill('white')
            self.display.fill((111, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.display, (self.OUTLINE, self.OUTLINE))
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    App().run()
