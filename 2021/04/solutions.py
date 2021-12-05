#!/usr/bin/env python3

class Space:
    def __init__(self, number):
        self._number = number
        self._checked = False
    
    @property
    def number(self):
        return self._number
    
    @property
    def checked(self):
        return self._checked
    
    def set_as_checked(self):
        self._checked = True


class Board:
    def __init__(self):
        self._text_rows = []
        self._num_rows = 0
        self._num_cols = 0
        self._spaces = {}

    def add_row(self, text_row):
        self._text_rows.append(text_row)

    def finish_processing(self):
        self._num_rows = len(self._text_rows)
        self._num_cols = len(self._text_rows[0].split())

        for i in range(self._num_rows):
            row = self._text_rows[i]
            row = row.split()

            for j in range(self._num_cols):
                number = int(row[j])
                s = Space(number)
                self._spaces[(j, i)] = s

    def add_number(self, number):
        for k in self._spaces:
            s = self._spaces[k]
            if s.number == number:
                s.set_as_checked()

    def check_for_win(self):
        return self.check_horizontals() or self.check_verticals()

    def all_checked(self, coords):
        for coord in coords:
            if not self._spaces[coord].checked:
                return False
        return True

    def check_horizontals(self):
        for r in range(self._num_rows):
            spaces_to_check = [(c, r) for c in range(self._num_cols)]
            if self.all_checked(spaces_to_check):
                return True
        return False

    def check_verticals(self):
        for c in range(self._num_cols):
            spaces_to_check = [(c, r) for r in range(self._num_rows)]
            if self.all_checked(spaces_to_check):
                return True
        return False

    def calculate_score(self, last_number_called):
        sum_of_unmarked = 0
        for k in self._spaces:
            s = self._spaces[k]
            if not s.checked:
                sum_of_unmarked = sum_of_unmarked + s.number

        return sum_of_unmarked * last_number_called


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    drawn_number_text = all_lines[0]
    board_text = all_lines[1:]

    drawn_numbers = [int(i) for i in drawn_number_text.split(',')]
    boards = []
    current_board = None
    current_board_rows = 0
    for line in board_text:
        l = line.strip()
        if len(l) == 0:
            current_board = None
            current_board_rows = 0
            continue

        if current_board is None:
            current_board = Board()

        current_board.add_row(l)
        current_board_rows = current_board_rows + 1

        if current_board_rows == 5:
            current_board.finish_processing()
            boards.append(current_board)
            current_board = None

    return (drawn_numbers, boards)


def solve_a(drawn_numbers, boards):
    for n in drawn_numbers:
        for b in boards:
            b.add_number(n)
            if b.check_for_win():
                score = b.calculate_score(n)
                print('Winning board score: {0}'.format(score))
                return

def main():
    drawn_numbers, boards = read_input('./input.txt')
    solve_a(drawn_numbers, boards)


if __name__ == '__main__':
    main()
