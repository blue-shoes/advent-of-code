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

def get_pattern(code:str, bot_num:int) -> str:
    start_pos = 'A'
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
    if bot_num < 3:
        #print(move_str)
        return get_pattern(move_str, bot_num+1)
    return move_str

def test():
    p1 = '<^A'
    print(f'{p1}, {len(get_pattern(p1, 2))}')
    p2 = '^<A'
    print(f'{p2}, {len(get_pattern(p2, 2))}')
    p3 = '<vA'
    print(f'{p3}, {len(get_pattern(p3, 2))}')
    p4 = 'v<A'
    print(f'{p4}, {len(get_pattern(p4, 2))}')
    p5 = '>^A'
    print(f'{p5}, {len(get_pattern(p5, 2))}')
    p6 = '^>A'
    print(f'{p6}, {len(get_pattern(p6, 2))}')
    p7 = '>vA'
    print(f'{p7}, {len(get_pattern(p7, 2))}')
    p8 = 'v>A'
    print(f'{p8}, {len(get_pattern(p8, 2))}')

def main_part1(codes:list[str]):
    c_sum = 0
    for code in codes:
        val = int(code[:-1])
        #if val != 179:
        #    continue
        move = get_pattern(code, 1)
        #print(move)
        print(len(move))
        c_sum += len(move) * val
    
    print(f'The Complexity sum is {c_sum}')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]

    main_part1(mult_string)
    #test()

    