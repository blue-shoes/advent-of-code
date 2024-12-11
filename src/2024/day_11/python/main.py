from datetime import datetime

calculated_results:dict[tuple[int, int], list[int]] = {}

def blink(stone:int) -> list[int]:
    new_order = list()
    if stone == 0:
        new_order.append(1)
    elif len(str_val := str(stone)) % 2 == 0:
        idx = len(str_val) // 2
        new_order.extend([int(str_val[:idx]), int(str_val[idx:])])
    else:
        new_order.append(stone * 2024)
    return new_order

def blink_count(stones:list[int], number_of_blinks:int):
    stone_map = {}
    for stone in stones:
        if stone not in stone_map:
            stone_map[stone] = 0
        stone_map[stone] += 1
    for _ in range(number_of_blinks):
        new_map = {}
        for key, count in stone_map.items():
            new_stones = blink(key)
            for stone in new_stones:
                if stone not in new_map:
                    new_map[stone] = 0
                new_map[stone] += count
        stone_map = new_map
    
    print(f'There are {sum(stone_map.values())} stones now')

def main(stones:list[int]):
    number_of_blinks = 75

    s_time = datetime.now()
    blink_count(stones, number_of_blinks)
    print(datetime.now() - s_time)

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        inputs = [int(num) for num in file.readline().strip().split()]

    main(inputs)