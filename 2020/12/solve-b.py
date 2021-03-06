#!/usr/bin/env python3
cw_bearings = ['N', 'E', 'S', 'W']
num_bearings = len(cw_bearings)


def parse_rotation(direc, mag):
    rotation = int(mag / 90)
    if direc == 'L':
        rotation = -1 * rotation

    cw_shifts = rotation % num_bearings
    return cw_shifts


def main():
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()

    steps = [line.strip() for line in all_lines]
    steps = [(i[0], int(i[1:])) for i in steps]

    x_pos = 0
    y_pos = 0
    relative_waypt_x = 10
    relative_waypt_y = 1
    for s in steps:
        direc = s[0]
        mag = s[1]

        if direc == 'F':
            x_pos = x_pos + (mag * relative_waypt_x)
            y_pos = y_pos + (mag * relative_waypt_y)
            continue

        if direc == 'L' or direc == 'R':
            rotation = parse_rotation(direc, mag)
            for i in range(rotation):
                temp = relative_waypt_x
                relative_waypt_x = relative_waypt_y
                relative_waypt_y = -1 * temp
        elif direc == 'N':
            relative_waypt_y = relative_waypt_y + mag
        elif direc == 'S':
            relative_waypt_y = relative_waypt_y - mag
        elif direc == 'E':
            relative_waypt_x = relative_waypt_x + mag
        elif direc == 'W':
            relative_waypt_x = relative_waypt_x - mag
        else:
            print('Invalid direction {0}'.format(direc))
            break

    print('Final position is ({0}, {1}), Manhattan distance = {2}'.format(x_pos, y_pos, abs(x_pos) + abs(y_pos)))


if __name__ == '__main__':
    main()
