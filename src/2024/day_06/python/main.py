import numpy as np
from numpy import ndarray

DIRECTIONS: dict[str: tuple[str, tuple[int, int]]] = \
    {
        '^': ('>', (0, -1)),
        '>': ('v', (1, 0)),
        'v': ('<', (0, 1)),
        '<': ('^', (-1, 0))
    }
def main_part1(obstacles:ndarray, start_coordinate:tuple[int, int], start_dir:str):
    visited_map = np.zeros(shape=obstacles.shape)
    direction = start_dir
    coord = start_coordinate
    while(True):
        steps = DIRECTIONS.get(direction)
        if steps[1][0] == 0:
            #column
            data = obstacles[:, coord[1]]
            dir_1d = steps[1][1]
            start_1d = coord[0]
            static = coord[1]
        else:
            #row
            data = obstacles[coord[0], :]
            dir_1d = steps[1][0]
            start_1d = coord[1]
            static = coord[0]
        data_obs = np.where(data == '#')[0]
        if dir_1d < 0:
            data_obs = data_obs[::-1]
        stop = -1
        for obs in data_obs:
            if dir_1d < 0 and obs < start_1d:
                stop = obs
                break
            if dir_1d > 0 and obs > start_1d:
                stop = obs
                break
        if stop == -1:
            #exited
            if steps[1][0] == 0:
                #column
                if steps[1][1] > 0:
                    stop = obstacles.shape[0]
                mark_visited_map(visited_map, start_1d, stop, steps[1][1], static, True)
            else:
                if steps[1][0] > 0:
                    stop = obstacles.shape[1]
                mark_visited_map(visited_map, start_1d, stop, steps[1][0], static, False)
            break
        if steps[1][0] == 0:
            mark_visited_map(visited_map, start_1d, stop, steps[1][1], static, True)
            coord = (stop-(steps[1][1]), coord[1])
        else:
            mark_visited_map(visited_map, start_1d, stop, steps[1][0], static, False)
            coord = (coord[0], stop-(steps[1][0]))
        
        direction = steps[0]
    print(f'Visited {np.sum(visited_map)} sites')

def mark_visited_map(visited_map:ndarray, start_1d, stop, step, static, col):
    for idx in range(start_1d, stop, step):
        if col:
            visited_map[idx, static] = 1
        else:
            visited_map[static, idx] = 1

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    
    #obstacles = ()
    site_map = []
    for y_idx, line in enumerate(mult_string):
        points = list(line.strip())
        site_map.append(points)
        for x_idx, point in enumerate(points):
            if point in DIRECTIONS:
                current_dir = point
                start_coordinate = (y_idx, x_idx)
    
    np_map = np.array(site_map)
    main_part1(np_map, start_coordinate, current_dir)

