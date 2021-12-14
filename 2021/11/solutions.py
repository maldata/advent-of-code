class Octopus:
    def __init__(self) -> None:
        self.energy = 0


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    stripped = [line.strip() for line in all_lines]
    num_rows = len(stripped)
    num_cols = len(stripped[0])
    octopi = {}
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            coord = (row_idx, col_idx)
            octopi[coord] = int(stripped[row_idx][col_idx])

    return octopi, num_rows, num_cols


def get_neighbors(coord, num_rows, num_cols):
    r = coord[0]
    c = coord[1]
    r_range = range(r - 1, r + 2)
    c_range = range(c - 1, c + 2)
    all_nearby = [(r,c) for r in r_range for c in c_range]

    # Take out the input
    neighbors = filter(lambda x: x != coord, all_nearby)
    
    # Take out the coordinates that are out of bounds
    neighbors = filter(lambda x: 0 <= x[0] < num_rows and 0 <= x[1] < num_cols, neighbors)

    return list(neighbors)


def do_one_step(octopi, num_rows, num_cols):
    flashed_this_step = {}
    all_coords = [(r,c) for r in range(num_rows) for c in range(num_cols)]

    # First, everyone goes up by one. Record the ones that flashed (went from 9 to 10)
    flashed = []
    for coord in all_coords:
        flashed_this_step[coord] = False
        octopi[coord] = octopi[coord] + 1
        if octopi[coord] > 9:
            flashed.append(coord)
            flashed_this_step[coord] = True

    # Get the neighbors of the ones that flashed most recently and add one to them
    # That might make more of them flash. Keep going until it converges        
    while len(flashed) > 0:
        coord = flashed.pop()
        neighbors = get_neighbors(coord, num_rows, num_cols)
        for n in neighbors:
            octopi[n] = octopi[n] + 1
            if octopi[n] > 9 and not flashed_this_step[n]:
                flashed.append(n)
                flashed_this_step[n] = True
    
    # Reset the ones that flashed to zero
    num_flashes = 0
    for coord in flashed_this_step:
        if flashed_this_step[coord]:
            octopi[coord] = 0
            num_flashes = num_flashes + 1
    
    return octopi, num_flashes


def print_octopi(octopi, num_rows, num_cols):
    print('------------------------')
    print()
    for r in range(num_rows):
        row = ''.join([str(octopi[(r,c)]) for c in range(num_cols)])
        print(row)


def solve_a(octopi, num_rows, num_cols, num_steps):
    num_flashes = 0
    for step in range(num_steps):
        octopi, step_flashes = do_one_step(octopi, num_rows, num_cols)
        num_flashes = num_flashes + step_flashes
        print_octopi(octopi, num_rows, num_cols)

    print('After {0} steps there were {1} flashes'.format(num_steps, num_flashes))


def main():
    octopi, num_rows, num_cols = read_input('./input.txt')
    solve_a(octopi, num_rows, num_cols, 100)


if __name__ == '__main__':
    main()
