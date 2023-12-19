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
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()
    
    all_lines = [l.strip() for l in all_lines]
    calibration_values = []
    for line in all_lines:
        exploded_line = [i for i in line]
        numbers = filter(lambda x: x[1].isnumeric(), enumerate(exploded_line))
        indices_and_values = list(numbers)
        indices_and_values = [(p[0], int(p[1])) for p in indices_and_values]

        # TODO: line 16 has two instances of "two" in it... we need to find both!

        for text_num in (('one', 1), ('two', 2), ('three', 3), 
                         ('four', 4), ('five', 5), ('six', 6),
                         ('seven', 7), ('eight', 8), ('nine', 9)):
            index = line.find(text_num[0])
            if index >= 0:
                indices_and_values.append((index, text_num[1]))
   
        indices_and_values.sort(key=lambda x: x[0])
        values = [i[1] for i in indices_and_values]
        calibration_values.append(values[0] + values[-1])
    
    print(f'Part 2: {sum(calibration_values)}')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
