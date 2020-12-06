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

    lowest_id = 2**10
    highest_id = 0
    all_ids = []
    for code in codes:
        row_code = code[:7]
        seat_code = code[7:]

        row_number = bin_str_to_num(row_code, 'F', 'B')
        seat_number = bin_str_to_num(seat_code, 'L', 'R')
        seat_id = (row_number * 8) + seat_number
        all_ids.append(seat_id)
        
        lowest_id = min(lowest_id, seat_id)
        highest_id = max(highest_id, seat_id)

    print('The lowest seat ID is {0}'.format(lowest_id))
    print('The highest seat ID is {0}'.format(highest_id))

    all_ids.sort()

    for i, j in enumerate(all_ids):
        if i == 0 or i == len(all_ids) - 1:
            continue

        if all_ids[i-1] == j - 1 and all_ids[i+1] == j + 1:
            continue

        print('Found a gap at index {0}.'.format(i))
        print(all_ids[i-1:i+1])

if __name__ == '__main__':
    main()
