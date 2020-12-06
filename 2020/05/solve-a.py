#!/usr/bin/env python3
def bin_str_to_num(s, z, o):
    value = 0
    for ch in s:
        if ch == z:
            value = value * 2
        elif ch == o:
            value = (value * 2) + 1
        else:
            print('Error: no {0} in {1}'.format(ch, s))
            return 0
    return value


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    codes = [line.strip() for line in all_lines]

    highest_id = 0
    for code in codes:
        row_code = code[:7]
        seat_code = code[7:]

        row_number = bin_str_to_num(row_code, 'F', 'B')
        seat_number = bin_str_to_num(seat_code, 'L', 'R')
        seat_id = (row_number * 8) + seat_number

        highest_id = max(highest_id, seat_id)

    print('The highest seat ID is {0}'.format(highest_id))


if __name__ == '__main__':
    main()
