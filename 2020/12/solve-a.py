#!/usr/bin/env python3
cw_bearings = ['N', 'E', 'S', 'W']
num_bearings = len(cw_bearings)


def parse_rotation(bearing, direc, mag):
    rotation = int(mag / 90)
    if direc == 'L':
        rotation = -1 * rotation

    bearing_idx = cw_bearings.index(bearing)
    new_bearing_idx = (bearing_idx + rotation) % num_bearings
    return cw_bearings[new_bearing_idx]


def main():
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()

    steps = [line.strip() for line in all_lines]
    steps = [(i[0], int(i[1:])) for i in steps]

    bearing = 'E'
    x_pos = 0
    y_pos = 0
    for s in steps:
        direc = s[0]
        mag = s[1]

        if direc == 'F':
            direc = bearing

        if direc == 'L' or direc == 'R':
            bearing = parse_rotation(bearing, direc, mag)
        elif direc == 'N':
            y_pos = y_pos + mag
        elif direc == 'S':
            y_pos = y_pos - mag
        elif direc == 'E':
            x_pos = x_pos + mag
        elif direc == 'W':
            x_pos = x_pos - mag
        else:
            print('Invalid direction {0}'.format(direc))
            break

    print('Final position is ({0}, {1}), Manhattan distance = {2}'.format(x_pos, y_pos, abs(x_pos) + abs(y_pos)))


if __name__ == '__main__':
    main()
