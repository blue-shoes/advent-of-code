from typing import Protocol, TypeVar, Optional
from queue import PriorityQueue

DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

Location = TypeVar('Location')
GridLocation = tuple[int, int]

class Graph(Protocol):
    def neighbors(self, id: Location) -> list[Location]: pass

class SquareGrid(Graph):
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []
    
    def in_bounds(self, loc_id:GridLocation) -> bool:
        r, c = loc_id
        return 0 <= r < self.height and 0 <= c < self.width
    
    def passable(self, loc_id:GridLocation) -> bool:
        return loc_id not in self.walls
    
    def neighbors(self, loc_id:GridLocation) -> list[GridLocation]:
        r, c = loc_id
        neighbors = [(r+d[0],c+d[1]) for d in DIRECTIONS.values()]
        results = filter(self.in_bounds, neighbors)
        return filter(self.passable, results)

class WeightedGraph(SquareGrid):
    def cost(self, from_node:GridLocation, to_node:GridLocation, previous_dir:tuple[int, int]) -> int:
        new_dir = (to_node[0] - from_node[0], to_node[1] - from_node[1])
        if new_dir == previous_dir:
            return 1
        else:
            return 1001

def search(graph: WeightedGraph, start:GridLocation, end:GridLocation) -> tuple[list[int], dict[Location, Optional[Location]]]:
    path = PriorityQueue()
    path.put((0, start))
    came_from: dict[Location, list[(Location, tuple[int, int]), int]] = {}

    came_from[start] = [(GridLocation((start[0], start[1]-1)), (0, 1), 0)]

    while not path.empty():
        current:Location = path.get()[1]
        if current == end:
            break

        for next_point in graph.neighbors(current):
            new_dir = (next_point[0] - current[0], next_point[1] - current[1])

            for unique_path in came_from[current]:
                prev_dir = unique_path[1]
                
                if new_dir != prev_dir and len(unique_path) == 4 and not unique_path[3]:
                    continue

                inc_cost = graph.cost(current, next_point, prev_dir)
                new_cost = unique_path[2] + inc_cost
                if next_point in came_from:
                    min_path_cost = min([path[2] for path in came_from.get(next_point)])
                else:
                    min_path_cost = 1e9

                if next_point not in came_from or min_path_cost > new_cost:

                    if next_point in came_from and min_path_cost - new_cost == 1000 and not graph.passable((next_point[0] + new_dir[0], next_point[1]+new_dir[1])):
                        came_from[next_point].append((current, new_dir, new_cost))
                    else:
                        priority = new_cost
                        path.put((priority, next_point))
                        came_from[next_point] = [(current, new_dir, new_cost)]
                elif min_path_cost == new_cost or (new_cost - min_path_cost == 1000 and inc_cost == 1):
                    next_next_point = (next_point[0]+new_dir[0], next_point[1]+new_dir[1])
                    if graph.passable(next_next_point) and next_next_point in came_from and min([path[2] for path in came_from.get(next_next_point)]) > new_cost:
                        came_from[next_point].append((current, new_dir,new_cost, True))
                    next_next_point = (next_point[0]+new_dir[1], next_point[1]+new_dir[0])
                    if graph.passable(next_next_point) and next_next_point in came_from and min([path[2] for path in came_from.get(next_next_point)]) > new_cost:
                        came_from[next_point].append((current, new_dir,new_cost, False))
                    next_next_point = (next_point[0]-new_dir[1], next_point[1]-new_dir[0])
                    if graph.passable(next_next_point) and next_next_point in came_from and min([path[2] for path in came_from.get(next_next_point)]) > new_cost:
                        came_from[next_point].append((current, new_dir,new_cost, False))
    return came_from
