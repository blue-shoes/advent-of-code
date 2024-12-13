import numpy as np
from numpy import ndarray

def in_plot(point:tuple[int, int], shape:tuple[int, int]) -> bool:
    return 0 <= point[0] < shape[0] and 0 <= point[1] < shape[1]

def get_inner_corners(mask:tuple[int, int], point:tuple[int, int], garden_map:ndarray, crop:str, orig_move:tuple[int, int]) -> int:
    inner_corners = 0
    for adj in [-1, 1]:
        new_point = (point[0] + adj*mask[0], point[1] + adj*mask[1])
        if in_plot(new_point, garden_map.shape):
            if garden_map[new_point] == crop:
                #print('test 1')
                test_point = (new_point[0] + (-1 * orig_move[0]), new_point[1] + (-1 * orig_move[1]))
                if garden_map[test_point] == crop:
                    inner_corners += 1
    return inner_corners

def get_contiguous_plots(garden_map:ndarray, point:tuple[int, int], crop:str, points:list[tuple[int, int]]) -> tuple[list[tuple[int, int]], int, int, bool]:
    r, c = point
    new_points = []
    perim = 0
    corners = 0
    tmp_corners = 0
    non_crops = 0
    edge_moves = set()
    inner_corners = 0
    if garden_map[point] == crop:
        is_edge = False
        if point in points:
            return [], 0, 0, False
        points.append(point)
        
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_point = (r + move[0], c + move[1])
            if in_plot(new_point, garden_map.shape):
                if new_point in points:
                    continue
                added_points, added_perim, added_corners, edge = get_contiguous_plots(garden_map, new_point, crop, points)
                if edge:
                    edge_moves.add(move)
                    if move[0] == 0:
                        inner_corners += get_inner_corners((1, 0), new_point, garden_map, crop, move)
                points.extend(added_points)
                perim += added_perim
                corners += added_corners
            else:
                perim += 1
                tmp_corners += 1
                non_crops += 1
                edge_moves.add(move)
    else:
        perim += 1
        tmp_corners += 1
        non_crops += 1
        is_edge = True
    
    if edge_moves == set([(1, 0), (-1, 0)]) or edge_moves == set([(0, 1), (0, -1)]):
        tmp_corners = 0
    elif len(edge_moves) == 4:
        tmp_corners = 4
    else:
        tmp_corners = max(len(edge_moves) - 1, 0)
    
    corners += tmp_corners + inner_corners

    return new_points, perim, corners, is_edge

def main_part1(garden_map:ndarray):
    fence_cost = 0
    discount = 0
    visited = []
    for r, row in enumerate(garden_map):
        for c, crop in enumerate(row):
            if (r, c) in visited:
                continue
            plot_points = []
            point = (r, c)
            plot_points.append(point)
            perim = 2
            corners = 1
            for move in [(1, 0), (0, 1)]:
                new_point = (r + move[0], c + move[1])
                if in_plot(new_point, garden_map.shape):
                    points, added_perim, added_corners, edge = get_contiguous_plots(garden_map, new_point, crop, plot_points)
                    plot_points.extend(points)
                    perim += added_perim
                    if edge:
                        if move[0] == 0:
                            corners += get_inner_corners((1, 0), new_point, garden_map, crop, move)
                        corners += 1
                    corners += added_corners
                else:
                    perim += 1
                    corners += 1
            if corners % 2 == 1:
                #Hack because we're sometimes off by one corner for reasons I can't determine
                corners += 1
            fence_cost += perim * len(plot_points)
            discount += corners * len(plot_points)
            visited.extend(plot_points)

    print(f'Total fence cost is {fence_cost}')
    print(f'Discount fence cost is {discount}')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [list(line.strip()) for line in file.readlines()]
    
    garden_map = np.array(mult_string)

    main_part1(garden_map)