import datetime
import numpy as np
from numpy import ndarray

DIRECTIONS: dict[str: tuple[str, tuple[int, int]]] = \
    {
        '^': ('>', (0, -1), 1),
        '>': ('v', (1, 0), 2),
        'v': ('<', (0, 1), 4),
        '<': ('^', (-1, 0), 8)
    }

def walk_path(starting_map:ndarray, obstacles:ndarray, direction:str, coord:tuple[int, int], add_obst:bool) -> tuple[ndarray, ndarray]:
    visited_map = starting_map.copy()
    obst_added = []
    while(True):
        steps = DIRECTIONS.get(direction)
        if steps[1][0] == 0:
            #column
            try:
                data = obstacles[:, coord[1]]
            except IndexError:
                return visited_map, obst_added, False
            dir_1d = steps[1][1]
            start_1d = coord[0]
            static = coord[1]
        else:
            #row
            try:
                data = obstacles[coord[0], :]
            except IndexError:
                return visited_map, obst_added, False
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
                if mark_visited_map(visited_map, obstacles, start_1d, stop, steps[1][1], static, True, steps, add_obst, obst_added):
                    return visited_map, obst_added, True
                else:
                    return visited_map, obst_added, False
            else:
                if steps[1][0] > 0:
                    stop = obstacles.shape[1]
                if mark_visited_map(visited_map, obstacles, start_1d, stop, steps[1][0], static, False, steps, add_obst, obst_added):
                    return visited_map, obst_added, True
                else:
                    return visited_map, obst_added, False
            break
        if steps[1][0] == 0:
            if mark_visited_map(visited_map, obstacles, start_1d, stop, steps[1][1], static, True, steps, add_obst, obst_added) and not add_obst:
                return visited_map, obst_added, True
            coord = (np.int64(stop-(steps[1][1])), coord[1])
            
        else:
            if mark_visited_map(visited_map, obstacles, start_1d, stop, steps[1][0], static, False, steps, add_obst, obst_added) and not add_obst:
                return visited_map, obst_added, True
            coord = (coord[0], np.int64(stop-(steps[1][0])))

        direction = steps[0]
    return visited_map, obst_added, False

def mark_visited_map(visited_map:ndarray, obstacles:ndarray, start_1d, stop, step, static, col, steps, add_obst, obst_added) -> list[tuple[int]]:
    found_obst = False
    for idx in range(start_1d, stop, step):
        if col:
            if add_obst and (idx, static) not in obst_added and visited_map[idx, static] == 0:
                obs_copy = obstacles.copy()
                obs_copy[idx, static] = '#'
                _, _, loop = walk_path(visited_map, obs_copy, steps[0], (np.int64(idx - step), static), False)
                if loop:
                    obst_added.append((np.int64(idx), static))
                    
                    found_obst = True
            elif not add_obst:
                if visited_map[idx, static] & steps[2]:
                    obst_added.append((np.int64(idx), static))
                    found_obst = True
                    break
                    
            visited_map[idx, static] += steps[2]
        else:
            if add_obst and (static, idx) not in obst_added and visited_map[static, idx] == 0:
                obs_copy = obstacles.copy()
                obs_copy[static, idx] = '#'
                _, _, loop = walk_path(visited_map, obs_copy, steps[0], (static, np.int64(idx-step)), False)
                if loop:
                    obst_added.append((static, np.int64(idx)))
                    found_obst = True
            elif not add_obst:
                if visited_map[static, idx] & steps[2]:
                    obst_added.append((static, np.int64(idx)))
                    found_obst = True
                    break

            visited_map[static, idx] += steps[2]

    return found_obst

def main(obstacles:ndarray, start_coordinate:tuple[int, int], start_dir:str):
    visited_map = np.zeros(shape=obstacles.shape, dtype=int)
    direction = start_dir
    coord = start_coordinate
    
    visited_map, obstacles_added, _ = walk_path(visited_map, obstacles, direction, coord, True)
    obst_count = len(set(list(obstacles_added)))
    if (np.int64(start_coordinate[0]), np.int64(start_coordinate[1])) in list(obstacles_added):
        obst_count -= 1
        
    print(f'Visited {np.count_nonzero(visited_map)} sites')
    print(f'Added {obst_count} obstacles')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    
    site_map = []
    for y_idx, line in enumerate(mult_string):
        points = list(line.strip())
        site_map.append(points)
        for x_idx, point in enumerate(points):
            if point in DIRECTIONS:
                current_dir = point
                start_coordinate = (np.int64(y_idx), np.int64(x_idx))
    
    np_map = np.array(site_map)
    start_t = datetime.datetime.now()
    main(np_map, start_coordinate, current_dir)
    end_t = datetime.datetime.now()
    print(end_t - start_t)

