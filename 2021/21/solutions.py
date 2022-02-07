from asyncio import all_tasks
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
    print('Result is {0}'.format(loser_score * total_rolls))


def get_next_states_player(s, p):
    if p < 0 or p > 1:
        print('Bad player index {0}'.format(p))
        return
    
    moving_player = p
    static_player = 0 if p == 1 else 1
    moving_player_state = s[moving_player]
    static_player_state = s[static_player]

    possible_next_states = []

    # If the score of the moving player is already 21 or greater, we're done, no more moves.
    if moving_player_state[1] >= 21:
        return possible_next_states

    num_spaces = 10
    for roll in range(1,4):
        new_pos = (((moving_player_state[0] - 1) + roll) % num_spaces) + 1
        new_score = moving_player_state[1] + new_pos
        
        if moving_player == 0:
            possible_next_states.append(((new_pos, new_score), static_player_state))
        else:
            possible_next_states.append((static_player_state, (new_pos, new_score)))

    return possible_next_states


def get_next_states(s):
    ns0 = get_next_states_player(s, 0)
    ns1 = get_next_states_player(s, 1)
    return ns0 + ns1


def generate_all_states(s0):
    all_states = set()
    all_states.add(s0)
    states_to_check = set()
    states_to_check.add(s0)

    while len(states_to_check) != 0:
        next_states = set()
        for s in states_to_check:
            all_states.add(s)
            ns = get_next_states(s)
            next_states.update(ns)

        states_to_check = next_states - all_states

    return all_states


def solve_b(p1_pos, p2_pos):
    # we'll call a "state" ((p1_pos, p1_score), (p2_pos, p2_score))
    initial_state = ((p1_pos, 0), (p2_pos, 0))
    all_states = generate_all_states(initial_state)
    print('Found {0} states'.format(len(all_states)))

    # We can just build the forward map by calling get_next_states()
    # We can build the backward map kinda the same way
    forward_map = {}   # a map from a state to all the states it could go to
    backward_map = {}  # a map from a state to all the states that could've gotten us here


def main():
    player1_pos, player2_pos = read_input('./input.txt')
    solve_a([player1_pos, player2_pos])
    player1_pos, player2_pos = read_input('./input-test.txt')
    solve_b(player1_pos, player2_pos)


if __name__ == '__main__':
    main()
