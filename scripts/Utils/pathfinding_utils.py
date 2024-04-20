import heapq
from functools import cache


def astar(graph, start, goal):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if current_node == goal:
            break

        for next_node, cost in graph[current_node].items():
            new_cost = cost_so_far[current_node] + cost
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current_node

    return reconstruct_path(start, goal, came_from)


def reconstruct_path(start, goal, came_from):
    current_node = goal
    path = []
    while current_node != start:
        path.append(current_node)
        current_node = came_from[current_node]
    path.append(start)
    path.reverse()
    return path


@cache
def heuristic(a: tuple[int, int] | list[int, int], b: tuple[int, int] | list[int, int], accuracy: int = 3) -> float | int:
    # Euclidean distance heuristic
    manhattan = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return ((a[0] - b[0]) ** 8 + (a[1] - b[1]) ** 8) ** 0.125


def pathfind(graph: dict[tuple[int, int]: dict[tuple[int, int]: int]], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    return astar(graph, start, end)
