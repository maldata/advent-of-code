#!/usr/bin/env python3
import re
from tile import Tile
from image import Image


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
