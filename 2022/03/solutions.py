def letter_priority(letter):
    upper_case_priority_offset = 38
    lower_case_priority_offset = 96

    priority = 0
    if letter.isupper():
        priority = ord(letter) - upper_case_priority_offset
    else:
        priority = ord(letter) - lower_case_priority_offset
    
    return priority

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
    return letter_priority(duplicated_char)


def part1():
    all_lines = []
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    sum_of_priorities = 0
    for line in all_lines:
        sum_of_priorities = sum_of_priorities + part1_calc_priority(line)

    print(f'Part 1 - sum of priorities: {sum_of_priorities}')


def part2_calc_priority(line_group):
    sack0 = set([i for i in line_group[0].strip()])
    sack1 = set([i for i in line_group[1].strip()])
    sack2 = set([i for i in line_group[2].strip()])

    badge_set = sack0.intersection(sack1, sack2)
    if len(badge_set) != 1:
        print("Didn't find exactly one badge!")

    badge = list(badge_set)[0]
    return letter_priority(badge)


def part2():
    all_lines = []
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    num_lines = len(all_lines)
    if num_lines % 3 != 0:
        print("We don't have an integer multiple of three lines!")
    num_groups = num_lines // 3

    sum_of_priorities = 0
    for group in range(num_groups):
        group_lines = all_lines[group * 3 : (group * 3) + 3]
        sum_of_priorities = sum_of_priorities + part2_calc_priority(group_lines)

    print(f'Part 2 - sum of priorities: {sum_of_priorities}')


if __name__ == '__main__':
    part1()
    part2()
