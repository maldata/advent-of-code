#!/usr/bin/env python3
from program import Program


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    program_text = all_lines[0].strip()
    program = Program(program_text)


if __name__ == '__main__':
    main()
