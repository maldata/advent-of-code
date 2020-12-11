#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_adapters = [int(i.strip()) for i in all_lines]
    all_adapters.sort()

    # Add the built-in adapter that's 3 jolts higher than the maximum
    all_joltages = [0] + all_adapters + [all_adapters[-1] + 3]
    deltas = [z[1] - z[0] for z in zip(all_joltages[:-1], all_joltages[1:])]

    output_msg = 'The number of 1-jolt differences ({0}) times the number of 3-jolt differences ({1}) = {2}'
    print(output_msg.format(deltas.count(1), deltas.count(3), deltas.count(1) * deltas.count(3)))


if __name__ == '__main__':
    main()
