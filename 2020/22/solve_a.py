#!/usr/bin/env python3

def read_deck(file_name):
    with open(file_name, 'r') as f:
        all_lines = f.readlines()

    return [int(line.strip()) for line in all_lines]


def play_one_round(deck1, deck2):
    p1 = deck1[0]
    p2 = deck2[0]

    if p1 > p2:
        new_deck1 = deck1[1:] + [p1, p2] 
        new_deck2 = deck2[1:]    
    elif p1 < p2:
        new_deck1 = deck1[1:]
        new_deck2 = deck2[1:] + [p2, p1]
    else:
        print('What do you do for a tie???')
        return None
    
    return new_deck1, new_deck2
    

def calculate_score(deck):
    points_per_card = list(range(1, len(deck) + 1))
    points_per_card.reverse()
    z = zip(deck, points_per_card)
    return sum([a * b for a, b in z])

    
def main():
    deck1 = read_deck('./player1.txt')
    deck2 = read_deck('./player2.txt')

    while len(deck1) > 0 and len(deck2) > 0:
        deck1, deck2 = play_one_round(deck1, deck2)
    
    if len(deck1) > 0:
        winner = deck1
    else:
        winner = deck2

    score = calculate_score(winner)
    print('Winning deck at the end: {0}'.format(winner))
    print('Score: {0}'.format(score))

if __name__ == '__main__':
    main()
