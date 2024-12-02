def get_lists(lists:list[str]) -> (list[int], list[int]):
    
    list1 = []
    list2 = []

    for _, line in enumerate(lists):
        vals = line.split()
        list1.append(int(vals[0]))
        list2.append(int(vals[1]))

    list1.sort()
    list2.sort()

    return list1, list2

def main_part1(list1, list2):

    diff_sum = 0

    for idx, v1 in enumerate(list1):
        diff_sum += abs(v1 - list2[idx])
    
    print (f'diff_sum = {diff_sum}')

def main_part2(list1, list2):

    sim_score = 0
    for _, val1 in enumerate(list1):
        sim_score += val1 * list2.count(val1)

    print(f'sim_score = {sim_score}')

def main():
    with open("../inputs.txt") as file:
        lists = file.readlines()
    
    list1, list2 = get_lists(lists=lists)
    main_part1(list1, list2)
    main_part2(list1, list2)

if __name__ == "__main__":
    main()
    