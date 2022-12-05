import re


def both_parts():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_ranges = []
    pattern = re.compile('([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)')
    for line in all_lines:
        line = line.strip()
        result = pattern.match(line)
        elf1_first = int(result.group(1))
        elf1_last  = int(result.group(2))
        elf2_first = int(result.group(3))
        elf2_last  = int(result.group(4))
        
        all_ranges.append((range(elf1_first, elf1_last + 1), range(elf2_first, elf2_last + 1)))

    num_dup_ranges = 0
    num_overlapped_pairs = 0
    for r in all_ranges:
        r1 = set(r[0])
        r2 = set(r[1])
        intersection = r1.intersection(r2)

        if intersection == r1 or intersection == r2:
            num_dup_ranges = num_dup_ranges + 1

        if len(intersection) != 0:
            num_overlapped_pairs = num_overlapped_pairs + 1

    print(f'The number of duplicated ranges is {num_dup_ranges}')
    print(f'The number of overlapping pairs is {num_overlapped_pairs}')


if __name__ == '__main__':
    both_parts()
