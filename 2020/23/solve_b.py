#!/usr/bin/env python3
def do_one_move(next_cup, current_cup, lowest_num, highest_num):
    # The crab picks up the three cups that are immediately clockwise of the
    # current cup. They are removed from the circle; cup spacing is adjusted
    # as necessary to maintain the circle.
    cw1 = next_cup[current_cup]
    cw2 = next_cup[cw1]
    cw3 = next_cup[cw2]

    next_cup[current_cup] = next_cup[cw3]

    # The crab selects a destination cup: the cup with a label equal to the
    # current cup's label minus one...
    destination_cup = current_cup - 1
    if destination_cup < lowest_num:
        destination_cup = highest_num

    # If this would select one of the cups that was just picked up, the
    # crab will keep subtracting one until it finds a cup that wasn't
    # just picked up.
    while destination_cup in [cw1, cw2, cw3]:
        destination_cup = destination_cup - 1
        
        # If at any point in this process the value goes
        # below the lowest value on any cup's label, it wraps
        # around to the highest value on any cup's label instead.
        if destination_cup < lowest_num:
            destination_cup = highest_num

    # The crab places the cups it just picked up so that they are immediately
    # clockwise of the destination cup. They keep the same order as when they
    # were picked up.
    cw4 = next_cup[destination_cup]
    next_cup[destination_cup] = cw1
    #next_cup[cw1] = cw2
    #next_cup[cw2] = cw3
    next_cup[cw3] = cw4
    
    return next_cup, next_cup[current_cup]

def main():
    max_label = 1000000
    cup_ring = [3, 6, 4, 2, 9, 7, 5, 8, 1] + list(range(10, max_label + 1))

    # If we do list operations, this is painfully slow. Like... days? Weeks?
    # We're cutting out chunks of the list, and we're looking up locations.
    # Turns out we get a huge speed boost by faking a linked-list with a dict.
    # So, next_cup will be a dictionary where the key is the cup label, and the
    # value is the label of the cup clockwise from it.
    next_cup = {}
    for idx in range(1, len(cup_ring)):
        cup1 = cup_ring[idx - 1]
        cup2 = cup_ring[idx]
        next_cup[cup1] = cup2

    # Close the loop
    next_cup[max_label] = cup_ring[0]

    current_cup = cup_ring[0]    
    num_moves = 10000000
    for i in range(num_moves):
        next_cup, current_cup = do_one_move(next_cup, current_cup, 1, max_label)

    cw1 = next_cup[1]
    cw2 = next_cup[cw1]

    print('{0} * {1} = {2}'.format(cw1, cw2, cw1 * cw2))
    
if __name__ == '__main__':
    main()
