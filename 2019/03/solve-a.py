#!/usr/bin/env python3
def generate_deltas(direction, distance):
    if direction == 'L':
        incr = -1
        idx = 0
    elif direction == 'R':
        incr = 1
        idx = 0
    elif direction == 'U':
        incr = 1
        idx = 1
    elif direction == 'D':
        incr = -1
        idx = 1
    else:
        print('Something has gone horrible wrong')
        return

    if idx == 0:
        d = (incr,0)
    else:
        d = (0,incr)

    return [d] * distance


def generate_path_points(full_path):
    points = [(0,0)]
    for leg in full_path:
        direction = leg[0]
        distance = int(leg[1:])

        deltas = generate_deltas(direction, distance)

        for d in deltas:
            prev = points[-1]
            new_point = (prev[0] + d[0], prev[1] + d[1])
            points.append(new_point)

    return points
    

def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_lines = [i.strip() for i in all_lines]
    all_wires = [i.split(',') for i in all_lines]

    paths = []
    for wire in all_wires:
        p = generate_path_points(wire)

        # Remove the origin from each path... we know the paths share it. 
        p = p[1:]
        paths.append(p)

    # print(paths)
    set0 = set(paths[0])
    set1 = set(paths[1])
    isct = set0.intersection(set1)

    manhattan_dists = [abs(i[0]) + abs(i[1]) for i in list(isct)]
    # print(isct)
    # print(manhattan_dists)
    print('The smallest Manhattan distance is {0}'.format(min(manhattan_dists)))
    

if __name__ == '__main__':
    main()
