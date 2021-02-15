#!/usr/bin/env python3

def read_deck(file_name):
    with open(file_name, 'r') as f:
        all_lines = f.readlines()

    return [int(line.strip()) for line in all_lines]
    

def calculate_score(deck):
    points_per_card = list(range(1, len(deck) + 1))
    points_per_card.reverse()
    z = zip(deck, points_per_card)
    return sum([a * b for a, b in z])


def find_winner(deck1, deck2):
    game_history = []
    # TODO: check that the decks aren't in the history
    # return recursive_short = True. Need to propagate up to the top level.

    p1 = deck1[0]
    p2 = deck2[0]

    remaining1 = len(deck1) - 1
    remaining2 = len(deck2) - 1

    if p1 <= remaining1 and p2 <= remaining2:
        new_deck1 = list(deck1[1:remaining1 + 1])
        new_deck2 = list(deck2[1:remaining2 + 1])
        winner_index = find_winner(new_deck1, new_deck2)
    else:
        if p1 > p2:
            winner_index = 0
        elif p1 < p2:
            winner_index = 1
        else:
            print("I don't know how to manage a tie!!!")
            winner_index = None
        
    return winner_index
    

def iterate_decks(winner_index, deck1, deck2):
    if winner_index == 0:
        new_deck1 = deck1[1:] + [deck1[0], deck2[0]]
        new_deck2 = deck2[1:]
    else:
        new_deck1 = deck1[1:]
        new_deck2 = deck2[1:] + [deck2[0], deck1[0]]

    return new_deck1, new_deck2


def main():
    deck1 = read_deck('./player1.txt')
    deck2 = read_deck('./player2.txt')

    while len(deck1) > 0 and len(deck2) > 0:
        winner_index = find_winner(deck1, deck2)
        if winner_index is None:
            winner_index = 0
            break
        
        deck1, deck2 = iterate_decks(winner_index, deck1, deck2)

    winner = (deck1, deck2)[winner_index]    
    score = calculate_score(winner)
    print('Winning deck at the end: {0}'.format(winner))
    print('Score: {0}'.format(score))

if __name__ == '__main__':
    main()
