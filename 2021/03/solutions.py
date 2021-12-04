#!/usr/bin/env python3

def read_report():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    stripped_lines = [line.strip() for line in all_lines]
    return [[int(i) for i in s] for s in stripped_lines]


def get_most_common(report):
    num_lines = len(report)
    bits = list(zip(*report))
    sums = [sum(b) for b in bits]
    return [0 if s <= num_lines / 2 else 1 for s in sums]


def get_least_common(report):
    most_common_bits = get_most_common(report)
    return [-i + 1 for i in most_common_bits]


def binary_list_to_integer(input_list):
    decimal_num = 0
    for i in range(len(input_list)):
        decimal_num = decimal_num + input_list[i] * (2 ** i)    
    return decimal_num


def get_gamma(report):
    most_common_bits = get_most_common(report)
    most_common_bits.reverse()
    return binary_list_to_integer(most_common_bits)
    

def get_epsilon(report):
    least_common_bits = get_least_common(report)
    least_common_bits.reverse()
    return binary_list_to_integer(least_common_bits)


def solve_a(report):
    gamma = get_gamma(report)
    epsilon = get_epsilon(report)
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
    report = read_report()
    solve_a(report)
    solve_b(report)


if __name__ == '__main__':
    main()
