Key = tuple[int, int, int, int, int]
Lock = tuple[int, int, int, int, int]

def key_fits(lock:Lock, key:Key) -> bool:
    for i in range(5):
        if lock[i] + key[i] > 5:
            return False
    return True

def main_part1(locks:list[Lock], keys:list[Key]):
    valid_combos = 0
    for lock in locks:
        for key in keys:
            if key_fits(lock, key):
                valid_combos += 1
    
    print(f'There are {valid_combos} valid lock/key combos')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [line.strip() for line in file.readlines()]
    
    keys:list[Key] = []
    locks:list[Lock] = []
    for idx in range(0,len(mult_string),8):
        line_1 = mult_string[idx]
        
        counts = [0, 0, 0, 0, 0]
        for i in range(1,6):
            col_line = mult_string[idx + i]
            for c in range(5):
                if col_line[c] == '#':
                    counts[c] += 1
        if line_1 == '#####':
            locks.append(Lock(tuple(counts)))
        else:
            keys.append(Key(tuple(counts)))
    
    main_part1(locks, keys)