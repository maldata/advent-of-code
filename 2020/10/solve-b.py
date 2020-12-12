#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_adapters = [int(i.strip()) for i in all_lines]
    all_adapters.sort()

    # Add the wall joltage and the built-in adapter that's 3 jolts higher than the maximum
    all_joltages = [0] + all_adapters + [all_adapters[-1] + 3]

    # We need to count the number of valid paths from the wall joltage to the device joltage.
    # Number of one-gaps between three-gaps        Number of paths between
    #                                     0        1
    #                                     1        1
    #                                     2        2
    #                                     3        4
    #                                     4        7
    gap_map = {0: 1, 1: 1, 2: 2, 3: 4, 4: 7}
    gaps = list([i[1]-i[0] for i in zip(all_joltages[:-1], all_joltages[1:])])

    runs_of_ones = []
    current_run_length = 0
    for idx in range(len(gaps)):
        if gaps[idx] == 3:
            runs_of_ones.append(current_run_length)
            current_run_length = 0
        else:
            current_run_length = current_run_length + 1

    multipliers = [gap_map[i] for i in runs_of_ones]

    num_paths = 1
    for i in multipliers:
        num_paths = num_paths * i
    
    print('There are {0} valid arrangements of adapters.'.format(num_paths))


if __name__ == '__main__':
    main()
