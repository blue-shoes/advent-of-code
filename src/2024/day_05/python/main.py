import functools

def map_page_dep(rules: list[tuple[int]]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    page_deps = {}
    rev_page_deps = {}
    for rule in rules:
        if rule[1] not in page_deps:
            page_deps[rule[1]] = []
        page_deps[rule[1]].append(rule[0])
        if rule[0] not in rev_page_deps:
            rev_page_deps[rule[0]] = []
        rev_page_deps[rule[0]].append(rule[1])
    return page_deps, rev_page_deps

def update_is_valid(page_deps: dict[int, list[int]], update:list[int]) -> bool:
    for idx, page in enumerate(update):
        for p_idx in range(idx, len(update)):
            if page not in page_deps:
                continue
            if update[p_idx] in page_deps[page]:
                return False
    return True   

def reorder_update(page_deps:dict[int, list[int]], rev_page_deps:dict[int, list[int]], update:list[int]) -> list[int]:
    return sorted(update, key=functools.cmp_to_key(lambda v1, v2: map_sort_order(page_deps, rev_page_deps, v1, v2)))

def map_sort_order(page_deps:dict[int, list[int]], rev_page_deps:dict[int, list[int]], v1:int, v2:int) -> int:
    if v2 in page_deps and v1 in page_deps[v2]:
        return -1
    if v2 in rev_page_deps and v1 in rev_page_deps[v2]:
        return 1
    return 0

def main_part2(page_deps: dict[int, list[int]], rev_page_deps: dict[int, list[int]], updates:list[list[int]]):
    sum = 0
    
    for u_idx, update in enumerate(updates):
        if not update_is_valid(page_deps, update):
            reordered = reorder_update(page_deps, rev_page_deps, update)
            sum += reordered[int(len(reordered)/2)]
    
    print(f'Sum of middle pages of reordered updates is {sum}')

def main_part1(page_deps: dict[int, list[int]], updates:list[list[int]]):
    sum = 0
    invalid = []
    for u_idx, update in enumerate(updates):
        if update_is_valid(page_deps, update):
            sum += update[int(len(update)/2)]
        else:
            invalid.append(u_idx)
    print(f'Sum of middle pages of correct updates is {sum}')


if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    
    rules = []
    updates = []
    writing_updates = False
    for line in mult_string:
        s_line = line.strip()
        if writing_updates:
            updates.append([int(u) for u in s_line.split(",")])
        elif s_line == '':
            writing_updates = True
        else:
            rules.append(tuple([int(u) for u in s_line.split("|")]))
    
    page_deps, rev_page_deps = map_page_dep(rules)
    main_part1(page_deps, updates)
    main_part2(page_deps, rev_page_deps, updates)