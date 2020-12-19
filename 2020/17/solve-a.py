#!/usr/bin/env python3
class Cube:
    def __init__(self, active, coords):
        self.active = active
        self.position = coords

        
class Space:
    def __init__(self, file_path):
        self.cube_lookup = {}
        self.frontier_cubes = []
        self.mins = []
        self.maxs = []

        with open(file_path, 'r') as f:
            all_lines = f.readlines()

        input_plane = [i.strip() for i in all_lines]
        for row_idx in range(len(input_plane)):
            for col_idx in range(len(input_plane[row_idx])):
                active = input_plane[row_idx][col_idx] == '#'
                pos = (col_idx, row_idx, 0)
                self.cube_lookup[pos] = Cube(active, pos)
                self.frontier_cubes.append(self.cube_lookup[pos])

        self.set_mins_maxs()

    def set_mins_maxs(self):
        all_coords = [(self.cube_lookup[point].position[0], self.cube_lookup[point].position[1], self.cube_lookup[point].position[2]) for point in self.cube_lookup]
        by_axis = list(zip(*all_coords))
        self.mins = list(map(min, by_axis))
        self.maxs = list(map(max, by_axis))

    def print_space(self):
        sep = '-----------------'
        for z in range(self.mins[2], self.maxs[2] + 1):
            print(sep)
            print('z = {0}'.format(z))
            print()
            
            for y in range(self.mins[1], self.maxs[1] + 1):
                row = ''
                for x in range(self.mins[0], self.maxs[0] + 1):
                    cube = self.cube_lookup[(x,y,z)]
                    if cube.active:
                        row = row + '#'
                    else:
                        row = row + '.'
                print(row)

            print()
            print(sep)

    def get_num_active_cubes(self):
        statuses = [self.cube_lookup[c].active for c in self.cube_lookup]
        f = filter(lambda x: x == True, statuses)
        return len(list(f))

    def get_neighboring_points(self, cube):
        deltas = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    deltas.append( (dx, dy, dz) )
                    
        index_of_origin = deltas.index( (0, 0, 0) )
        deltas = deltas[0:index_of_origin] + deltas[index_of_origin + 1:]
        
        p = cube.position
        neighbors = [(p[0] + d[0], p[1] + d[1], p[2] + d[2]) for d in deltas]
        return neighbors
    
    def grow(self):
        new_frontier = []
        for fc in self.frontier_cubes:
            neighboring_points = self.get_neighboring_points(fc)
            for n in neighboring_points:
                if n not in self.cube_lookup:
                    # Nothing at this position yet. Make a new
                    # cube and set it as being on the frontier.
                    self.cube_lookup[n] = Cube(False, n)
                    new_frontier.append(self.cube_lookup[n])

        self.frontier_cubes = new_frontier
        self.set_mins_maxs()


    def evolve(self):
        for c in self.cube_lookup:
            current_cube = self.cube_lookup[c]
            active_neighbors = 0
            for n in self.get_neighboring_points(current_cube):                
                if n in self.cube_lookup and self.cube_lookup[n].active:
                    active_neighbors = active_neighbors + 1

            if c[0] == 0 and c[1] == 1 and c[2] == -1:
                print(self.get_neighboring_points(current_cube))
                    
            is_active = current_cube.active
            if is_active and (active_neighbors == 2 or active_neighbors == 3):
                current_cube.active = True
            elif not is_active and active_neighbors == 3:
                current_cube.active = True
            else:
                current_cube.active = False


def main():
    s = Space('./test-input.txt')
    s.print_space()

    sep = "*****************"
    
    num_iterations = 1
    for i in range(num_iterations):
        s.grow()
        s.evolve()

        print(sep)
        print('AFTER {0} ITERATIONS:'.format(i+1))
        print()
        s.print_space()
        
        
if __name__ == '__main__':
    main()
