#!/usr/bin/env python3

def read_report(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    stripped_lines = [line.strip() for line in all_lines]
    return [[int(i) for i in s] for s in stripped_lines]


def get_most_common(report):
    num_lines = len(report)
    bits = list(zip(*report))
    num_ones = [sum(b) for b in bits]
    num_zeros = [num_lines - n for n in num_ones]

    return [0 if num_zeros[i] > num_ones[i] else 1 for i in range(len(num_ones))]


def get_least_common(report):
    num_lines = len(report)
    bits = list(zip(*report))
    num_ones = [sum(b) for b in bits]
    num_zeros = [num_lines - n for n in num_ones]

    return [1 if num_zeros[i] > num_ones[i] else 0 for i in range(len(num_ones))]


def binary_list_to_integer(input_list):
    list_copy = [i for i in input_list]
    list_copy.reverse()
    decimal_num = 0
    for i in range(len(list_copy)):
        decimal_num = decimal_num + list_copy[i] * (2 ** i)    
    return decimal_num


def solve_a(report):
    most_common_bits = get_most_common(report)
    gamma = binary_list_to_integer(most_common_bits)
    least_common_bits = get_least_common(report)
    epsilon = binary_list_to_integer(least_common_bits)
    print('Power consumption: {0}'.format(gamma * epsilon))


def get_o2_rating(report):
    target_position = 0
    while len(report) > 1:
        most_common_bits = get_most_common(report)
        target_bit = most_common_bits[target_position]
        f = filter(lambda x: x[target_position] == target_bit, report)
        report = list(f)
        target_position = target_position + 1
    return binary_list_to_integer(report[0])


def get_co2_rating(report):
    target_position = 0
    while len(report) > 1:
        least_common_bits = get_least_common(report)
        target_bit = least_common_bits[target_position]
        f = filter(lambda x: x[target_position] == target_bit, report)
        report = list(f)
        target_position = target_position + 1
    return binary_list_to_integer(report[0])


def solve_b(report):
    o2_rating = get_o2_rating(report)
    co2_rating = get_co2_rating(report)
    print('Life support rating: {0}'.format(o2_rating * co2_rating))


def main():
    report = read_report('./input.txt')
    solve_a(report)
    solve_b(report)


if __name__ == '__main__':
    main()
