
def main_part1(reports:list[int]):
    safe_count = 0
    
    for report in reports:
        safe, _ = evaluate_report(report)
        if safe:
            safe_count += 1
    
    print(f'There are {safe_count} safe reports')

def evaluate_report(report:list[int]) -> (bool, int):
    last_inc = None
    last_val = None
    for idx, level in enumerate(report):
        if not last_val:
            last_val = level
            continue

        inc = last_val - level
        if inc == 0:
            return False, idx
        if abs(inc) > 3:
            return False, idx
        if last_inc and inc * last_inc <= 0:
            return False, idx
        last_inc = inc
        last_val = level
    
    return True, -1

def main_part2(reports:list[list[int]]):
    safe_count = 0
    for r_idx, report in enumerate(reports):
        safe, idx = evaluate_report(report)
        if safe:
            safe_count += 1
            continue
        tmp_report = report.copy()
        tmp_report.pop(idx)
        safe, _ = evaluate_report(tmp_report)
        if safe:
            safe_count += 1
            continue
        tmp_report2 = report.copy()
        tmp_report2.pop(idx-1)
        safe, _ = evaluate_report(tmp_report2)
        if safe:
            safe_count += 1
            continue

        if idx-1 > 0:
            tmp_report3 = report.copy()
            tmp_report3.pop(0)
            safe, _ = evaluate_report(tmp_report3)
            if safe:
                safe_count += 1

    print(f'With the Problem Dampener, there are {safe_count} safe reports')

def get_reports(report_str: list[str]) -> list[int]:      
    return [[int(level) for level in report.strip().split()] for report in report_str]

def main():
    with open("../inputs.txt") as file:
        report_strs = file.readlines()
    
    reports = get_reports(report_str=report_strs)

    main_part1(reports)
    main_part2(reports)

if __name__ == "__main__":
    main()
    