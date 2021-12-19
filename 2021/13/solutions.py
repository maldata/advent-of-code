def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    reading_folds = False
    raw_points = []
    raw_folds = []
    for l in all_lines:
        s = l.strip()
        if s == '':
            reading_folds = True
            continue

        if reading_folds:
            raw_folds.append(s)
        else:
            raw_points.append(s)

    points = []
    for rp in raw_points:
        coord_str = rp.split(',')
        points.append((int(coord_str[0]), int(coord_str[1])))

    folds = []
    for rf in raw_folds:
        fold_str = rf.split(' ')
        fold_str = fold_str[2]
        fold = fold_str.split('=')
        folds.append((fold[0], int(fold[1])))

    return points, folds


def remove_duplicates(points):
    return list(set(points))


def do_x_fold(points, pos):
    # Doing an x fold, the flipped points keep the same y coordinate
    new_points = []
    for p in points:
        x = p[0]
        y = p[1]

        if x > pos:
            new_points.append((2 * pos - x, y))
        else:
            new_points.append((x, y))
    
    return remove_duplicates(new_points)


def do_y_fold(points, pos):
    # Doing a y fold, the flipped points keep the same x coordinate.
    new_points = []
    for p in points:
        x = p[0]
        y = p[1]

        if y > pos:
            new_points.append((x, 2 * pos - y))
        else:
            new_points.append((x, y))

    return remove_duplicates(new_points)


def do_one_fold(canvas, dir, pos):
    if dir == 'x':
        return do_x_fold(canvas, pos)
    else:
        return do_y_fold(canvas, pos)


def solve_a(points, folds):
    fold = folds[0]
    resulting_canvas = do_one_fold(points, fold[0], fold[1])
    num = len(resulting_canvas)
    print('Number of dots: {0}'.format(num))


def solve_b(points, folds):
    for fold in folds:
        points = do_one_fold(points, fold[0], fold[1])

    max_x = 0
    max_y = 0
    for p in points:
        max_x = max([p[0], max_x])
        max_y = max([p[1], max_y])

    num_chars = max_x + 1
    num_rows = max_y + 1
    all_coords = [(x, y) for x in range(num_chars) for y in range(num_rows)]

    for row_idx in range(num_rows):
        line_chars = [' '] * num_chars
        for c in all_coords:
            x = c[0]
            y = c[1]
            if y == row_idx and (x, y) in points:
                line_chars[x] = '#'
        line = ''.join(line_chars)
        print(line)


def main():
    points, folds = read_input('./input.txt')
    solve_a(points, folds)
    solve_b(points, folds)


if __name__ == '__main__':
    main()
