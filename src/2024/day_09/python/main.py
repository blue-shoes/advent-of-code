import numpy as np
from numpy import ndarray

def main_part1(np_array:ndarray, block_array:ndarray):
    current_insert_idx = 0
    current_value_idx = 0
    current_rev_value_idx = len(np_array) - 1
    current_file_id = 0
    current_rev_file_id = int(len(np_array) / 2)
    used_rev_file_blocks = 0
    
    for idx, val in enumerate(np_array):
        if idx % 2 == 0:
            for i in range(val):
                if current_value_idx >= current_rev_value_idx:
                    while block_array[current_insert_idx] != 0:
                        current_insert_idx += 1
                    for j in range(i, val):
                        block_array[current_insert_idx] = current_file_id
                    
                    return
                block_array[current_insert_idx] = current_file_id
                current_insert_idx += 1
            current_file_id += 1
            current_value_idx += 2
            
        else:
            for i in range(val):
                while block_array[current_insert_idx] != 0 and current_rev_value_idx > current_value_idx:
                    if current_value_idx >= current_rev_value_idx:
                        return
                    current_insert_idx += 1
                
                if used_rev_file_blocks == np_array[current_rev_value_idx]:
                    current_rev_file_id -= 1
                    current_rev_value_idx -= 2
                    used_rev_file_blocks = 0
                    if current_rev_value_idx <= current_value_idx:
                        while block_array[current_insert_idx] != 0:
                            current_insert_idx += 1
                            for j in range(used_rev_file_blocks, val):
                                block_array[current_insert_idx] = current_rev_file_id
                        return
                block_array[current_insert_idx] = current_rev_file_id
                current_insert_idx += 1
                used_rev_file_blocks += 1

def main_part2(np_array:ndarray, block_array:ndarray):
    mod_space = {}
    
    for f_idx, f_val in enumerate(np_array):
        idx = len(np_array) - f_idx - 1
        val = np_array[idx]
        if idx % 2 == 0:
            insert = 0
            for idx_front, space_val in enumerate(np_array):
                if idx_front >= idx:
                    for i in range(val):
                        block_array[insert + i] = int(idx/2)
                    break
                if idx_front % 2 == 0:
                    insert += space_val
                    continue
                if val > space_val:
                    insert += space_val
                    continue
                
                if idx_front in mod_space and val > space_val - mod_space[idx_front]:
                    insert += space_val
                    continue
                
                for i in range(val):
                    block_array[insert + mod_space.get(idx_front, 0)] = int(idx / 2)
                    insert += 1
                mod_space[idx_front] = val + mod_space.get(idx_front, 0)
                break

def calc_checksum(block_array:ndarray) -> int:
    sum = 0
    for idx, val in enumerate(block_array):
        sum += idx*val
    return sum

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [int(num) for line in file.readlines() for num in line.strip() ]
    
    np_array = np.array(mult_string)
    block_array = np.zeros(np.sum(np_array))


    main_part1(np_array, block_array)
    cksum = calc_checksum(block_array)            
    print(f'New checksum is {cksum}')

    block_array = np.zeros(np.sum(np_array))
    main_part2(np_array, block_array)
    #print(block_array)
    cksum = calc_checksum(block_array)
    print(f'New checksum is {cksum}')