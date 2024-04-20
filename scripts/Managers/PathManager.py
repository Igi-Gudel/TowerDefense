from scripts.Utils.pathfinding_utils import pathfind


class PathManager:
    def __init__(self, app):
        self.app = app
        self.paths: dict[int: list[tuple[int, int]]] = {}

    def get_path(self, pathID: int) -> list:
        if pathID in self.paths:
            return self.paths[pathID].copy()
        start, end = self.app.tileManager.special_tiles['spawns'][pathID].get_rect().center, self.app.tileManager.special_tiles['targets'][pathID].get_rect().center
        path: list = pathfind(self.make_graph(), start, end)
        self.paths[pathID] = path
        return path.copy()

    def update_paths(self) -> None:
        for pathID in self.paths:
            start, end = self.app.tileManager.special_tiles['spawns'][pathID].get_rect().center, self.app.tileManager.special_tiles['targets'][pathID].get_rect().center
            path: list = pathfind(self.make_graph(), start, end)
            self.paths[pathID] = path

    def __make_points(self) -> dict[tuple[int, int], tuple[int, int]]:
        pathing: dict[tuple[int, int], tuple[int, int]] = {}
        point_removal = set()
        for pos in self.app.tileManager.tiles:
            tile = self.app.tileManager.tiles[pos]
            if not tile.valid():
                point_removal.update(tile.get_points())
            for point in tile.get_points():
                pathing[point] = pos

        for point in pathing.copy():
            if point in point_removal:
                del pathing[point]

        return pathing

    def make_graph(self) -> dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]]:
        pathing = self.__make_points()
        graph = {}
        for point in pathing:
            graph[point] = {}
            for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                adjacent = point[0] + self.app.tileManager.TILE_SIZE // 2 * direction[0], point[1] + self.app.tileManager.TILE_SIZE // 2 * direction[1]
                if adjacent in pathing:
                    weight = 3 if abs(direction[0]) + abs(direction[1]) == 2 else 2
                    graph[point][adjacent] = weight
        return graph
