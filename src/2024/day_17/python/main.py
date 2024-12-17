import re
from enum import Enum
from functools import lru_cache

def adv(operand:int):
    global register_a
    register_a = register_a // (2**get_combo_operand(operand))

def bxl(operand:int):
    global register_b
    register_b = register_b ^ operand

def bst(operand:int):
    global register_b
    register_b = get_combo_operand(operand) % 8   

def jnz(operand:int):
    global register_a, i_pointer
    if register_a == 0:
        return
    i_pointer = operand - 2

def bxc(operand:int):
    global register_b, register_c
    register_b = register_b ^ register_c

def out(operand:int):
    global output
    output.append(get_combo_operand(operand) % 8)

def bdv(operand:int):
    global register_a, register_b
    register_b = register_a // (2**get_combo_operand(operand))

def cdv(operand:int):
    global register_a, register_c
    register_c = register_a // (2**get_combo_operand(operand))

class OpCode(Enum):

    ADV = (0, adv)
    BXL = (1, bxl)
    BST = (2, bst)
    JNZ = (3, jnz)
    BXC = (4, bxc)
    OUT = (5, out)
    BDV = (6, bdv)
    CDV = (7, cdv)

    def __call__(self, *args, **kwargs):
        self.value[1](*args, **kwargs)
    
    @staticmethod
    @lru_cache()
    def get_enum(int_id:int):
        return {val.value[0]:val for val in OpCode}[int_id]

register_a = 0
register_b = 0
register_c = 0
i_pointer = 0 
output = []

def get_combo_operand(operand:int) -> int:
    global register_a, register_b, register_c, i_pointer
    if operand == 7:
        print(i_pointer, register_a, register_b, register_c, operand)
        raise Exception('Found unexpected operand 7')
    if operand == 6:
        return register_c
    if operand == 5:
        return register_b
    if operand == 4:
        return register_a
    return operand

def main_part1(mult_string:list[str]):
    global register_a, register_b, register_c, i_pointer
    regex = '(\\d+)'
    compiled = re.compile(regex)
    register_a = int(compiled.findall(mult_string[0])[0])
    register_b = int(compiled.findall(mult_string[1])[0])
    register_c = int(compiled.findall(mult_string[2])[0])

    instructions = [int(i) for i in compiled.findall(mult_string[-1])]

    while i_pointer < len(instructions):
        operand = instructions[i_pointer+1]
        OpCode.get_enum(instructions[i_pointer])(operand)
        i_pointer += 2

    print(','.join([str(i) for i in output]))

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    main_part1(mult_string)
