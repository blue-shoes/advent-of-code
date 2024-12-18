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

def search(graph: SquareGrid, start:GridLocation, end:GridLocation) -> tuple[list[int], dict[Location, Optional[Location]]]:
    path = PriorityQueue()
    path.put((0, start))
    came_from: dict[Location, Location] = {}
    came_from[start] = None
    cost_so_far: dict[Location, int] = {}
    cost_so_far[start] = 0

    while not path.empty():
        current:Location = path.get()[1]
        if current == end:
            break

        for next_point in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
                cost_so_far[next_point] = new_cost
                priority = new_cost
                path.put((priority, next_point))
                came_from[next_point] = current
            
    return came_from, cost_so_far
