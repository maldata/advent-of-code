#!/usr/bin/env python3

import re


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    lines = [l.strip() for l in all_lines]

    passes = 0
    failures = 0
    for line in lines:
        result = re.search('^\s*([0-9]+)\s*-\s*([0-9]+)\s*([a-zA-Z])\s*:\s*([a-zA-Z]+)\s*$', line)
        if result and len(result.groups()) == 4:
            low = int(result.group(1))
            high = int(result.group(2))
            letter = result.group(3)
            password = result.group(4)

            num_target_letter = password.count(letter)
            if num_target_letter >= low and num_target_letter <= high:
                passes = passes + 1
            else:
                failures = failures + 1

    print("There were {0} valid passwords and {1} invalid passwords".format(passes, failures))


if __name__ == '__main__':
    main()
