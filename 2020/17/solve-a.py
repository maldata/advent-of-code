#!/usr/bin/env python3

deltas = []
for dx in range(-1, 2):
    for dy in range(-1, 2):
        for dz in range(-1, 2):
            deltas.append( (dx, dy, dz) )

index_of_origin = deltas.index( (0, 0, 0) )
deltas = deltas[0:index_of_origin] + deltas[index_of_origin + 1:]


def get_neighbors(point):
    return [(point[0] + d[0], point[1] + d[1], point[2] + d[2]) for d in deltas]


def iterate(coords):
    new_coords = {}
    for c in coords:
        active_neighbors = 0
        for n in get_neighbors(c):
            if coords.get(n, False):
                active_neighbors = active_neighbors + 1
            
        is_active = coords[c]
        if is_active and (active_neighbors == 2 or active_neighbors == 3):
            new_coords[c] = True
        elif not is_active and active_neighbors == 3:
            new_coords[c] = True
        else:
            new_coords[c] = False
        
    return new_coords


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    plane = [i.strip() for i in all_lines]
    coords = {}
    for row_idx in range(len(plane)):
        for col_idx in range(len(plane[row_idx])):
            active = plane[row_idx][col_idx] == '#'
            element = (col_idx, row_idx, 0)
            coords[element] = active

    for cycle_idx in range(6):
        coords = iterate(coords)
        print(new_coords)
        print()
        print()
        print()
        
    active_cubes = 0
    for cube in coords:
        if cube:
            active_cubes = active_cubes + 1

    print('There are {0} active cubes.'.format(active_cubes))
    
    
if __name__ == '__main__':
    main()
