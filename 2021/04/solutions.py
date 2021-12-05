#!/usr/bin/env python3

class Space:
    def __init__(self, number):
        self._number = number
        self._checked = False


class Board:
    def __init__(self, text_lines):
        pass

    def add_number(self, number):
        pass

    def check_for_win(self):
        return self.check_horizontals() or self.check_verticals()

    def check_horizontals(self):
        return False

    def check_verticals(self):
        return False


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    drawn_number_text = all_lines[0]
    board_text = all_lines[1:]

    drawn_numbers = [int(i) for i in drawn_number_text.split(',')]
    boards = []
    return (drawn_numbers, boards)


def main():
    drawn_numbers, boards = read_input('./input.txt')
    print(drawn_numbers)


if __name__ == '__main__':
    main()
