#!/usr/bin/env python3

def read_depths():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    return [int(line.strip()) for line in all_lines]


def solve_a(depths):
    pairs = zip(depths[0:-1], depths[1:])
    increases = filter(lambda x: x[1] > x[0], pairs)
    num_increases = len(list(increases))
    print('The depth increases {0} times.'.format(num_increases))

    
def solve_b(depths, window_size):
    num_windows = len(depths) - window_size + 1
    window_sums = [sum(depths[start_idx:start_idx+window_size]) for start_idx in range(num_windows)]
    solve_a(window_sums)

    
if __name__ == '__main__':
    depths = read_depths()
    solve_a(depths)
    solve_b(depths, 3)
