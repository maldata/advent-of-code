#!/usr/bin/env python3

def read_course():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    stripped_lines = [line.strip() for line in all_lines]
    split_lines = [line.split() for line in stripped_lines]
    return [(s[0].lower(), int(s[1])) for s in split_lines]


def solve_a(moves):
    horizontal_pos = 0
    depth = 0

    for move in moves:
        direction = move[0]
        quantity = move[1]

        if direction == 'forward':
            horizontal_pos = horizontal_pos + quantity
        elif direction == 'down':
            depth = depth + quantity
        elif direction == 'up':
            depth = depth - quantity
        else:
            print("I don't know what to do with '{0}'".format(direction))
    
    print('Final horizontal position and depth: {0} and {1}.'.format(horizontal_pos, depth))
    print('Product of horizontal position and depth: {0}'.format(horizontal_pos * depth))

    
def solve_b(moves):
    horizontal_pos = 0
    depth = 0
    aim = 0

    for move in moves:
        direction = move[0]
        quantity = move[1]

        if direction == 'forward':
            horizontal_pos = horizontal_pos + quantity
            depth = depth + aim * quantity
        elif direction == 'down':
            aim = aim + quantity
        elif direction == 'up':
            aim = aim - quantity
        else:
            print("I don't know what to do with '{0}'".format(direction))
    
    print('Final horizontal position and depth: {0} and {1}.'.format(horizontal_pos, depth))
    print('Product of horizontal position and depth: {0}'.format(horizontal_pos * depth))

    
if __name__ == '__main__':
    moves = read_course()
    solve_a(moves)
    solve_b(moves)
