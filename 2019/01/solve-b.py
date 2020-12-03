#!/usr/bin/env python3

import math


def calc_fuel(m):
    fuel = math.floor(m/3.0) - 2

    if fuel < 0:
        return 0
    else:
        return fuel + calc_fuel(fuel)


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    module_masses = [int(line.strip()) for line in all_lines]
    fuel_per_module = [calc_fuel(m) for m in module_masses]

    print('Cumulative fuel requirement: {0}'.format(sum(fuel_per_module)))
    

if __name__ == '__main__':
    main()
    
