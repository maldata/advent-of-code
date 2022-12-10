def is_visible(grid, row, col):
    """
    The tree at (row, col) in the grid is visible if it's the tallest one
    from its position out to at least one edge.
    """
    num_rows = len(grid)
    num_cols = len(grid[0])
    this_tree_height = grid[row][col]

    # First we'll look left (smaller column index)
    visible = True
    for c in range(col - 1, -1, -1):
        visible = visible and this_tree_height > grid[row][c]
        if not visible:
            break
    
    if visible:
        return True

    # Then we'll look right (larger column index)
    visible = True
    for c in range(col + 1, num_cols):
        visible = visible and this_tree_height > grid[row][c]
        if not visible:
            break

    if visible:
        return True
    
    # Then we'll look up (smaller row index)
    visible = True
    for r in range(row - 1, -1, -1):
        visible = visible and this_tree_height > grid[r][col]
        if not visible:
            break

    if visible:
        return True

    # Then we'll look down (larger row index)
    visible = True
    for r in range(row + 1, num_rows):
        visible = visible and this_tree_height > grid[r][col]
        if not visible:
            break

    return visible


def part1():
    with open('./input.txt', 'r') as f:
        all_rows_str = f.readlines()
    
    all_rows_str = [r.strip() for r in all_rows_str]
    all_rows = [ [int(l) for l in r] for r in all_rows_str ]
    
    num_rows = len(all_rows)
    num_cols = len(all_rows[0])

    num_visible = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if is_visible(all_rows, r, c):
                num_visible = num_visible + 1
    
    print(f'{num_visible} trees are visible')


def calc_score(grid, row, col):
    num_rows = len(grid)
    num_cols = len(grid[0])
    this_tree_height = grid[row][col]

    # First we'll look left (smaller column index)
    visible_left = 0
    for c in range(col - 1, -1, -1):
        visible_left = visible_left + 1
        if this_tree_height <= grid[row][c]:
            break
    
    # Then we'll look right (larger column index)
    visible_right = 0
    for c in range(col + 1, num_cols):
        visible_right = visible_right + 1
        if this_tree_height <= grid[row][c]:
            break

    # Then we'll look up (smaller row index)
    visible_up = 0
    for r in range(row - 1, -1, -1):
        visible_up = visible_up + 1
        if this_tree_height <= grid[r][col]:
            break

    # Then we'll look down (larger row index)
    visible_down = 0
    for r in range(row + 1, num_rows):
        visible_down = visible_down + 1
        if this_tree_height <= grid[r][col]:
            break

    return visible_left * visible_right * visible_up * visible_down


def part2():
    with open('./input.txt', 'r') as f:
        all_rows_str = f.readlines()
    
    all_rows_str = [r.strip() for r in all_rows_str]
    all_rows = [ [int(l) for l in r] for r in all_rows_str ]
    
    num_rows = len(all_rows)
    num_cols = len(all_rows[0])

    max_score = 0
    all_scores = {}
    # Note: skip all the edge trees... they have a score of zero
    for r in range(1, num_rows - 1):
        for c in range(1, num_cols - 1):
            score = calc_score(all_rows, r, c)
            all_scores[(r, c)] = score
            if score > max_score:
                max_score = score
    
    print(f'Max scenery score is {max_score}')

    for coord in all_scores:
        if all_scores[coord] == max_score:
            print(coord)
            calc_score(all_rows, coord[0], coord[1])


if __name__ == '__main__':
    part1()
    part2()
