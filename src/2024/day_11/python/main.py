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

def recursive_blink(stone:int, blinks:int) -> list[int]:
    for b in range(blinks,0, -1):
        if (stone, b) in calculated_results:
            new_stones = calculated_results[(stone, b)]
            if b == blinks:
                return new_stones
            n_stones = [s for new_stone in new_stones for s in recursive_blink(new_stone, blinks-b)]
            calculated_results[(stone, blinks)] = n_stones
            return n_stones
    
    new_stones = blink(stone)
    calculated_results[(stone, 1)] = new_stones
    
    if blinks == 1:
        return new_stones
    new_stones = [s for new_stone in new_stones for s in recursive_blink(new_stone, blinks-1)]
    calculated_results[stone, blinks] = new_stones
    return new_stones

def blink_with_cache(stones:list[int], number_of_blinks:int) -> list[int]:
    new_stones = []
    for stone in stones:
        new_stones.extend(recursive_blink(stone, number_of_blinks))
    return new_stones


def main(stones:list[int]):
    #print(f'Original Arrangement:\n{stones}')
    number_of_blinks = 25
    s_time = datetime.now()
    new_stones = blink_with_cache(stones, number_of_blinks)
    print(datetime.now() - s_time)

    print(f'Now a total of {len(new_stones)} stones')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        inputs = [int(num) for num in file.readline().strip().split()]

    main(inputs)