#!/usr/bin/env python3

class Game:
    def __init__(self, deck0, deck1):
        self._initial_deck0 = list(deck0)
        self._initial_deck1 = list(deck1)
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
            return 0 if len(self._deck1) > 0 else 1
        else:
            return None
    
    def get_scores(self):
        # TODO: get the scores based on the current decks
        return (0, 0)
    
    def play(self):        
        while not self.game_finished():
            # TODO: if the current decks are in the history, return 0.
            round_winner = self.do_one_round()

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

        return 0 if len(self._deck1) == 0 else 1

    def do_one_round(self):
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
    
