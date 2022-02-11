from asyncio import all_tasks
import re
from turtle import backward


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
    states_to_check = set()
    states_to_check.add(s0)
    forward_map = {}   # a map from a state to all the states it could go to
    backward_map = {}  # a map from a state to all the states that could've gotten us there

    while len(states_to_check) != 0:
        next_states = set()
        for s in states_to_check:
            all_states.add(s)
            ns = get_next_states(s)
            forward_map[s] = ns

            for n in ns:
                # There's a little subtlety here. We have to create an empty set
                # first. We do NOT do set(s), because that will add each element
                # of our tuple s to the set, when we want the whole thing in there.
                if n not in backward_map:
                    backward_map[n] = set()
                backward_map[n].add(s)

            next_states.update(ns)

        states_to_check = next_states - all_states

    return all_states, forward_map, backward_map


def num_ways_to_get_to(s, backward_map):
    if s not in backward_map:
        return 1
    
    precursors = backward_map[s]
    return sum([num_ways_to_get_to(p, backward_map) for p in precursors])


def get_all_quantum_rolls(die_faces, num_rolls):
    if num_rolls == 1:
        return [[i] for i in range(1, die_faces + 1)]
    
    agg = []
    for i in get_all_quantum_rolls(die_faces, num_rolls - 1):
        for j in range(1, die_faces + 1):
            aug = i[:]
            aug.append(j)
            agg.append(aug)
    return agg


def states_after_quantum_rolls(s0, quantum_rolls, player):
    opponent = 0 if player == 1 else 0
    player_state = s0[player]
    player_pos = player_state[0]
    player_score = player_state[1]
    opponent_state = s0[opponent]

    new_states = []
    for qr in quantum_rolls:
        sum_of_rolls = sum(qr)
        new_position = (((player_pos - 1) + sum_of_rolls) % 10) + 1
        new_score = player_score + new_position

        if player == 0:
            new_state = ((new_position, new_score), opponent_state)
        else:
            new_state = (opponent_state, (new_position, new_score))

        new_states.append(new_state)

    return new_states

def solve_b(p1_pos, p2_pos):
    # we'll call a "state" ((p1_pos, p1_score), (p2_pos, p2_score))

    # As we play the game, 3 universes get spawned with each roll of the die, moving us into
    # 3 states (sometimes one we've already been in, sometimes a new one). All we really need
    # to know is in how many universes we end up in each state. Then, when we're done,
    # we'll look at all the end-game states and simply look up how many universes ended up there.
    num_universes = {}

    initial_state = ((p1_pos, 0), (p2_pos, 0))
    num_universes[initial_state] = 1

    all_quantum_roll_combos = get_all_quantum_rolls(3, 3)
    next_states = states_after_quantum_rolls(initial_state, all_quantum_roll_combos)

    # Now next_states is a list of all the states we could end up in based on
    # every combination of the three dice rolls from the state we were in.


    all_states, forward_map, backward_map = generate_all_states(initial_state)
    print('Found {0} states'.format(len(all_states)))

    p0_wins = set()
    p1_wins = set()
    ways_for_0_to_win = 0
    ways_for_1_to_win = 0
    for s in all_states:
        if s[0][1] >= 21:
            p0_wins.add(s)
            ways_for_0_to_win = ways_for_0_to_win + num_ways_to_get_to(s, backward_map)
        elif s[1][1] >= 21:
            p1_wins.add(s)
            ways_for_1_to_win = ways_for_1_to_win + num_ways_to_get_to(s, backward_map)

    print('There are {0} ways for player 0 to win'.format(ways_for_0_to_win))
    print('There are {0} ways for player 1 to win'.format(ways_for_1_to_win))


def main():
    player1_pos, player2_pos = read_input('./input.txt')
    solve_a([player1_pos, player2_pos])
    player1_pos, player2_pos = read_input('./input-test.txt')
    solve_b(player1_pos, player2_pos)


if __name__ == '__main__':
    main()
