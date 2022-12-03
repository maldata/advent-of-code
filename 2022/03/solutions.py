def part1_calc_priority(raw_line):
    line = raw_line.strip()
    length = len(line)

    if length % 2 != 0:
        print("There's a line that has an odd number of letters!")
    
    first_half = line[0 : length // 2]
    second_half = line[length // 2 :]

    first_set = set([i for i in first_half])
    second_set = set([i for i in second_half])

    same_char_set = first_set.intersection(second_set)
    if len(same_char_set) != 1:
        print("There's an intersection without exactly one character!")

    duplicated_char = list(same_char_set)[0]

    upper_case_priority_offset = 38
    lower_case_priority_offset = 96

    priority = 0
    if duplicated_char.isupper():
        priority = ord(duplicated_char) - upper_case_priority_offset
    else:
        priority = ord(duplicated_char) - lower_case_priority_offset
    
    return priority

def part1():
    all_lines = []
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    sum_of_priorities = 0
    for line in all_lines:
        sum_of_priorities = sum_of_priorities + part1_calc_priority(line)

    print(f'Part 1 - sum of priorities: {sum_of_priorities}')
        

def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
