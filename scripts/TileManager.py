import pygame
from scripts.Tile import Tile


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

    def render_all(self, surf: pygame.SurfaceType) -> None:
        for pos in self.tiles:
            self.tiles[pos].render(surf)

    def get_tile(self, x: int, y: int, idx=True) -> Tile:
        if idx:
            return self.tiles[(x, y)]
        pos = int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)
        return self.tiles[pos]

    def add_spawn(self, pos, idx=True) -> None:
        tile = self.get_tile(*pos, idx=idx)
        self.special_tiles['spawns'].append(tile)

    def add_target(self, pos, idx=True) -> None:
        tile = self.get_tile(*pos, idx=idx)
        self.special_tiles['targets'].append(tile)

    def add_path(self, start, end, idx=True) -> None:
        self.add_spawn(start, idx=idx)
        self.add_target(end, idx=idx)

    def get_path(self, pathID: int):
        pathTiles = self.special_tiles['spawns'][pathID], self.special_tiles['targets'][pathID]
