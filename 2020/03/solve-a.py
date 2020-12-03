#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    map_rows = [line.strip() for line in all_lines]
    num_rows = len(map_rows)
    unit_width = len(map_rows[0])

    x_pos = 0
    y_pos = 0
    delta_x = 3
    delta_y = 1
    num_trees = 0
    while True:
        x_pos = (x_pos + delta_x) % unit_width
        y_pos = y_pos + delta_y

        if y_pos >= num_rows:
            break

        new_space = map_rows[y_pos][x_pos]
        if new_space == '#':
            num_trees = num_trees + 1

    print('Ran into {0} trees.'.format(num_trees))


if __name__ == '__main__':
    main()
