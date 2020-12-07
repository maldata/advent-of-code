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

    #print(paths)
    set0 = set(paths[0])
    set1 = set(paths[1])
    iscts = list(set0.intersection(set1))

    #print(iscts)

    # Don't forget to add 1 because we got rid of (0,0)
    path0_steps = [paths[0].index(i) + 1 for i in iscts]
    path1_steps = [paths[1].index(i) + 1 for i in iscts]
    #print(path0_steps)
    #print(path1_steps)
    z = zip(path0_steps, path1_steps)
    sum_steps = [i[0] + i[1] for i in z]
    print('The smallest total number of steps is {0}'.format(min(sum_steps)))

if __name__ == '__main__':
    main()
