import datetime
import numpy as np
from numpy import ndarray

DIRECTIONS: dict[str: tuple[str, tuple[int, int]]] = \
    {
        '^': ('>', (0, -1)),
        '>': ('v', (1, 0)),
        'v': ('<', (0, 1)),
        '<': ('^', (-1, 0))
    }
def main_part1(obstacles:ndarray, start_coordinate:tuple[int, int], start_dir:str, max_step:int=None) -> ndarray:
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
                mark_visited_map(visited_map, start_1d, stop, steps[1][1], static, True, max_step)
            else:
                if steps[1][0] > 0:
                    stop = obstacles.shape[1]
                mark_visited_map(visited_map, start_1d, stop, steps[1][0], static, False, max_step)
            break
        if steps[1][0] == 0:
            mark_visited_map(visited_map, start_1d, stop, steps[1][1], static, True, max_step)
            coord = (stop-(steps[1][1]), coord[1])
        else:
            mark_visited_map(visited_map, start_1d, stop, steps[1][0], static, False, max_step)
            coord = (coord[0], stop-(steps[1][0]))
        
        direction = steps[0]
        if max_step and np.sum(visited_map) > max_step:
            return visited_map, True
    if not max_step:
        print(f'Visited {np.sum(visited_map)} sites')
    return visited_map, False

def mark_visited_map(visited_map:ndarray, start_1d, stop, step, static, col, max_step):
    for idx in range(start_1d, stop, step):
        if col:
            if max_step:
                visited_map[idx, static] += 1
            else:
                visited_map[idx, static] = 1
        else:
            if max_step:
                visited_map[static, idx] += 1
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
    visited_map, _ = main_part1(np_map, start_coordinate, current_dir)
    #print(visited_map)
    max_spots = visited_map.shape[0]*visited_map.shape[1]
    sum_obs = 0
    s_time = datetime.datetime.now()
    for row_idx in range(visited_map.shape[0]):
        for col_idx in range(visited_map.shape[1]):
            if visited_map[col_idx, row_idx] == 1:
                new_obs = np_map.copy()
                new_obs[col_idx, row_idx] = '#'
                if np_map[col_idx, row_idx] == current_dir:
                    continue
                _, loop = main_part1(new_obs, start_coordinate, current_dir, max_spots)
                if loop:
                    sum_obs += 1
    e_time = datetime.datetime.now()
    print(e_time - s_time)
    print(f'Obstacles that make a loop: {sum_obs}')




