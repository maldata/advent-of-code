#!/usr/bin/env python3

def left_rotate_once(ring_list):
    return ring_list[1:] + [ring_list[0]]
    

def rotate_to_zero(ring_list, start_index):
    for i in range(start_index):
        ring_list = left_rotate_once(ring_list)

    return ring_list


def do_one_move(ring_list, start_index, lowest_num, highest_num):
    # First, let's rotate the list so the current cup is index 0
    ring_list = rotate_to_zero(ring_list, start_index)
    start_index = 0

    # The crab picks up the three cups that are immediately clockwise of the
    # current cup. They are removed from the circle; cup spacing is adjusted
    # as necessary to maintain the circle.
    removed_cups = ring_list[1:4]
    ring_list = [ring_list[0]] + ring_list[4:]

    # The crab selects a destination cup: the cup with a label equal to the
    # current cup's label minus one...
    destination_cup = ring_list[0] - 1

    # If this would select one of the cups that was just picked up, the
    # crab will keep subtracting one until it finds a cup that wasn't
    # just picked up.
    while True:
        # If at any point in this process the value goes
        # below the lowest value on any cup's label, it wraps
        # around to the highest value on any cup's label instead.
        if destination_cup < lowest_num:
            destination_cup = highest_num

        if destination_cup not in removed_cups:
            break

        destination_cup = destination_cup - 1

    # The crab places the cups it just picked up so that they are immediately
    # clockwise of the destination cup. They keep the same order as when they
    # were picked up.
    destination_index = ring_list.index(destination_cup)
    pre = ring_list[0:destination_index + 1]
    post = ring_list[destination_index + 1:]
    ring_list = pre + removed_cups + post
    
    # The crab selects a new current cup: the cup which is immediately
    # clockwise of the current cup.
    return ring_list, start_index + 1

def main():
    # cup_ring = [3, 6, 4, 2, 9, 7, 5, 8, 1]
    cup_ring = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    current_idx = 0

    max_label = 1000000
    cup_ring = cup_ring + list(range(10, max_label + 1))
    
    num_moves = 100
    for i in range(num_moves):
        cup_ring, current_idx = do_one_move(cup_ring, current_idx, 1, max_label)

    # print(cup_ring)

    # Find the 1 and rotate it to the front
    one_index = cup_ring.index(1)
    next1 = one_index + 1
    next2 = next1 + 1
    print('{0} * {1} = {2}'.format(cup_ring[next1], cup_ring[next2], cup_ring[next1] * cup_ring[next2]))
    
    
if __name__ == '__main__':
    main()
