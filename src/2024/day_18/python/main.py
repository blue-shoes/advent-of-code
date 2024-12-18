import re
import dijkstra

def main_part2(coords:list[tuple[int,int]], grid_size:tuple[int,int], fallen_bytes:int):
    graph = dijkstra.SquareGrid(grid_size[0], grid_size[1])

    low = fallen_bytes
    high = len(coords) - 1
    mid = 0
    while(True):
        mid = (high + low) // 2
        graph.walls = coords[:mid]
        came_from, _ = dijkstra.search(graph, (0,0), (grid_size[0]-1, grid_size[1]-1))

        if (grid_size[0]-1, grid_size[1]-1) in came_from:
            low = mid + 1
        else:
            high = mid - 1
        
        if low >= high:
            break
    
    blocker = coords[mid-1]
    print(f'First byte that will block the exit is {blocker[1], blocker[0]}')

def main_part1(coords:list[tuple[int,int]], grid_size:tuple[int,int], fallen_bytes:int):
    graph = dijkstra.SquareGrid(grid_size[0], grid_size[1])
    graph.walls = coords[:fallen_bytes]

    came_from, cost = dijkstra.search(graph, (0,0), (grid_size[0]-1, grid_size[1]-1))

    print(f'Shortest path after {fallen_bytes} bytes fallen: {cost.get((grid_size[0]-1, grid_size[1]-1), None)}')

if __name__ == "__main__":
    regex = '(\\d+),(\\d+)'
    match_regex = re.compile(regex)
    
    with open("../inputs.txt") as file:
        coords = [tuple(map(int,list(match_regex.findall(line.strip())[0])))[::-1] for line in file.readlines()]

    #Test grid
    #grid_size = (7, 7)
    #Full grid
    grid_size = (71, 71)

    #Test grid
    #fallen_bytes = 12
    #Full grid
    fallen_bytes = 1024

    main_part1(coords, grid_size, fallen_bytes)
    main_part2(coords, grid_size, fallen_bytes)