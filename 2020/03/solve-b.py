#!/usr/bin/env python3
def get_num_trees(map_rows, delta_x, delta_y):
    num_rows = len(map_rows)
    unit_width = len(map_rows[0])

    x_pos = 0
    y_pos = 0
    num_trees = 0
    while True:
        x_pos = (x_pos + delta_x) % unit_width
        y_pos = y_pos + delta_y

        if y_pos >= num_rows:
            break

        new_space = map_rows[y_pos][x_pos]
        if new_space == '#':
            num_trees = num_trees + 1

    return num_trees


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    map_rows = [line.strip() for line in all_lines]
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    product = 1
    for delta_x, delta_y in slopes:
        product = product * get_num_trees(map_rows, delta_x, delta_y)

    print('Final product : {0}'.format(product))


if __name__ == '__main__':
    main()
