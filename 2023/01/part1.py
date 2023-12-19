
def part1():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()
    
    all_lines = [l.strip() for l in all_lines]
    exploded_lines = [[i for i in l] for l in all_lines]
    numbers_only = []
    for exploded_line in exploded_lines:
        numbers = filter(lambda x: x.isnumeric(), exploded_line)
        numbers_only.append(list(numbers))
    
    calibration_values = [int(n[0] + n[-1]) for n in numbers_only]
    print(f'Part 1: {sum(calibration_values)}')


def part2():
    print('Part 2, need to pick out the strings of spelled out numbers also')
    print('That kinda sucks, because sometimes letters can be shared,')
    print('like in "oneight" or "twone"')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
