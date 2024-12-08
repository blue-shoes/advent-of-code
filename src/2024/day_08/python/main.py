import numpy as np

def main(antenna_map: dict[str, tuple[int, int]], map_size:tuple[int, int], res_freq:bool):
    antinode_map = np.zeros(shape=map_size, dtype=int)
    for nodes in antenna_map.values():
        for idx, node in enumerate(nodes):
            if len(nodes) > 1 and res_freq:
                antinode_map[node] = 1
            for a_node in nodes[idx+1:]:
                r_change = node[0] - a_node[0]
                c_change = node[1] - a_node[1]
                test_node = (node[0] + r_change, node[1] + c_change)
                while(True):
                    if test_node[0] >= 0 and test_node[0] < map_size[0] and test_node[1] >= 0 and test_node[1] < map_size[1]:
                        antinode_map[test_node] = 1
                    else:
                        break
                    if not res_freq:
                        break
                    test_node = (test_node[0] + r_change, test_node[1] + c_change)
                
                test_node = (a_node[0] - r_change, a_node[1] - c_change)
                while(True):
                    if test_node[0] >= 0 and test_node[0] < map_size[0] and test_node[1] >= 0 and test_node[1] < map_size[1]:
                        antinode_map[test_node] = 1
                    else:
                        break
                    if not res_freq:
                        break
                    test_node = (test_node[0] - r_change, test_node[1] - c_change)
    
    print(f'There are {np.count_nonzero(antinode_map)} antinodes')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    
    antenna_map = {}
    
    for r_idx, line in enumerate(mult_string):
        for c_idx, node in enumerate(list(line.strip())):
            if r_idx == 0 and c_idx == 0:
                map_size = (len(mult_string), len(line.strip()))
            if node == '.':
                continue
            if node not in antenna_map:
                antenna_map[node] = []
            antenna_map[node].append((r_idx, c_idx))
    
    main(antenna_map, map_size, False)    
    main(antenna_map, map_size, True)    
