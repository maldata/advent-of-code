#!/usr/bin/env python3

# We will establish a coordinate system where we ignore the offset between
# odd & even rows. For example, consider the center tile A to be at (0,0).
# We can move west to F, east to C, northwest to G, northeast to B,
# southwest to E, or southeast to D.
#                                           Moves from a tile in an...
#        / \ / \        A - (0,0)           odd row            even row
#       | G | B |       B - (0,1)     NE -> dx=0,  dy=1        dx=1,  dy=1
#      / \ / \ / \      C - (1,0)     E  -> dx=1,  dy=0        dx=1,  dy=0
#     | F | A | C |     D - (0,-1)    SE -> dx=0,  dy=-1       dx=1,  dy=-1
#      \ / \ / \ /      E - (-1,-1)   SW -> dx=-1, dy=-1       dx=0,  dy=-1
#       | E | D |       F - (-1,0)    W  -> dx=-1, dy=0        dx=-1, dy=0
#        \ / \ /        G - (-1,1)    NW -> dx=-1, dy=1        dx=0,  dy=1
#
# We'll say that, in the odd-numbered rows (like -1 and 1), tiles that are
# offset by half a tile in the positive x direction will share the same
# x-coordinate. So, tiles A, B, and D are all x=0. E, F, and G are all x=-1.

from enum import Enum


class Direction(Enum):
    NE=0
    E=1
    SE=2
    SW=3
    W=4
    NW=5
    

def parse_line(line):
    tokens = []
    enum_lookup = {
        'ne': Direction.NE,
        'e': Direction.E,
        'se': Direction.SE,
        'sw': Direction.SW,
        'w': Direction.W,
        'nw': Direction.NW
    }
    
    idx = 0
    while idx < len(line):
        if line[idx] == 'n' or line[idx] == 's':
            token_length = 2
        else:
            token_length = 1

        token = line[idx:idx + token_length]
        tokens.append(enum_lookup[token])
        idx = idx + token_length

    return tokens


def follow_path(start, path):
    even_row_delta = {
        Direction.NE: (0,1),
        Direction.E:  (1,0),
        Direction.SE: (0,-1),
        Direction.SW: (-1,-1),
        Direction.W:  (-1,0),
        Direction.NW: (-1,1)
    }
    
    odd_row_delta = {
        Direction.NE: (1,1),
        Direction.E:  (1,0),
        Direction.SE: (1,-1),
        Direction.SW: (0,-1),
        Direction.W:  (-1,0),
        Direction.NW: (0,1)
    }

    x = start[0]
    y = start[1]
    for step in path:
        # Get the right dictionary depending on whether it's an odd or even row
        if y % 2 == 0:
            deltas = even_row_delta
        else:
            deltas = odd_row_delta

        delta = deltas[step]
        x = x + delta[0]
        y = y + delta[1]

    return x, y


def get_num_adjacent_black_tiles(floor, tile):
    adjacent_tiles = [follow_path(tile, [dir]) for dir in Direction]
    num_black = 0

    for adj in adjacent_tiles:
        if adj in floor and floor[adj] == 'b':
            num_black = num_black + 1

    return num_black


def next_day(original_floor):
    # 1. Any black tile with zero or more than 2 black tiles
    #    immediately adjacent to it is flipped to white.
    # 2. Any white tile with exactly 2 black tiles immediately
    #    adjacent to it is flipped to black.

    new_floor = {}
    for tile in original_floor:
        num_adj_black = get_num_adjacent_black_tiles(original_floor, tile)
        if original_floor[tile] == 'b' and (num_adj_black == 0 or num_adj_black > 2):
            new_floor[tile] = 'w'
        elif original_floor[tile] == 'w' and num_adj_black == 2:
            new_floor[tile] = 'b'
        else:
            new_floor[tile] = original_floor[tile]

    return new_floor


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()
    lines = [line.strip() for line in all_lines]
    paths = [parse_line(line) for line in lines]
    
    # keys are x,y tuples (using our weird hex coordinates described above)
    # values are 'w' (white) by default, or 'b' (black)
    floor = {(0,0): 'w'}
    for path in paths:
        endpoint = follow_path((0,0), path)

        if endpoint in floor:
            current_color = floor[endpoint]
            if current_color == 'w':
                floor[endpoint] = 'b'
            else:
                floor[endpoint] = 'w'
        else:
            floor[endpoint] = 'b'

    # We now have the configuration on day 0.
    for _ in range(100):
        floor = next_day(floor)

    num_white = 0
    num_black = 0
    for tile in floor:
        if floor[tile] == 'w':
            num_white = num_white + 1
        else:
            num_black = num_black + 1
            
    print('{0} white + {1} black = {2} total'.format(num_white, num_black, num_white + num_black))

            
if __name__ == '__main__':
    main()
