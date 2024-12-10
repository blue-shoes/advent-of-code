import numpy as np
from numpy import ndarray

def in_map(point:tuple[int, int], size:tuple[int, int]) -> bool:
    if point[0] < 0 or point[0] >= size[0]:
        return False
    if point[1] < 0 or point[1] >= size[1]:
        return False
    return True

def get_valid_steps(height:int, point:tuple[int, int], hiking_map:ndarray) -> list[tuple[int, int]]:
    valid_moves = []
    for move in [(1, 0), (0,1), (-1, 0), (0, -1)]:
        move_point = (point[0] + move[0], point[1] + move[1])
        if in_map(move_point, hiking_map.shape):
            if hiking_map[move_point] - height == 1:
                valid_moves.append(move_point)
    return valid_moves

def walk_path(c_point:tuple[int, int], path_dict:dict[tuple[int, int], list[tuple[int, int]]], peaks:list[tuple[int, int]]) -> list[tuple[int, int]]:
    if c_point in peaks:
        return list([c_point])
    walked_peaks = []
    for next_point in path_dict.get(c_point, []):
        walked_peaks.extend(walk_path(next_point, path_dict, peaks))
    
    return walked_peaks

def main(inputs:list[list[int]]):
    trail_heads = []
    peaks = []
    path_dict = {}

    hiking_map = np.array(inputs)
    for (r, c), height in np.ndenumerate(hiking_map):
        if height == 0:
            trail_heads.append((r,c))
        if height == 9:
            peaks.append((r,c))
        path_dict[(r, c)] = get_valid_steps(height, (r, c), hiking_map)

    trailhead_scores = []
    trailhead_ratings = []
    
    for s_point in trail_heads:
        trail_head_peaks = walk_path(s_point, path_dict, peaks)
        
        trailhead_scores.append(len(set(trail_head_peaks)))
        trailhead_ratings.append(len(trail_head_peaks))

    print(f'The trailhead score sum is {sum(trailhead_scores)}')
    print(f'The trailhead rating sum is {sum(trailhead_ratings)}')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        inputs = [[int(num) for num in line.strip()] for line in file.readlines()]
    
    main(inputs)
    