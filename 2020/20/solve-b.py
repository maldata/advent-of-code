#!/usr/bin/env python3
import re


class Tile:
    def __init__(self, tile_id, lines):
        self.id = tile_id
        self.lines = lines

        # border is a list of 4 strings (top, right, bottom, left). We don't
        # much care about the innards, just lining up the borders. When we
        # rotate it, we'll shift them. The border strings are always interpreted
        # as being read from left to right or from top to bottom.
        top = self.lines[0]
        bottom = self.lines[-1]
        left = ''.join([i[0] for i in self.lines])
        right = ''.join([i[-1] for i in self.lines])
        self.border = [top, right, bottom, left]
        self.border_matches = 0

    def rotate(self, num_rotations):
        """
        Rotate the tile by 90 degrees (one shift of the border list) per rotation.
        Note that during a rotation, we need to reverse some strings in order to
        preserve the left-to-right & top-to-bottom interpretations.
        """
        for i in range(num_rotations):
            self.border = [self.border[-1]] + self.border[0:-1]

        # After we rotate, reverse the order of the new top & bottom strings
        self.border[0] = self.border[0][::-1]
        self.border[2] = self.border[2][::-1]

    def flip(self):
        """
        Flip along the vertical axis. Keep border strings 0 & 2 where they are
        in the array, but swap 1 & 3. Then, reverse strings 0 & 2.
        """
        temp = self.border[1]
        self.border[1] = self.border[3]
        self.border[3] = temp
        self.border[0] = self.border[0][::-1]
        self.border[2] = self.border[2][::-1]

    def num_shared_borders(self, other_tile):
        # I guess we'll just assume we put the other tile to the right of this one,
        # rotate four times, flip, and rotate 4 times again.
        for ro in range(4):
            for r in range(4):
                if self.border[1] == other_tile.border[3]:
                    self.border_matches = self.border_matches + 1
                self.rotate(1)

            self.flip()

            for r in range(4):
                if self.border[1] == other_tile.border[3]:
                    self.border_matches = self.border_matches + 1
                self.rotate(1)

            # Rotate the other one, but don't flip it (only need to flip one of the two)
            other_tile.rotate(1)


def populate_num_shared_borders(tiles):
    all_tile_ids = list(tiles)
    num_shifts = 0
    while num_shifts < len(all_tile_ids):
        target_tile_id = all_tile_ids[0]
        target_tile = tiles[target_tile_id]

        comparison_tile_ids = all_tile_ids[1:]
        for ct in comparison_tile_ids:
            comp_tile = tiles[ct]
            target_tile.num_shared_borders(comp_tile)

        all_tile_ids = all_tile_ids[1:] + [all_tile_ids[0]]
        num_shifts = num_shifts + 1


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

    populate_num_shared_borders(tiles)

    corner_tiles = []
    product = 1
    for tile_id in tiles:
        tile = tiles[tile_id]
        if tile.border_matches == 2:
            corner_tiles.append(tile_id)
            product = product * int(tile_id)

    print('Corner tiles: {0}. Product: {1}'.format(corner_tiles, product))


if __name__ == '__main__':
    # main('./test-input1.txt')
    main('./input.txt')
