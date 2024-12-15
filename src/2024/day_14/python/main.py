import re
from functools import reduce
from operator import mul, itemgetter
from itertools import groupby

def main_part1(pos:list[tuple[int, int]], vel:list[tuple[int, int]], space:tuple[int, int], time:int):
    quad_count = {'NW':0, 'NE':0, 'SW':0, 'SE': 0}
    mid_r = space[0] // 2
    mid_c = space[1] // 2
    for (pos_r, pos_c), (vel_r, vel_c) in zip(pos, vel):
        f_pos_r = (pos_r + time*vel_r) % space[0]
        f_pos_c = (pos_c + time*vel_c) % space[1]

        if f_pos_r == mid_r or f_pos_c == mid_c:
            continue

        if f_pos_r < mid_r:
            if f_pos_c < mid_c:
                quad_count['NW'] += 1
            else:
                quad_count['NE'] += 1
        else:
            if f_pos_c < mid_c:
                quad_count['SW'] += 1
            else:
                quad_count['SE'] += 1
    
    safety_factor = reduce(mul, quad_count.values())

    print(f'After {time} seconds, the safety factor is {safety_factor}')


def main_part2(pos:list[tuple[int, int]], vel:list[tuple[int, int]], space:tuple[int, int]):
    seconds = 0
    while(True):
        seconds += 1
        r_map = {}
        c_map = {}
        for (pos_r, pos_c), (vel_r, vel_c) in zip(pos, vel):
            pos_r = (pos_r + seconds*vel_r) % space[0]
            pos_c = (pos_c + seconds*vel_c) % space[1]
            if pos_r not in r_map:
                r_map[pos_r] = []
            r_map[pos_r].append(pos_c)
            if pos_c not in c_map:
                c_map[pos_c] = []
            c_map[pos_c].append(pos_r)
        
        i_tree, max_g = is_tree(r_map, c_map, space)
        if i_tree:
            break
        if seconds % 10000 == 0:
            print(f'{seconds} seconds have elapsed, max grouping was {max_g}')

    print(f'There is a Christmas tree after {seconds} seconds')
        
def is_tree(r_map:dict[int, list[int]], c_map:dict[int, list[int]], space:tuple[int, int]) -> tuple[bool, int]:
    
    groups = []

    for rows in c_map.values():
        s_rows = sorted(list(set(rows)))
    
        for k, g in groupby(enumerate(s_rows), lambda ix: ix[0] - ix[1]):
            groups.append(len(list(map(itemgetter(1), g))))

    max_g = max(groups) 
    if max(groups) > 10:
        return True, max_g
    return False, max_g

if __name__ == "__main__":

    pos = []
    vel = []
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    regex = '=(-*\\d+),(-*\\d+) v=(-*\\d+),(-*\\d+)'
    compiled = re.compile(regex)
    for line in mult_string:
        pc, pr, vc, vr = compiled.findall(line)[0]
        pos.append((int(pr), int(pc)))
        vel.append((int(vr), int(vc)))
    
    #Test space
    #space = (7, 11)
    #Actual space
    space = (103, 101)

    time = 100

    main_part1(pos, vel, space, time)
    main_part2(pos, vel, space)
