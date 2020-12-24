#!/usr/bin/env python3
import re


class Image:
    def __init__(self, tiles):
        self.tiles = tiles
        self.placed_tiles = {}

    def place_tiles(self):
        """
        The tiles are all tagged with the number of borders that match another tile.
        The center ones have 4 shared borders, the corners have 2, the ones along the
        edge have 3.
        """
        # A big-ass dictionary that maps border strings to tile IDs
        all_edges = {}

        centers = []
        sides = []
        corners = []
        for tile_id in self.tiles:
            t = self.tiles[tile_id]
            if t.border_matches == 4:
                centers.append(tile_id)
            elif t.border_matches == 3:
                sides.append(tile_id)
            else:
                corners.append(tile_id)

            for border_edge in t.border:
                if border_edge in all_edges:
                    all_edges[border_edge].append(tile_id)
                    all_edges[border_edge[::-1]].append(tile_id)
                else:
                    all_edges[border_edge] = [tile_id]
                    all_edges[border_edge[::-1]] = [tile_id]

        # Pick a corner tile arbitrarily. Orient it to sit in the top left corner. That is,
        # the edge strings that only exist on this tile are on top & left.
        arbitrary_corner_id = corners[0]
        arbitrary_corner = self.tiles[arbitrary_corner_id]
        while True:
            if len(all_edges[arbitrary_corner.border[0]]) == 1 and len(all_edges[arbitrary_corner.border[3]]) == 1:
                break
            else:
                arbitrary_corner.rotate(1)

        # i will be our row index, j will be our column index. So we go left to right, top to bottom.
        square_size = 12
        for i in range(square_size):
            for j in range(square_size):
                if i == 0 and j == 0:
                    # We already got this one set up correctly, so just set it
                    self.placed_tiles[(i, j)] = arbitrary_corner_id
                elif j == 0:
                    # If it's the first tile in a row (other than (0, 0)), use the one above
                    # it to identify the tile, then orient to match the tile above
                    tile_above_id = self.placed_tiles[(i - 1, j)]
                    tile_above = self.tiles[tile_above_id]
                    target_border_str = tile_above.border[2]  # bottom string of above tile
                    target_tile_ids = all_edges[target_border_str]
                    target_tile_id = filter(lambda x: x != tile_above_id, target_tile_ids)
                    target_tile_id = list(target_tile_id)[0]
                    target_tile = self.tiles[target_tile_id]

                    # Orient it so the edge that doesn't match anything is on the left
                    while True:
                        if len(all_edges[target_tile.border[3]]) == 1:
                            break
                        else:
                            target_tile.rotate(1)

                    # Now you still might need to flip it, if the top edge of the new tile
                    # is backward relative to the tile above. If so, we flip it along the
                    # vertical axis, putting the outer edge on the inside, then rotate twice.
                    if target_border_str != target_tile.border[0]:
                        target_tile.flip()
                        target_tile.rotate(2)

                    self.placed_tiles[(i, j)] = target_tile_id
                else:
                    # For everything else, align it with the one on the left
                    left_tile_id = self.placed_tiles[(i, j - 1)]
                    left_tile = self.tiles[left_tile_id]
                    target_border_str = left_tile.border[1]  # right string of left tile
                    target_tile_ids = all_edges[target_border_str]
                    target_tile_id = filter(lambda x: x != left_tile_id, target_tile_ids)
                    target_tile_id = list(target_tile_id)[0]
                    target_tile = self.tiles[target_tile_id]

                    # Orient it so the target_border_str is on the left
                    while True:
                        if target_tile.border[3] == target_border_str:
                            break
                        elif target_tile.border[3][::-1] == target_border_str:
                            target_tile.flip()
                            target_tile.rotate(2)
                            break
                        else:
                            target_tile.rotate(1)

                    self.placed_tiles[(i, j)] = target_tile_id

        deleteme = self.tiles['3373']
        pass

    def print_with_borders(self):
        square_size = 12
        num_lines = 10
        for i in range(square_size):
            for k in range(num_lines):
                full_line = ''
                for j in range(square_size):
                    tile_id = self.placed_tiles[(i, j)]
                    tile = self.tiles[tile_id]
                    full_line = full_line + tile.lines[k]
                print(full_line)


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

        # TODO: extract from lines instead
        # After we rotate, reverse the order of the new top & bottom strings
        self.border[0] = self.border[0][::-1]
        self.border[2] = self.border[2][::-1]

        new_lines = []
        for i in range(len(self.lines)):
            new_line = ''.join([line[i] for line in self.lines])
            new_lines.append(new_line[::-1])
        self.lines = new_lines

    def flip(self):
        """
        Flip along the vertical axis. Keep border strings 0 & 2 where they are
        in the array, but swap 1 & 3. Then, reverse strings 0 & 2.
        """
        # TODO: extract from lines instead
        temp = self.border[1]
        self.border[1] = self.border[3]
        self.border[3] = temp
        self.border[0] = self.border[0][::-1]
        self.border[2] = self.border[2][::-1]

        self.lines = [line[::-1] for line in self.lines]

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
    print('Reading data...')
    with open(tile_file, 'r') as f:
        all_lines = f.readlines()

    all_lines = [line.strip() for line in all_lines]
    filtered = filter(lambda line: line != '', all_lines)
    all_lines = list(filtered)

    print('Creating tiles...')
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

    print("Populating each tile's number of shared borders...")
    populate_num_shared_borders(tiles)

    print('Laying out tiles...')
    image = Image(tiles)
    image.place_tiles()

    print('Printing the full image...')
    print()
    print()
    image.print_with_borders()


if __name__ == '__main__':
    # main('./test-input1.txt')
    main('./input.txt')
