import collections

def mix(secret:int, given:int) -> int:
    return secret ^ given

def prune(secret:int) -> int:
    return secret % 16777216

def step1(previous:int) -> int:
    return prune(mix(previous, previous*64))

def step2(previous:int) -> int:
    return prune(mix(previous, previous // 32))

def step3(previous:int) -> int:
    return prune(mix(previous, previous * 2048))

def new_secret(val:int) -> int:
    val = step1(val)
    val = step2(val)
    return step3(val)

def main_part1(start_nums:list[int]):
    sum = 0
    for num in start_nums:
        val = num
        for i in range(2000):
            val = new_secret(val)
        sum += val
    
    print(f'Secret sum = {sum}')

def main_part2(start_nums:list[int]):
    sell_map = {}
    all_change_sets = set()
    for monkey, num in enumerate(start_nums):
        val = num
        change_queue = collections.deque([], 4)
        monkey_map = {}
        sell_map[monkey] = monkey_map
        for i in range(2000):
            new_sec = new_secret(val)
            change = (new_sec % 10) - (val % 10)
            change_queue.append(change)
            if len(change_queue) == 4:
                change_list = tuple(change_queue)
                if change_list not in monkey_map:
                    monkey_map[change_list] = new_sec % 10
                    all_change_sets.add(change_list)
            val = new_sec
    
    max_sales = 0
    for change in all_change_sets:
        sales = 0
        for monkey, monkey_map in sell_map.items():
            sales += monkey_map.get(change, 0)
        if sales > max_sales:
            max_sales = sales
            max_change = change
    
    print(f'The max change {max_change} gets {max_sales} bananas')


if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = [int(line.strip()) for line in file.readlines()]
    
    main_part1(mult_string)
    main_part2(mult_string)