def test_answers(answer:int, input_nums: list[int], concat:bool = False) -> bool:
    test_answer = answer
    for num in reversed(input_nums):
        if len(input_nums) == 1:
            return test_answer == input_nums[0]
        if concat:
            arg_len = len(str(num))
            str_test_answer = str(test_answer)
            if str_test_answer[-arg_len:] == str(num):
                if arg_len == len(str_test_answer):
                    return True
                if test_answers(int(str_test_answer[:len(str_test_answer)-arg_len]), input_nums[:-1], concat):
                    return True
        if test_answer % num == 0:
            if test_answers(int(test_answer / num), [x for x in input_nums[:-1]], concat):
                return True
        test_answer -= num
        if test_answer < 0:
            return False
        
        return test_answers(test_answer, [x for x in input_nums[:-1]], concat)
            

def main_part1(inputs:list[str]):
    valid_sum = 0
    for line in inputs:
        answer, input_num_str = line.strip().split(':')
        answer = int(answer)
        input_nums = [int(val) for val in input_num_str.strip().split()]
        valid = test_answers(answer, input_nums)
        if valid:
            valid_sum += answer
    
    print(f'Sum of valid calibrations = {valid_sum}')

def main_part2(inputs:list[str]):
    valid_sum = 0
    for line in inputs:
        answer, input_num_str = line.strip().split(':')
        answer = int(answer)
        input_nums = [int(val) for val in input_num_str.strip().split()]
        valid = test_answers(answer, input_nums, True)
        if valid:
            valid_sum += answer
    
    print(f'Sum of valid calibrations with concat = {valid_sum}')

if __name__ == "__main__":
    with open("../inputs.txt") as file:
        mult_string = file.readlines()
    
    main_part1(mult_string)
    main_part2(mult_string)