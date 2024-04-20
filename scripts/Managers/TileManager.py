import pygame
from scripts.Entities.Tile import Tile


class TileManager:
    def __init__(self, app) -> None:
        self.app = app
        self.TILES_X, self.TILES_Y = 48, 27
        self.TILE_SIZE = 32

        self.tiles: dict[tuple[int, int], Tile] = {(x, y): Tile(self, x, y) for x in range(self.TILES_X) for y in range(self.TILES_Y)}
        self.special_tiles: dict[str, list[Tile]] = {
            "spawns": [],
            "targets": []
        }
        self.paths: dict[int: list] = {}

    def __str__(self):
        return f"{[tile for tile in self.tiles]}"

    def render_all(self, surf: pygame.SurfaceType) -> None:
        for pos in self.tiles:
            self.tiles[pos].render(surf)

    def get_tile(self, x: int, y: int, idx=True) -> Tile:
        try:
            if idx:
                return self.tiles[(x, y)]
            pos = int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)
            return self.tiles[pos]
        except KeyError:
            return None

    def __add_spawn(self, pos, idx=True) -> None:
        tile = self.get_tile(*pos, idx=idx)
        self.special_tiles['spawns'].append(tile)

    def __add_target(self, pos, idx=True) -> None:
        tile = self.get_tile(*pos, idx=idx)
        self.special_tiles['targets'].append(tile)

    def add_path(self, start: tuple[int, int], end: tuple[int, int], idx=True) -> None:
        self.__add_spawn(start, idx=idx)
        self.__add_target(end, idx=idx)

    def get_target(self, *, pathID: int = -1) -> tuple[int, int]:
        return self.special_tiles['targets'][pathID].get_rect().center

    def get_start(self, *, pathID: int = -1) -> tuple[int, int]:
        return self.special_tiles['spawns'][pathID].get_rect().center

    def collide_with(self, pos: tuple[int, int]) -> bool:
        tile = self.get_tile(*pos, idx=False)
        return tile.tower
