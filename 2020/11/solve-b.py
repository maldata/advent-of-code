#!/usr/bin/env python3
def get_changed(seat_map, new_seat_map):
    num_rows = len(seat_map)
    num_cols = len(seat_map[0])
    changed = 0
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            if seat_map[row_idx][col_idx] != new_seat_map[row_idx][col_idx]:
                changed = changed + 1

    return changed


def get_occupied(seat_map):
    num_rows = len(seat_map)
    num_cols = len(seat_map[0])
    occupied = 0
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            if seat_map[row_idx][col_idx] == '#':
                occupied = occupied + 1

    return occupied


def get_num_visible_occupied_seats(seat_map, row_idx, col_idx):
    """
    Step in each of the eight directions until you hit the first non-floor square or the edge.
    If we hit an occupied seat, it's visible. Count it!
    """
    num_rows = len(seat_map)
    num_cols = len(seat_map[0])

    occupied = 0
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in deltas:
        steps = 1
        c = col_idx + steps * dx
        r = row_idx + steps * dy
        while 0 <= r < num_rows and 0 <= c < num_cols:
            if seat_map[r][c] == '#':
                occupied = occupied + 1
                break
            elif seat_map[r][c] == 'L':
                break
            steps = steps + 1
            c = col_idx + steps * dx
            r = row_idx + steps * dy

    return occupied


def evaluate_seat(seat_map, row_idx, col_idx):
    if seat_map[row_idx][col_idx] == '.':
        # If it's floor, it stays floor
        return '.'
    elif seat_map[row_idx][col_idx] == 'L':
        # If it's an empty seat and none of the surrounding 8
        # squares is an occupied seat, it becomes occupied.
        if get_num_visible_occupied_seats(seat_map, row_idx, col_idx) == 0:
            return '#'
        else:
            return 'L'
    elif seat_map[row_idx][col_idx] == '#':
        # If it's an occupied seat and 5 or more adjacent
        # squares are also occupied, it becomes empty.
        if get_num_visible_occupied_seats(seat_map, row_idx, col_idx) >= 5:
            return 'L'
        else:
            return '#'
    else:
        # Anything else is an error
        print('"{0}" is not a valid character'.format(seat_map[row_idx][col_idx]))
        return None

    
def iterate(seat_map):
    num_rows = len(seat_map)
    num_cols = len(seat_map[0])
    
    # Initialize a new map. Every square is floor by default
    new_map = [['.' for _ in range(num_cols)] for _ in range(num_rows)]

    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            new_map[row_idx][col_idx] = evaluate_seat(seat_map, row_idx, col_idx)
    
    return new_map


def main():
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()

    rows = [line.strip() for line in all_lines]
    rows = [[i for i in r] for r in rows]
    num_cols_all = [len(r) for r in rows]
    num_cols = num_cols_all[0]

    if not all([c == num_cols for c in num_cols_all]):
        print('Problem reading the input')
        return

    num_occupied = 0
    keep_going = True
    while keep_going:
        new_rows = iterate(rows)
        num_changed = get_changed(rows, new_rows)
        num_occupied = get_occupied(new_rows)
        rows = new_rows

        if num_changed == 0:
            keep_going = False

    print('At steady-state, there are {0} occupied seats.'.format(num_occupied))
    
    
if __name__ == '__main__':
    main()
