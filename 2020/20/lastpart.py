#!/usr/bin/env python3
import re


def rotate(image_lines):
    rotated = []
    for i in range(len(image_lines)):
        new_line = ''.join([line[i] for line in image_lines])
        rotated.append(new_line[::-1])

    return rotated


def flip(image_lines):
    return [line[::-1] for line in image_lines]


def highlight_sea_monster(flat_img, offsets, start_idx):
    exploded = [i for i in flat_img]

    for offset in offsets:
        exploded[offset + start_idx] = 'O'

    return ''.join(exploded)


def print_flattened_image(flat_img, side_length):
    for line_num in range(side_length):
        start_idx = line_num * side_length
        print(flat_img[start_idx:start_idx + side_length])


def main():
    with open('rendered-image.txt', 'r') as f:
        all_lines = f.readlines()

    image = [line.strip() for line in all_lines]

    side_length = len(image)
    print('Image is {0}x{0}'.format(side_length))

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
    
    exploded = [i for i in sea_monster_regex]
    hash_offsets = [i for (i, j) in enumerate(exploded) if j == '#']
    
    # Rotate the image and count the sea monsters in each orientation
    for orientation in range(8):
        if orientation == 4:
            image = flip(image)
            
        flattened_image = ''.join(image)
        r = re.search(sea_monster_regex, flattened_image)

        if r:
            break
        
        image = rotate(image)

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
        flattened_image = highlight_sea_monster(flattened_image, hash_offsets, span_start)

    print_flattened_image(flattened_image, side_length)
    sea_roughness = flattened_image.count('#')
    print('Sea monsters: {0}'.format(num_monsters))
    print('Sea roughness: {0}'.format(sea_roughness))
        
    
if __name__ == '__main__':
    main()
