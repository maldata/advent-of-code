#!/usr/bin/env python3
import re


def process_mask_line(cmd_string):
    # example: mask = 11111XX10X1X0XX01101101X111101011000
    parts = cmd_string.split('=')
    if len(parts) != 2:
        print('Malformed mask line "{0}"'.format(cmd_string))
        return None
    return parts[1].strip()
    

def process_mem_line(cmd_string, memory, mask_str):
    # example: mem[23668] = 290432615
    parts = cmd_string.split('=')
    if len(parts) != 2:
        print('Malformed mem line "{0}"'.format(cmd_string))
        return None

    input_value = parts[1].strip()
    # TODO: append more memory if needed
    # TODO: apply the mask to the value
    # TODO: set the masked value in memory
    pass


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    command_strings = [i.strip() for i in all_lines]

    mask_str = ''
    mem = []
    for cmd in command_strings:
        if cmd[0:4] == 'mask':
            mask_str = process_mask_line(cmd)
        elif cmd[0:3] == 'mem':
            process_mem_line(cmd, mem, mask)
        else:
            print('I have no idea how to process a line like "{0}"'.format(cmd))


if __name__ == '__main__':
    main()
