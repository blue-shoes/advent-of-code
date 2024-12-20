import dijkstra
import datetime

def main_part1(walls:list[tuple[int, int]], start_pos:tuple[int, int], end_pos:tuple[int, int], shape:tuple[int, int]):
    graph = dijkstra.SquareGrid(shape[0], shape[1])
    graph.walls = walls
    _, time_to = dijkstra.search(graph, start_pos, end_pos)

    cheats:list[tuple[int, int], int] = []
    for key, time in time_to.items():
        for (dir_r, dir_c) in dijkstra.DIRECTIONS.values():
            cheat_coord = (key[0] + 2*dir_r, key[1] + 2*dir_c)
            new_time = time_to.get(cheat_coord, 0)
            if new_time - 2 - time >= 100:
                cheats.append((cheat_coord, (new_time-time-2)))

    print(f'There are {len(cheats)} cheats that save at least 100 picoseconds')

def main_part2(walls:list[tuple[int, int]], start_pos:tuple[int, int], end_pos:tuple[int, int], shape:tuple[int, int]):
    graph = dijkstra.SquareGrid(shape[0], shape[1])
    graph.walls = walls

    _, time_to = dijkstra.search(graph, start_pos, end_pos)

    cheats:list[tuple[int, int], int] = []
    max_cheat_time = 20

    for key, time in time_to.items():
        for dist in range(2,max_cheat_time+1):
            for delta in range(dist+1):
                for (move_r, move_c) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    if delta == 0 and move_r == -1:
                        continue
                    if delta == dist and move_c == -1:
                        continue
                    coord = (key[0] + delta*move_r, key[1] + (dist - delta)*move_c)
                    new_time = time_to.get(coord, 0)
                    if new_time - dist - time >= 100:
                        cheats.append((coord, (new_time-time-dist)))

    print(f'There are {len(cheats)} cheats of 20 or fewer picoseconds that save at least 100 picoseconds')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    walls:list[tuple[int, int]] = []
    for r_idx, row in enumerate(mult_string):
        for c_idx, val in enumerate(row):
            if val == '#':
                walls.append((r_idx, c_idx))
            if val == 'S':
                start_pos = (r_idx, c_idx)
            if val == 'E':
                end_pos = (r_idx, c_idx)

    main_part1(walls, start_pos, end_pos, (len(mult_string), len(mult_string[0])))
    main_part2(walls, start_pos, end_pos, (len(mult_string), len(mult_string[0])))