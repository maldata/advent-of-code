#!/usr/bin/env python3
import re


def process_mask_line(cmd_string):
    # example: mask = 11111XX10X1X0XX01101101X111101011000
    parts = cmd_string.split('=')
    if len(parts) != 2:
        print('Malformed mask line "{0}"'.format(cmd_string))
        return None
    return parts[1].strip()
    

def process_mem_line(cmd_string, mem, mask_str):
    # example: mem[23668] = 290432615
    r = re.search('^mem\[([0-9]+)\] = ([0-9]+)', cmd_string)
    if r is None or len(r.groups()) != 2:
        print('Malformed mem line "{0}"'.format(cmd_string))
        return None

    index = int(r.group(1))
    value = int(r.group(2))

    # Make sure our array is large enough
    current_size = len(mem)
    required_size = index + 1
    if required_size > current_size:
        additional_buffer = [0] * (required_size - current_size)
        mem = mem + additional_buffer

    value_as_bits = format(value, 'b')
    # add leading zeros
    if len(value_as_bits) < 36:
        value_as_bits = '0' * (36 - len(value_as_bits)) + value_as_bits

    masked = [mask_bit(i[0], i[1]) for i in zip(mask_str, value_as_bits)]
    masked = ''.join(masked)
    addresses = expand_floating_masks([masked])
    for a in addresses:
        int_addr = int(a, base=2)
        mem[int_addr] = value

    return mem


def expand_floating_masks(mask_str_list):
    no_floats = list(filter(lambda s: 'X' not in s, mask_str_list))
    has_floats = list(filter(lambda s: 'X' in s, mask_str_list))

    # If the there are no floating bits left in list we got, we're done!
    if len(no_floats) == len(mask_str_list):
        return no_floats

    # If there are floating bits left, we expand one, then repeat
    working = has_floats[0]
    remaining = has_floats[1:]

    i = working.index('X')
    pre = working[0:i]
    post = working[i + 1:]
    replacements = [pre + '0' + post, pre + '1' + post]
    return no_floats + expand_floating_masks(remaining + replacements)


def mask_bit(mask, bit):
    if mask == 'X':
        return 'X'
    elif mask == '0':
        return bit
    elif mask == '1':
        return '1'
    else:
        print('{0} is not a valid mask!'.format(mask))
        return None


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
            mem = process_mem_line(cmd, mem, mask_str)
        else:
            print('I have no idea how to process a line like "{0}"'.format(cmd))

    print('The sum of values in memory is {0}'.format(sum(mem)))


if __name__ == '__main__':
    main()
