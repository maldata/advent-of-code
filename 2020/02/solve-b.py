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
            idx1 = int(result.group(1))
            idx2 = int(result.group(2))
            letter = result.group(3)
            password = result.group(4)

            # Adjust for the index-zero policy
            idx1 = idx1 - 1
            idx2 = idx2 - 1

            idx1_valid = len(password) > idx1 and password[idx1] == letter
            idx2_valid = len(password) > idx2 and password[idx2] == letter

            if (idx1_valid and not idx2_valid) or (idx2_valid and not idx1_valid):
                passes = passes + 1
            else:
                failures = failures + 1

    print("There were {0} valid passwords and {1} invalid passwords".format(passes, failures))


if __name__ == '__main__':
    main()
