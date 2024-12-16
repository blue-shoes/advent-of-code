import numpy as np
from numpy import ndarray
from functools import reduce

DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def can_move(walls:ndarray, boxes:ndarray, start_pos:tuple[int, int], move:tuple[int, int]) -> bool:
    new_pos = (start_pos[0] + move[0], start_pos[1] + move[1])
    if walls[new_pos]:
        return False
    if boxes[new_pos]:
        if can_move(walls, boxes, new_pos, move):
            boxes[new_pos[0] + move[0], new_pos[1] + move[1]] = True
            boxes[new_pos] = False
            return True
        else:
            return False
    return True

def main_part1(orig_walls:ndarray, orig_boxes:ndarray, init_pos:tuple[int, int], directions:list[tuple[int, int]]):
    robot_pos = init_pos
    walls = np.copy(orig_walls)
    boxes = np.copy(orig_boxes)
    for move in directions:
        if can_move(walls, boxes, robot_pos, move):
            robot_pos = (robot_pos[0] + move[0], robot_pos[1] + move[1])

    gps_val = np.sum(gps_function(boxes))
    print(gps_val)

    print_step(walls, boxes, robot_pos)

def print_step(walls:ndarray, boxes:ndarray, robot_pos:tuple[int, int], file=None):
    results = np.empty(boxes.shape, dtype = str)
    for i_row, row in enumerate(boxes):
        for i_col, val in enumerate(row):
            point = (i_row, i_col)
            if walls[point]:
                results[point] = '#'
            elif boxes[point]:
                results[point] = 'O'
            elif robot_pos == point:
                results[point] = '@'
            else:
                results[point] = '.'
    
    if file:
        np.savetxt(file, results, fmt='%s')
    else:
        print(results)

def gps_function(boxes:ndarray) -> int:
    gps_sum = 0
    for i_row, row in enumerate(boxes):
        for i_col, val in enumerate(row):
            if val:
                gps_sum += i_row * 100 + i_col
    
    return gps_sum

def populate_double_wide(orig_walls:ndarray, orig_boxes:ndarray) -> tuple[ndarray, ndarray]:
    double_wide = (orig_walls.shape[0], orig_walls.shape[1]*2)
    walls = np.zeros(double_wide, int)
    boxes = np.zeros(double_wide, int)

    for i_row, row in enumerate(orig_walls):
        for i_col, val in enumerate(orig_walls):
            point = (i_row, i_col)
            if orig_walls[point]:
                walls[i_row, i_col*2] = -1
                walls[i_row, i_col*2 + 1] = 1
            if orig_boxes[point]:
                boxes[i_row, i_col*2] = -1
                boxes[i_row, i_col*2 + 1] = 1
    
    return walls, boxes

def can_move_wide(walls:ndarray, boxes:ndarray, start_pos:tuple[int, int], move:tuple[int, int], first_move:bool=False) -> tuple[bool, list[tuple[int, int]]]:
    if first_move or move[1] == -1:
        new_pos = (start_pos[0] + move[0], start_pos[1] + move[1])
    else:
        new_pos = (start_pos[0] + move[0], start_pos[1] + move[1]*2)
    if walls[new_pos]:
        return False, list()
    if boxes[new_pos]:
        if move[1] == 0:
            #row movement
            if boxes[new_pos] == 1:
                #right side of box
                check_pos = (new_pos[0], new_pos[1]-1)
            else:
                check_pos = new_pos
            
            l_movable, l_moves = can_move_wide(walls, boxes, check_pos, move)
            if not l_movable:
                return False, list()
            r_movable, r_moves = can_move_wide(walls, boxes, (check_pos[0], check_pos[1]+1), move)
            if not r_movable:
                return False, list()
            
            movables = l_moves
            movables.extend(r_moves)
            movables.extend([check_pos, (check_pos[0], check_pos[1]+1)])
            return True, movables
        else:
            #column movement
            if move[1] == -1 and first_move:
                new_pos = (new_pos[0], new_pos[1]-1)
            movable, moves = can_move_wide(walls, boxes, new_pos, move)
            if not movable:
                return False, list()
            if move[1] == -1:
                moves.append(new_pos)
                moves.append((new_pos[0], new_pos[1]+1))
            else:
                moves.append((new_pos[0], new_pos[1]+1))
                moves.append(new_pos)
            return True, moves
            
    return True, list()

def main_part2(orig_walls:ndarray, orig_boxes:ndarray, init_pos:tuple[int, int], directions:list[tuple[int, int]]):
    walls, boxes = populate_double_wide(orig_walls, orig_boxes)
    robot_pos = (init_pos[0], init_pos[1]*2)
    count = 0 
    for move in directions:
        count += 1
        movable, boxes_to_move = can_move_wide(walls, boxes, robot_pos, move, True)
        if movable:
            robot_pos = (robot_pos[0] + move[0], robot_pos[1] + move[1])
            moved = []
            for box in boxes_to_move:
                if box in moved:
                    continue
                boxes[box[0] + move[0], box[1] + move[1]] = boxes[box]
                boxes[box] = 0
                moved.append(box)

    gps_val = np.sum(gps_function_wide(boxes))
    print(gps_val)

    print_step(walls, boxes, robot_pos)

def gps_function_wide(boxes:ndarray) -> int:
    gps_sum = 0
    for i_row, row in enumerate(boxes):
        for i_col, val in enumerate(row):
            if val == -1:
                gps_sum += i_row * 100 + i_col
    
    return gps_sum

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [list(line.strip()) for line in file.readlines()]
    
    for idx, line in enumerate(mult_string):
        if not line:
            break
    map_shape = (idx, len(list(mult_string[0])))
    walls = np.zeros(map_shape, bool)
    boxes = np.zeros(map_shape, bool)
    robot_pos = ()
    directions = []
    now_directions = False
    
    for row, line in enumerate(mult_string):
        if not line:
            now_directions = True
            continue
        if now_directions:
            directions.extend([DIRECTIONS[s] for s in list(line)])
        else:
            for col, val in enumerate(list(line)):
                if val == 'O':
                    boxes[row, col] = True
                elif val == '#':
                    walls[row, col] = True
                elif val == '@':
                    robot_pos = (row, col)
                
    main_part1(walls, boxes, robot_pos, directions)
    main_part2(walls, boxes, robot_pos, directions)