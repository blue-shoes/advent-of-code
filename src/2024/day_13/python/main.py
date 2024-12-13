import re
from re import Pattern

def convert_to_int(line:str, regex:Pattern) -> tuple[int, int]:
    return tuple(int(num) for num in regex.findall(line.strip())[0])

if __name__ == "__main__":
    button_match = '\\+(\\d+), Y\\+(\\d+)'
    button_regex = re.compile(button_match)
    prize_match = '=(\\d+), Y=(\\d+)'
    prize_regex = re.compile(prize_match)

    cost = 0
    cost2 = 0
    impossible = []
    idx = -3
    with open("../inputs.txt") as file:
        while True:
            idx += 4
            x1, y1 = convert_to_int(file.readline(), button_regex)
            x2, y2 = convert_to_int(file.readline(), button_regex)
            xt, yt = convert_to_int(file.readline(), prize_regex)
            
            for add in [0, 10000000000000]:
                xt += add
                yt += add

                b = round((yt - (y1*xt)/x1) / (y2-(y1*x2)/x1))
                if b < 0:
                    continue

                a = round((xt - b*x2) / x1)
                if a < 0:
                    continue

                if a*x1 + b*x2 == xt and a*y1 + b*y2 == yt and a >= 0 and b >= 0:
                    if add == 0:
                        cost += 3*a + b
                    else:
                        cost2 += 3*a + b
                        
            blank = file.readline()
            if not blank:
                break

    print(f'Minimum token amount to win is {cost}')
    print(f'Minimum token amount to win part 2 is {cost2}')