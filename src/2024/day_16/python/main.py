import numpy as np
from numpy import ndarray
import dijkstra

DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

def get_open_points(walls:ndarray, pos:tuple[int, int], visited:list[tuple[int, int]], current_points:int, orig_d:str) -> list[tuple[tuple[int, int]]]:
    open_points = []
    for d, move in DIRECTIONS.items():
        next_point = (pos[0] + move[0], pos[1] + move[1])
        if walls[next_point]:
            continue
        if next_point in visited:
            continue
        open_points.append((d, next_point, visited, current_points, orig_d))
    return open_points

def main_part1(walls:ndarray, start_pos:tuple[int, int], end_pos:tuple[int, int]):
    init_dir = 'E'
    visited = []
    visited.append(start_pos)
    d = init_dir
    pos = start_pos
    open_points = get_open_points(walls, pos, visited, 0, d)
    highest_score = 1e9
    path = []
    while open_points:
        next_open_points = []
        #print(open_points)
        for next_d, next_point, next_visited, current_points, orig_d in open_points:
            if next_d == orig_d:
                point = current_points + 1
            else:
                point = current_points + 1001
            if point > highest_score:
                continue
            if next_point == end_pos:
                highest_score = point
                print(f'found end, score = {point}')
                continue
            next_visited.append(next_point)
            next_open_points.extend(get_open_points(walls, next_point, next_visited, point, next_d))
        open_points = next_open_points
    
    print(f'The lowest maze score is {highest_score}')
    #print(path)

def main_part1_graph(walls:ndarray, start_pos:tuple[int, int], end_pos:tuple[int, int]):
    wall_list:list[dijkstra.GridLocation] = []
    for i_row, row in enumerate(walls):
        for i_col, val in enumerate(row):
            if val:
                wall_list.append(dijkstra.GridLocation((i_row, i_col)))
    
    graph = dijkstra.WeightedGraph(walls.shape[1], walls.shape[0])
    graph.walls = wall_list
    costs, paths = dijkstra.search(graph, start_pos, end_pos)

    print(min(costs))

    positions = get_paths(end_pos, start_pos, paths)
    positions.append(end_pos)

    path_array = np.empty(walls.shape, dtype=str)
    for i_row in range(walls.shape[0]):
        for i_col in range(walls.shape[1]):
            path_array[(i_row, i_col)] = '.'
            if walls[i_row, i_col]:
                path_array[(i_row, i_col)] = '|'
    for val in positions:
        path_array[val] = 'X'
    #print(positions)
    with open('../test_output.txt', 'w') as file:
        #file.write(','.join([f'({p[0]},{p[1]})' for p in positions]))
        for i_row in range(walls.shape[0]):
            for i_col in range(walls.shape[1]):
                file.write(path_array[i_row,i_col])
            file.write('\n')

    #print(positions)
    unique_positions = set(positions)
    #print(len(positions) - len(unique_positions))
    print(len(unique_positions))

def get_paths(end_pos:tuple[int, int], start_pos:tuple[int, int], paths:dict[dijkstra.Location, list[(dijkstra.Location, tuple[int, int])]]) -> list[dijkstra.Location]:
    current = end_pos
    best_paths = []
    while current != start_pos:
        prev_locs = paths.get(current)
        if len(prev_locs) > 1:
            for prev_loc in prev_locs:
                best_paths.append(prev_loc[0])
                best_paths.extend(get_paths(prev_loc[0], start_pos, paths))
            break
        else:
            best_paths.append(prev_locs[0][0])
            current = prev_locs[0][0]
    return best_paths

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [list(line.strip()) for line in file.readlines()]
    
    walls = np.zeros((len(mult_string), len(mult_string[0])))
    for i_row, row in enumerate(mult_string):
        for i_col, val in enumerate(list(row)):
            if val == '#':
                walls[i_row, i_col] = True
            if val == 'S':
                start_pos = (i_row, i_col)
            if val == 'E':
                end_pos = (i_row, i_col)
    
    #main_part1(walls, start_pos, end_pos)
    main_part1_graph(walls, start_pos, end_pos)