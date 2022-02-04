import re


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    player_positions = {}
    for line in all_lines:
        m = re.match('Player ([0-9]+) starting position: ([0-9]+)', line)
        if m:
            player_positions[m.group(1)] = m.group(2)

    return int(player_positions['1']), int(player_positions['2'])


def deterministic_die100():
    current = 1
    while True:
        yield current
        current = current + 1
        if current > 100:
            current = 1


def solve_a(positions):
    num_players = len(positions)
    scores = [0] * num_players
    current_player_index = 0
    rolls_per_turn = 3
    total_rolls = 0
    num_spaces = 10
    gen = deterministic_die100()
    while True:
        dice = [next(gen) for i in range(rolls_per_turn)]
        total_rolls = total_rolls + rolls_per_turn
        spaces_moved = sum(dice)
        p = positions[current_player_index]
        new_p = (((p - 1) + spaces_moved) % num_spaces) + 1
        positions[current_player_index] = new_p
        scores[current_player_index] = scores[current_player_index] + new_p

        if scores[current_player_index] >= 1000:
            winner_index = current_player_index
            loser_index = (current_player_index + 1) % num_players
            break

        current_player_index = (current_player_index + 1) % num_players

    loser_score = scores[loser_index]
    return loser_score * total_rolls


def main():
    player1_pos, player2_pos = read_input('./input.txt')
    result = solve_a([player1_pos, player2_pos])
    print('Result is {0}'.format(result))


if __name__ == '__main__':
    main()
