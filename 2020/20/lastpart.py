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
    sea_monster_regex = sea_monster[0] + padding + sea_monster[1] + padding + sea_monster[2]
    sea_monster_num_hashes = sea_monster_regex.count('#')

    # Rotate the image and count the sea monsters in each orientation
    for orientation in range(8):
        num_monsters = 0
        if orientation == 4:
            image = flip(image)
            
        flattened_image = ''.join(image)
        r = re.findall(sea_monster_regex, flattened_image)
        num_monsters = len(r)

        if num_monsters != 0:
            break
        
        image = rotate(image)

    print('Found {0} sea monsters!'.format(num_monsters))

    image_num_hashes = flattened_image.count('#')
    sea_roughness = image_num_hashes - (num_monsters * sea_monster_num_hashes)

    print('Sea roughness: {0}'.format(sea_roughness))
        
    
if __name__ == '__main__':
    main()
