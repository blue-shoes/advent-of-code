from functools import cache

impossible_patterns:list[str] = []

def main_part2(towels:list[str], patterns:list[str]):
    result = 0
    for pattern in patterns:
        result += part2_test(pattern, frozenset(towels))
    print(f'There are {result} unique design combinations')

def towel_is_possible(pattern:str, towel:str, t_heirarchy:dict[str, list[str]], towels:list[str]) -> bool:
    children = t_heirarchy.get(towel, [])
    if pattern == towel or pattern in children:
        return True
    if pattern.startswith(towel):
        if is_possible(pattern[len(towel):], towels, t_heirarchy):
            return True
        for child in children:
            if pattern.startswith(child):
                if is_possible(pattern[len(child):], towels, t_heirarchy):
                    return True    
    return False

def is_possible(pattern:str, towels:list[str], t_heirarchy:dict[str, list[str]]) -> bool:
    global impossible_patterns
    if pattern in impossible_patterns:
        return False
    possible = [t for t in towels if t in pattern]
    for towel in possible:
        if towel_is_possible(pattern, towel, t_heirarchy, towels):
            return True
    impossible_patterns.append(pattern)
    return False

def main_part1(t_heirarchy:dict[str, list[str]], towels:list[str], patterns:list[str]):
    possible_designs = list(filter(lambda p: is_possible(p, towels, t_heirarchy), patterns))

    print(f'There are {len(possible_designs)} possible designs')

def add_downstream(downstream:dict[str,list[str]], parent:str, child:str):
    if parent not in downstream:
        downstream[parent] = []
    downstream[parent].append(child)

@cache
def part2_test(pattern, towels) -> int:
    if pattern == '':
        return 1
    result = 0
    for towel in towels:
        if pattern.startswith(towel):
            result += part2_test(pattern[len(towel):], towels)
    return result


if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    towels = mult_string[0].split(', ')
    patterns = mult_string[2:]

    downstream = {}
    for idx, towel_1 in enumerate(towels):
        for towel_2 in towels[idx+1:]:
            #if towel_2 in towel_1:
            #    add_downstream(downstream, towel_2, towel_1)
            #elif towel_1 in towel_2:
            #    add_downstream(downstream, towel_1, towel_2)
            if towel_1.startswith(towel_2):
                add_downstream(downstream, towel_2, towel_1)
            elif towel_2.startswith(towel_1):
                add_downstream(downstream, towel_1, towel_2)
    
    sorted_downstream = {}
    for key,val in downstream.items():
        sorted_downstream[key] = sorted(val, key=lambda v: len(v))

    never_parent = [t for t in towels if t not in downstream.keys()]
    all_children = list(set([t for lt in downstream.values() for t in lt]))

    not_in_downstream = [t for t in never_parent if t not in all_children]

    main_part1(downstream, towels, patterns)
    main_part2(towels, patterns)
