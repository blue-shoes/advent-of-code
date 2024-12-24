def main_part1(network_map:dict[str, list[str]]):
    link_count = 0
    for comp, linked in network_map.items():
        if not comp.startswith('t'):
            continue
        for idx, link in enumerate(linked):
            for link2 in network_map[link]:
                if link2 in linked[idx+1:]:
                    link_count += 1 / len(list(filter(lambda s: s.startswith('t'), [comp, link, link2])))
                    #print(comp, link, link2)
    
    print(f'There are {int(link_count)} linked networks with "t"')

def recursive_network(newtork_map:dict[str, list[str]], ordered_keys:list[str],  network:list[str], possible_conn:list[str], start_idx:int) -> list[str]:
    max_depth = 0
    max_network = network
    for key in possible_conn:
        if ordered_keys.index(key) < start_idx:
            continue
        new_network = network.copy()
        new_network.append(key)
        if len(new_network) > max_depth:
            max_depth = len(new_network)
            max_network = new_network
        child_keys = sorted(list(set(possible_conn) & set(network_map[key])))
        if not child_keys:
            continue
        new_network = recursive_network(network_map, ordered_keys, new_network, child_keys, ordered_keys.index(key)+1)
        if len(new_network) > max_depth:
            max_depth = len(new_network)
            max_network = new_network

    return max_network

def main_part2(network_map:dict[str, list[str]]):
    ordered_keys = list(sorted(network_map.keys()))
    max_network_len = 0
    for idx, key in enumerate(ordered_keys):
        for idx2, key2 in enumerate(ordered_keys[idx+1:]):
            if key not in network_map[key2]:
                continue
            child_keys = sorted(list(set(network_map[key]) & set(network_map[key2])))
            network = recursive_network(network_map, ordered_keys, [key, key2], child_keys, (idx+idx2+1))
            if len(network) > max_network_len:
                max_network_len = len(network)
                max_network = network
    
    print(','.join(max_network))

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    network_map = {}
    for line in mult_string:
        comps = line.split('-')
        if comps[0] not in network_map:
            network_map[comps[0]] = []
        network_map[comps[0]].append(comps[1])
        if comps[1] not in network_map:
            network_map[comps[1]] = []
        network_map[comps[1]].append(comps[0])
    
    main_part1(network_map)
    main_part2(network_map)