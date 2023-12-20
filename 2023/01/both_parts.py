def get_indices_of_numerals(full_line):
    exploded_line = [i for i in full_line]
    numbers = filter(lambda x: x[1].isnumeric(), enumerate(exploded_line))
    return [(p[0], int(p[1])) for p in numbers]


def part1():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()
    
    all_lines = [l.strip() for l in all_lines]
    firsts_and_lasts = []
    for line in all_lines:
        indices_and_values = get_indices_of_numerals(line)
        indices_and_values.sort(key=lambda x: x[0])
        values = [i[1] for i in indices_and_values]
        firsts_and_lasts.append( (values[0], values[-1]) )

    calibration_values = [(10 * i[0]) + i[1] for i in firsts_and_lasts]
    print(f'Part 1: {sum(calibration_values)}')


def get_indices_of_words(full_line):
    indices_and_values = []
    for text_num in (('one', 1), ('two', 2), ('three', 3), 
                     ('four', 4), ('five', 5), ('six', 6),
                     ('seven', 7), ('eight', 8), ('nine', 9)):
        idx = 0
        while True:
            found_idx = full_line.find(text_num[0], idx)
            if found_idx < 0:
                break
            else:
                indices_and_values.append((found_idx, text_num[1]))
                idx = found_idx + 1

    return indices_and_values


def get_indices_and_values(full_line):
    return get_indices_of_numerals(full_line) + get_indices_of_words(full_line)


def part2():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()
    
    all_lines = [l.strip() for l in all_lines]
    firsts_and_lasts = []
    for line in all_lines:
        indices_and_values = get_indices_and_values(line)
        indices_and_values.sort(key=lambda x: x[0])
        values = [i[1] for i in indices_and_values]
        firsts_and_lasts.append( (values[0], values[-1]) )

    calibration_values = [(10 * i[0]) + i[1] for i in firsts_and_lasts]    
    print(f'Part 2: {sum(calibration_values)}')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
