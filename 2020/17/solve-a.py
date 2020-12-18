#!/usr/bin/env python3

deltas = []
for dx in range(-1, 2):
    for dy in range(-1, 2):
        for dz in range(-1, 2):
            deltas.append( (dx, dy, dz) )

index_of_origin = deltas.index( (0, 0, 0) )
deltas = deltas[0:index_of_origin] + deltas[index_of_origin + 1:]


class Cube:
    def __init__(self, active, frontier, coords):
        self.active = active
        self.frontier = frontier
        self.position = coords


def get_neighboring_points(point):
    return [(point[0] + d[0], point[1] + d[1], point[2] + d[2]) for d in deltas]


def grow_space(coords, frontier_cubes):
    new_frontier = []
    for fc in frontier_cubes:
        fc.frontier = False  # Unset this cube as a frontier cube
        neighboring_points = get_neighboring_points(fc.position)
        for n in neighboring_points:
            if n not in coords:
                # Nothing at this position yet. Make a new cube and set it as being on the frontier.
                coords[n] = Cube(False, True, n)
                new_frontier.append(coords[n])

    return coords, new_frontier


def iterate(coords, frontier_cubes):
    new_coords, new_frontier = grow_space(coords, frontier_cubes)
    for c in new_coords:
        active_neighbors = 0
        for n in get_neighboring_points(c):
            if n in new_coords and new_coords[n].active:
                active_neighbors = active_neighbors + 1
            
        is_active = new_coords[c].active
        if is_active and (active_neighbors == 2 or active_neighbors == 3):
            new_coords[c].active = True
        elif not is_active and active_neighbors == 3:
            new_coords[c].active = True
        else:
            new_coords[c].active = False
        
    return new_coords, new_frontier


def main():
    with open('./test-input.txt', 'r') as f:
        all_lines = f.readlines()

    plane = [i.strip() for i in all_lines]
    coords = {}
    frontier_cubes = []
    for row_idx in range(len(plane)):
        for col_idx in range(len(plane[row_idx])):
            active = plane[row_idx][col_idx] == '#'
            pos = (col_idx, row_idx, 0)
            coords[pos] = Cube(active, True, pos)
            frontier_cubes.append(coords[pos])

    for cycle_idx in range(6):
        coords, frontier_cubes = iterate(coords, frontier_cubes)
        print([(coord, coords[coord].active) for coord in coords])
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
