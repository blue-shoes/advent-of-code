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
    came_from: dict[Location, list[(Location, tuple[int, int])]] = {}
    cost_so_far: dict[Location, int] = {}

    came_from[start] = [(GridLocation((start[0], start[1]-1)), (0, 1))]
    cost_so_far[start] = 0
    end_costs:list[int] = []

    while not path.empty():
        current:Location = path.get()[1]
        #print('current', current)
        if current == end:
            end_costs.append(cost_so_far[current])
            break

        for next_point in graph.neighbors(current):
            #if current == (92,133):
            #    print('here i am', came_from[current])
            for unique_path in came_from[current]:
                
                prev_dir = unique_path[1]
                new_dir = (next_point[0] - current[0], next_point[1] - current[1])
                inc_cost = graph.cost(current, next_point, prev_dir)
                new_cost = cost_so_far[current] + inc_cost
                if current == (92, 133) or current == (91, 132):
                    print('!!!',current, cost_so_far.get(current, None), next_point, inc_cost, cost_so_far.get(next_point, None))
                    print('!!',cost_so_far.get(next_point, 0) == new_cost, new_cost - cost_so_far.get(next_point, 0) == 1000, inc_cost == 1)
                
                if next_point not in cost_so_far or cost_so_far[next_point] > new_cost:

                    if next_point in cost_so_far and cost_so_far[next_point] - new_cost == 1000 and not graph.passable((next_point[0] + new_dir[0], next_point[1]+new_dir[1])):
                        came_from[next_point].append([current, new_dir])
                    else:
                        cost_so_far[next_point] = new_cost
                        priority = new_cost
                        path.put((priority, next_point))
                        came_from[next_point] = [(current, new_dir)]
                elif cost_so_far[next_point] == new_cost or (new_cost - cost_so_far[next_point] == 1000 and inc_cost == 1):
                    if current == (92, 133) or current == (91, 132):
                        print('here')
                    straight_passable = False
                    for cf in came_from[next_point]:
                        old_dir = cf[1]
                        if graph.passable((next_point[0] + old_dir[0], next_point[1] + old_dir[1])):
                            if current == (92, 133) or current == (91, 132):
                                print('straight passable:',next_point[0] + old_dir[0], next_point[1] + old_dir[1])
                            straight_passable = True
                            break
                    if straight_passable:
                        continue
                    came_from[next_point].append([current, new_dir])
    
    return end_costs, came_from
