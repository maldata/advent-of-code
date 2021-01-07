#!/usr/bin/env python3
import re
from tile import Tile
from image import Image


def rotate_image(image_lines):
    rotated = []
    for i in range(len(image_lines)):
        new_line = ''.join([line[i] for line in image_lines])
        rotated.append(new_line[::-1])

    return rotated


def flip_image(image_lines):
    return [line[::-1] for line in image_lines]


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

    print('Laying out tiles...')
    image = Image(tiles)
    image.place_tiles()

    print('Finished assembling the image. Rendering...')
    rendered_image = image.render()

    side_length = len(rendered_image)
    print('Image is {0} x {0}'.format(side_length))

    sea_monster = ['                  # ',
                   '#    ##    ##    ###',
                   ' #  #  #  #  #  #   ']
    sea_monster = [s.replace(' ', '.') for s in sea_monster]
    
    sea_monster_len = len(sea_monster[0])

    # Construct the regex for finding sea monsters
    num_padding_chars = side_length - sea_monster_len
    padding = '.' * num_padding_chars
    sea_monster_regex = padding.join(sea_monster)
    sea_monster_num_hashes = sea_monster_regex.count('#')

    # Rotate the image and count the sea monsters in each orientation
    for orientation in range(8):
        num_monsters = 0
        if orientation == 4:
            rendered_image = flip_image(rendered_image)
            
        flattened_image = ''.join(rendered_image)
        r = re.findall(sea_monster_regex, flattened_image)
        num_monsters = len(r)

        if num_monsters != 0:
            break
        
        rendered_image = rotate_image(rendered_image)

    print('Found {0} sea monsters!'.format(num_monsters))

    image_num_hashes = flattened_image.count('#')
    print('There are {0} hashes in the image'.format(image_num_hashes))
    sea_roughness = image_num_hashes - (num_monsters * sea_monster_num_hashes)

    print('Sea roughness: {0}'.format(sea_roughness))
        

if __name__ == '__main__':
    # main('./test-input1.txt')
    main('./input.txt')
