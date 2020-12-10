#!/usr/bin/env python3
from computer import Computer


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    program_text = all_lines[0].strip()
    program = program_text.split(',')
    c = Computer(program)
    c.compute()


if __name__ == '__main__':
    main()
