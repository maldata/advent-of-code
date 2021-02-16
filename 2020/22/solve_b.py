#!/usr/bin/env python3
from game import Game


def read_deck(file_name):
    with open(file_name, 'r') as f:
        all_lines = f.readlines()

    return [int(line.strip()) for line in all_lines]


def main():
    deck1 = read_deck('./player1.txt')
    deck2 = read_deck('./player2.txt')

    main_game = Game(deck1, deck2)
    main_game.play()
    scores = main_game.get_scores()
    winner_index = main_game.get_winner_index()
    
    print('Winning deck at the end: {0}'.format(winner_index))
    print('Score: {0}'.format(scores[winner_index]))
    main_game.print_decks()

if __name__ == '__main__':
    main()
