import pygame
from scripts.Tile import Tile
from scripts.pathfinding_utils import astar


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
        if idx:
            return self.tiles[(x, y)]
        pos = int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)
        return self.tiles[pos]

    def __add_spawn(self, pos, idx=True) -> None:
        tile = self.get_tile(*pos, idx=idx)
        self.special_tiles['spawns'].append(tile)

    def __add_target(self, pos, idx=True) -> None:
        tile = self.get_tile(*pos, idx=idx)
        self.special_tiles['targets'].append(tile)

    def add_path(self, start, end, idx=True) -> None:
        self.__add_spawn(start, idx=idx)
        self.__add_target(end, idx=idx)

    def get_path(self, pathID: int) -> list:
        if pathID in self.paths:
            return self.paths[pathID]
        start, end = self.special_tiles['spawns'][pathID].get_rect().center, self.special_tiles['targets'][pathID].get_rect().center
        path = astar(self.make_graph(), start, end)
        self.paths[pathID] = path
        return path

    def get_target(self):
        return self.special_tiles['targets'][0]

    def make_pathing(self) -> dict[tuple[int, int], tuple[int, int]]:
        pathing: dict[tuple[int, int], tuple[int, int]] = {}
        point_removal = set()
        for pos in self.tiles:
            tile = self.tiles[pos]
            if not tile.valid():
                point_removal.update(tile.get_points())
            for point in tile.get_points():
                pathing[point] = pos

        for point in pathing.copy():
            if point in point_removal:
                del pathing[point]

        return pathing

    def make_graph(self) -> dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]]:
        graph = {}
        pathing = self.make_pathing()
        for point in pathing:
            graph[point] = {}
            for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                adjacent = point[0] + self.TILE_SIZE//2 * direction[0], point[1] + self.TILE_SIZE//2 * direction[1]
                if adjacent in pathing:
                    weight = 3 if abs(direction[0]) + abs(direction[1]) == 2 else 2
                    graph[point][adjacent] = weight
        return graph
