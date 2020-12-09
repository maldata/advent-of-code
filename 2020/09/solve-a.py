#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    sequence = [int(i.strip()) for i in all_lines]
    seed_length = 25
    idx = seed_length
    while idx < len(sequence):
        seeds = sequence[idx - seed_length:idx]
        target = sequence[idx]

        pair_found = False
        for s in seeds:
            t = target - s
            if t in seeds and t != s:
                pair_found = True

        if not pair_found:
            print('{0} at index {1} is not the sum of any two of the previous {2} values.'.format(target, idx, seed_length))
            break

        idx = idx + 1


if __name__ == '__main__':
    main()
