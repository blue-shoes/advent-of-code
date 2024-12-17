import numpy as np
from numpy import ndarray
import dijkstra

DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

def main_part1_graph(walls:ndarray, start_pos:tuple[int, int], end_pos:tuple[int, int]):
    wall_list:list[dijkstra.GridLocation] = []
    for i_row, row in enumerate(walls):
        for i_col, val in enumerate(row):
            if val:
                wall_list.append(dijkstra.GridLocation((i_row, i_col)))
    
    graph = dijkstra.WeightedGraph(walls.shape[1], walls.shape[0])
    graph.walls = wall_list
    paths = dijkstra.search(graph, start_pos, end_pos)

    print(f'Lowest path score is {paths[end_pos][0][2]}')

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

    with open('../test_output.txt', 'w') as file:
        for i_row in range(walls.shape[0]):
            for i_col in range(walls.shape[1]):
                file.write(path_array[i_row,i_col])

    unique_positions = set(positions)
    print(f'Possible {len(unique_positions)} positions to watch from')

def get_paths(end_pos:tuple[int, int], start_pos:tuple[int, int], paths:dict[dijkstra.Location, list[(dijkstra.Location, tuple[int, int])]], prev_move:tuple[int, int]=(0,0)) -> list[dijkstra.Location]:
    current = end_pos
    best_paths = []
    while current != start_pos:
        prev_locs = paths.get(current)
        if len(prev_locs) > 1:
            for prev_loc in prev_locs:
                if len(prev_loc) == 4 and prev_move != prev_loc[1] and prev_loc[3]:
                    continue
                best_paths.append(prev_loc[0])
                best_paths.extend(get_paths(prev_loc[0], start_pos, paths, prev_loc[1]))
            break
        else:
            best_paths.append(prev_locs[0][0])
            current = prev_locs[0][0]
            prev_move = prev_locs[0][1]
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
    
    main_part1_graph(walls, start_pos, end_pos)