from enum import Enum
from functools import cache

class Button(Enum):
    NINE = ('9', (0, 2))
    EIGHT = ('8', (0, 1))
    SEVEN = ('7', (0, 0))
    SIX = ('6', (1, 2))
    FIVE = ('5', (1, 1))
    FOUR = ('4', (1, 0))
    THREE = ('3', (2, 2))
    TWO = ('2', (2, 1))
    ONE = ('1', (2, 0))
    ZERO = ('0', (3, 1))
    A = ('A', (3, 2))
    UP = ('^', (3, 1))
    DOWN = ('v', (4, 1))
    LEFT = ('<', (4, 0))
    RIGHT = ('>', (4, 2))

    @staticmethod
    @cache
    def get_enum(s_val:str):
        return {val.value[0]:val for val in Button}[s_val]

def get_move(start:str, end:str) -> tuple[int, int]:
    start_coord = Button.get_enum(start).value[1]
    end_coord = Button.get_enum(end).value[1]
    return end_coord[0] - start_coord[0], end_coord[1] - start_coord[1]

def get_pattern(code:str, bot_num:int, start_pos:str = 'A') -> str:
    move_str = ''
    for s in list(code):
        move = get_move(start_pos, s)
        #print(start_pos, s, move)
        #print(move)
        if (bot_num > 1):
            #if lower row, down first, if upper row, over first
            if move[0] > 0:
                for r in range(abs(move[0])):
                    move_str += 'v'
                for c in range(abs(move[1])):
                    if move[1] < 0:
                        move_str += '<'
                    else:
                        move_str += '>'
            else:
                for c in range(abs(move[1])):
                    if move[1] < 0:
                        move_str += '<'
                    else:
                        move_str += '>'
                for r in range(abs(move[0])):
                    move_str += '^'
        else:
            start_enum_coord = Button.get_enum(start_pos).value[1]
            end_enum_coord = Button.get_enum(s).value[1]
            #if down, over first, if not, vert first
            #print(start_enum_coord, end_enum_coord)
            if (end_enum_coord[0] == 3 and start_enum_coord[1] == 0):
                for c in range(abs(move[1])):
                    if move[1] < 0:
                        move_str += '<'
                    else:
                        move_str += '>'
                for r in range(abs(move[0])):
                    if move[0] < 0:
                        move_str += '^'
                    else:
                        move_str += 'v'
            elif start_enum_coord[0] == 3 and end_enum_coord[1] == 0:
                for r in range(abs(move[0])):
                    if move[0] < 0:
                        move_str += '^'
                    else:
                        move_str += 'v'
                for c in range(abs(move[1])):
                    if move[1] < 0:
                        move_str += '<'
                    else:
                        move_str += '>'
            else:
                if move[1] < 0:
                    for c in range(abs(move[1])):
                        if move[1] < 0:
                            move_str += '<'
                        else:
                            move_str += '>'
                    for r in range(abs(move[0])):
                        if move[0] < 0:
                            move_str += '^'
                        else:
                            move_str += 'v'
                else:
                    for r in range(abs(move[0])):
                        if move[0] < 0:
                            move_str += '^'
                        else:
                            move_str += 'v'
                    for c in range(abs(move[1])):
                        if move[1] < 0:
                            move_str += '<'
                        else:
                            move_str += '>'

        move_str += 'A'
        start_pos = s
    if bot_num < 3 and bot_num != -1:
        return get_pattern(move_str, bot_num+1)
    return move_str

def map_moves() -> dict[tuple[Button, Button], str]:
    possible_moves = [
        (Button.A.value[0], Button.LEFT.value[0]),
        (Button.A.value[0], Button.RIGHT.value[0]),
        (Button.A.value[0], Button.UP.value[0]),
        (Button.A.value[0], Button.DOWN.value[0]),
        (Button.A.value[0], Button.A.value[0]),
        (Button.LEFT.value[0], Button.LEFT.value[0]),
        (Button.LEFT.value[0], Button.UP.value[0]),
        (Button.LEFT.value[0], Button.DOWN.value[0]),
        (Button.LEFT.value[0], Button.A.value[0]),
        (Button.UP.value[0], Button.LEFT.value[0]),
        (Button.UP.value[0], Button.RIGHT.value[0]),
        (Button.UP.value[0], Button.UP.value[0]),
        (Button.UP.value[0], Button.A.value[0]),
        (Button.DOWN.value[0], Button.LEFT.value[0]),
        (Button.DOWN.value[0], Button.RIGHT.value[0]),
        (Button.DOWN.value[0], Button.DOWN.value[0]),
        (Button.DOWN.value[0], Button.A.value[0]),
        (Button.RIGHT.value[0], Button.RIGHT.value[0]),
        (Button.RIGHT.value[0], Button.UP.value[0]),
        (Button.RIGHT.value[0], Button.DOWN.value[0]),
        (Button.RIGHT.value[0], Button.A.value[0])
    ]
    move_map = {}
    for move in possible_moves:
        move_map[''.join(move)] = get_pattern(move[1], -1, move[0])
    
    return move_map

def main_part2(codes:list[str], robots:int):
    move_map = map_moves()
    c_sum = 0
    for code in codes:
        val = int(code[:-1])
        init_pattern = 'A' + get_pattern(code, -1)
        pattern_count = {key:0 for key in move_map.keys()}
        for idx in range(len(init_pattern)-1):
            pattern_count[init_pattern[idx:idx+2]] += 1
        for _ in range(robots):
            tmp_count = {key:0 for key in pattern_count.keys()}

            for move_pair, num in pattern_count.items():
                if num == 0:
                    continue
                new_pattern = 'A' + move_map.get(move_pair)
                for idx in range(len(new_pattern)-1):
                    tmp_count[new_pattern[idx:idx+2]] += num
            pattern_count = tmp_count
        
        c_sum += sum([v for v in pattern_count.values()])*val
    
    print(f'The Complexity sum is {c_sum}')


def main_part1(codes:list[str]):
    c_sum = 0
    for code in codes:
        val = int(code[:-1])
        move = get_pattern(code, 1)
        c_sum += len(move) * val
    
    print(f'The Complexity sum is {c_sum}')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]

    main_part1(mult_string)
    main_part2(mult_string, 25)