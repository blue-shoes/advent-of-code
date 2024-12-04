
# Directions:
# 1  2  3
# 8  X  4
# 7  6  5

def search_direction(letters:list[list[str]], start_x:int, start_y:int, dir:int, match_len:int, match_str:str) -> (bool, (int, int)):
    match dir:
        case 1:
            next = [(-1, -1), (-2, -2), (-3, -3)]
        case 2:
            next = [(0, -1), (0, -2), (0, -3)]
        case 3:
            next = [(1, -1), (2, -2), (3, -3)]
        case 4:
            next = [(1, 0), (2, 0), (3, 0)]
        case 5:
            next = [(1, 1), (2, 2), (3, 3)]
        case 6:
            next = [(0, 1), (0, 2), (0, 3)]
        case 7:
            next = [(-1, 1), (-2, 2), (-3, 3)]
        case 8:
            next = [(-1, 0), (-2, 0), (-3, 0)]

    max_x = start_x + next[match_len-1][0]
    max_y = start_y + next[match_len-1][1]

    if max_y < 0 or max_x < 0 or max_y >= len(letters) or max_x >= len(letters[start_y]):
        return False, (0, 0)
    

    val = match_str == ''.join([letters[start_y + next[i][1]][start_x + next[i][0]] for i in range(match_len)])

    return val, (start_x + next[match_len-2][0], start_y + next[match_len-2][1])

def main_part1(word_search: list[list[str]]):
    count = 0
    for idx_y, line in enumerate(word_search):
        for idx_x, letter in enumerate(line):
            if letter == 'X':
                count += sum([search_direction(word_search, idx_x, idx_y, dir, 3, 'MAS')[0] for dir in range(1,9)])
    
    print(f"XMAS appears {count} times")

def main_part2(word_search: list[list[str]]):
    
    x_mas_matches = []
    for idx_y, line in enumerate(word_search):
        for idx_x, letter in enumerate(line):
            if letter == 'M':
                x_mas_matches.extend(filter(lambda x: x[0], [search_direction(word_search, idx_x, idx_y, dir, 2, 'AS') for dir in [1, 3, 7, 5]]))

    x_mas_set = set(x_mas_matches)
    count = len(x_mas_matches) - len(x_mas_set)

    print(f"X-MAS appears {count} times")

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    word_search = [list(line.strip()) for line in mult_string]

    main_part1(word_search)
    main_part2(word_search)
    