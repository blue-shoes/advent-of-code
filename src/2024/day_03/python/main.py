import re
import functools

def get_sequence_sums(sequences:list[str]) -> int:
    mult_opts = []
    pattern = re.compile("mul\\((\\d{1,3},\\d{1,3})\\)")
    for line in sequences:
        mult_opts.extend(re.findall(pattern, line))

    mult_map = list(map(lambda pair: int(pair.split(',')[0])*int(pair.split(',')[1]),mult_opts))
    return functools.reduce(lambda a, b: a + b, mult_map)

def main_part1(mult_string:list[str]):
    
    sum = get_sequence_sums(mult_string)

    print(f'Multiplication results are {sum}')

def main_part2(mult_string:list[str]):
    full_string = ''.join(mult_string)
    dont_splits = full_string.split("don't()")

    do_splits = []
    for idx, split in enumerate(dont_splits):
        if idx == 0:
            do_splits.append(split)
            continue
        do_split = split.split('do()')
        if len(do_split) > 1:
            do_splits.extend(do_split[1:])

    sum = get_sequence_sums(do_splits)
    print(f'Enabled multiplication results are {sum}')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    main_part1(mult_string)
    main_part2(mult_string)