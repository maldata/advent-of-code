import re


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    line_definitions = []
    for line in all_lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        m = re.match('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)', line)
        if m is None:
            print("A line doesn't match the regex!: {0}".format(line))
            return

        line_definitions.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    
    return line_definitions


def do_horiz_and_vert(line_definitions):
    counts = {}

    for line_def in line_definitions:
        x1 = line_def[0]
        y1 = line_def[1]
        x2 = line_def[2]
        y2 = line_def[3]

        if x1 != x2 and y1 != y2:
            continue

        xmin = min([x1, x2])
        xmax = max([x1, x2])
        ymin = min([y1, y2])
        ymax = max([y1, y2])

        if xmin == xmax:
            y_vals = range(ymin, ymax + 1)
            coords = [(xmin, y) for y in y_vals]
        elif ymin == ymax:
            x_vals = range(xmin, xmax + 1)
            coords = [(x, ymin) for x in x_vals]

        for coord in coords:
            if coord in counts:
                counts[coord] = counts[coord] + 1
            else:
                counts[coord] = 1

    return counts


def add_diagonals(counts, line_definitions):
    for line_def in line_definitions:
        x1 = line_def[0]
        y1 = line_def[1]
        x2 = line_def[2]
        y2 = line_def[3]

        # We're only doing the diagonal lines here
        if x1 == x2 or y1 == y2:
            continue

        xmin = min([x1, x2])
        xmax = max([x1, x2])
        ymin = min([y1, y2])
        ymax = max([y1, y2])

        x_vals = list(range(xmin, xmax + 1))
        y_vals = list(range(ymin, ymax + 1))

        if x1 == xmax:
            x_vals.reverse()
        if y1 == ymax:
            y_vals.reverse()

        coords = zip(x_vals, y_vals)

        for coord in coords:
            if coord in counts:
                counts[coord] = counts[coord] + 1
            else:
                counts[coord] = 1


def get_at_least(counts, at_least):
    num_at_least = 0
    for coord in counts:
        if counts[coord] >= at_least:
            num_at_least = num_at_least + 1
    return num_at_least    


def solve_a(line_definitions):
    counts = do_horiz_and_vert(line_definitions)
    at_least_two = get_at_least(counts, 2)
    print("There are {0} points with at least two counts.".format(at_least_two))


def solve_b(line_definitions):
    counts = do_horiz_and_vert(line_definitions)
    add_diagonals(counts, line_definitions)
    at_least_two = get_at_least(counts, 2)
    print("There are {0} points with at least two counts.".format(at_least_two))


def main():
    line_definitions = read_input('./input.txt')
    solve_a(line_definitions)
    solve_b(line_definitions)


if __name__ == '__main__':
    main()
