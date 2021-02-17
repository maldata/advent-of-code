#!/usr/bin/env python3
import pdb

class Game:
    def __init__(self, deck0, deck1):
        self._deck0 = list(deck0)
        self._deck1 = list(deck1)
        self._history = []

    def print_decks(self):
        print(self._deck0)
        print(self._deck1)
        
    def game_finished(self):
        return len(self._deck0) == 0 or len(self._deck1) == 0

    def get_winner_index(self):
        if self.game_finished():
            return 0 if len(self._deck0) > 0 else 1
        else:
            return None
        
    def get_scores(self):
        scores = []
        for deck in [self._deck0, self._deck1]:
            points_per_card = list(range(1, len(deck) + 1))
            points_per_card.reverse()
            z = zip(deck, points_per_card)
            score = sum([a * b for a, b in z])
            scores.append(score)
        
        return scores
    
    def play(self):
        """
        Given the current deck state, iterate until the game ends,
        then return the index of the winner.
        """
        while not self.game_finished():
            deck_state = (list(self._deck0), list(self._deck1))
            if deck_state in self._history:
                return 0
            
            self._history.append(deck_state)
            
            round_winner = self.get_round_winner()

            p0 = self._deck0[0]
            p1 = self._deck1[0]
            
            if round_winner == 0:
                self._deck0 = self._deck0[1:] + [p0, p1]
                self._deck1 = self._deck1[1:]
            elif round_winner == 1:
                self._deck0 = self._deck0[1:]
                self._deck1 = self._deck1[1:] + [p1, p0]
            else:
                print('The winner of a round was None!!!')
                break

        return self.get_winner_index()

    def get_round_winner(self):
        """
        Determine the winner of one round. That is, draw a card from each
        deck and do a recursive subgame or determine the winner based on
        the drawn card. This method returns the index of the winner but
        does not remove a card from the front of each deck or put cards
        into the winner's deck.
        """
        p0 = self._deck0[0]
        p1 = self._deck1[0]
        
        remaining0 = len(self._deck0) - 1
        remaining1 = len(self._deck1) - 1
        
        if p0 <= remaining0 and p1 <= remaining1:
            sub_deck0 = list(self._deck0[1:p0 + 1])
            sub_deck1 = list(self._deck1[1:p1 + 1])
            subgame = Game(sub_deck0, sub_deck1)
            winner_index = subgame.play()
        else:
            if p0 > p1:
                winner_index = 0
            elif p0 < p1:
                winner_index = 1
            else:
                print("I don't know how to manage a tie!!!")
                winner_index = None
                
        return winner_index
