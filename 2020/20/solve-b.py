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


def highlight_sea_monster(flat_img, sea_monster_regex, start_idx):
    exploded_monster = [i for i in sea_monster_regex]
    hash_offsets = [i for (i, j) in enumerate(exploded_monster) if j == '#']
    
    exploded_img = [i for i in flat_img]

    for offset in hash_offsets:
        exploded_img[offset + start_idx] = 'O'

    return ''.join(exploded_img)


def print_flattened_image(flat_img, side_length):
    for line_num in range(side_length):
        start_idx = line_num * side_length
        print(flat_img[start_idx:start_idx + side_length])


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

    # Rotate/flip the image until we find one sea monster
    for orientation in range(8):
        if orientation == 4:
            rendered_image = flip_image(rendered_image)
            
        flattened_image = ''.join(rendered_image)
        r = re.findall(sea_monster_regex, flattened_image)
        if r:
            break
        
        rendered_image = rotate_image(rendered_image)

    print('The image is now correctly oriented.')

    num_monsters = 0
    while True:
        r = re.search(sea_monster_regex, flattened_image)
        if r is None:
            break
        
        span = r.span()
        span_start = span[0]
        span_end = span[1]
        num_monsters = num_monsters + 1
        flattened_image = highlight_sea_monster(flattened_image, sea_monster_regex, span_start)

    print_flattened_image(flattened_image, side_length)
    sea_roughness = flattened_image.count('#')
    print('Sea monsters: {0}'.format(num_monsters))
    print('Sea roughness: {0}'.format(sea_roughness))
        

if __name__ == '__main__':
    # main('./test-input1.txt')
    main('./input.txt')
