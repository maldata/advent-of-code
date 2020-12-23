#!/usr/bin/env python3
import re


class Tile:
    def __init__(self, tile_id, lines):
        self.id = tile_id
        self.lines = lines

        # border is a list of 4 strings (top, right, bottom, left). We don't
        # much care about the innards, just lining up the borders. When we
        # rotate it, we'll shift them.
        top = self.lines[0]
        bottom = self.lines[-1]
        left = ''.join([i[0] for i in self.lines])
        right = ''.join([i[-1] for i in self.lines])
        self.border = [top, right, bottom, left]

    def rotate(self, num_rotations):
        """
        Rotate the tile by 90 degrees (one shift of the border list) per rotation
        """
        for i in range(num_rotations):
            self.border = [self.border[-1]] + self.border[0:-1]

    def shared_border(self, other_tile):
        for b in self.border:
            if b in other_tile.border:
                return b


def get_corner_tiles(tiles):
    all_tile_ids = list(tiles)
    corner_tile_ids = []
    while len(corner_tile_ids) < 4:
        target_tile_id = all_tile_ids[0]
        target_tile = tiles[target_tile_id]

        num_borders = 0
        comparison_tile_ids = all_tile_ids[1:]
        for ct in comparison_tile_ids:
            comp_tile = tiles[ct]
            if target_tile.shared_border(comp_tile) is not None:
                num_borders = num_borders + 1

        # If we found a corner piece, hold onto its ID.
        # Either way, shift it to the end of the list.
        if num_borders == 2:
            corner_tile_ids.append(target_tile_id)

        all_tile_ids = all_tile_ids[1:] + [all_tile_ids[0]]

    return corner_tile_ids


def main(tile_file):
    with open(tile_file, 'r') as f:
        all_lines = f.readlines()

    all_lines = [line.strip() for line in all_lines]
    filtered = filter(lambda line: line != '', all_lines)
    all_lines = list(filtered)

    tiles = {}
    lines_per_tile = 11
    for i in range(len(all_lines) // lines_per_tile):
        start = i * lines_per_tile
        end = (i + 1) * lines_per_tile
        tile_lines = all_lines[start:end]
        header = tile_lines[0]
        m = re.match('^Tile ([0-9]+):$', header)
        if m:
            tile_id = m.group(1)
            body = tile_lines[1:]
            tiles[tile_id] = Tile(tile_id, body)

    corner_tiles = get_corner_tiles(tiles)
    product = 1
    for corner_id in corner_tiles:
        product = product * int(corner_id)

    print('Corner tiles: {0}. Product: {1}'.format(corner_tiles, product))


if __name__ == '__main__':
    main('./test-input1.txt')
