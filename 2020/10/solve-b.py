#!/usr/bin/env python3
def count_paths(joltages):
    if len(joltages) == 1:
        return 1

    valid_next_joltages = filter(lambda x: x <= joltages[0] + 3, joltages[1:])
    child_indices = [joltages.index(i) for i in valid_next_joltages]
    child_paths = [count_paths(joltages[c:]) for c in child_indices]
    return sum(child_paths)


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_adapters = [int(i.strip()) for i in all_lines]
    all_adapters.sort()

    # Add the wall joltage and the built-in adapter that's 3 jolts higher than the maximum
    all_joltages = [0] + all_adapters + [all_adapters[-1] + 3]

    # We need to count the number of valid paths from the wall joltage to the device joltage
    num_paths = count_paths(all_joltages)
    print('There are {0} valid arrangements of adapters.'.format(num_paths))


if __name__ == '__main__':
    main()
