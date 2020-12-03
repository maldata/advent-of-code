#!/usr/bin/env python3

import math

def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    lines = [int(line.strip()) for line in all_lines]
    fuels = [math.floor(mass/3.0) - 2 for mass in lines]

    print('Total fuel: {0}'.format(sum(fuels)))
    

if __name__ == '__main__':
    main()
    
