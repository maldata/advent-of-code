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
    opponent_pos = opponent_state[0]
    opponent_score = opponent_state[1]

    new_states = []
    
    # If someone already won, no new states
    if player_score >= 21 or opponent_score >= 21:
        return new_states
    
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
    roll_sums = [sum(i) for i in all_quantum_roll_combos]

    # We don't really care what order the rolls happen, it just matters what the sum is.
    # There's only one way to get a sum of 9 (rolling three threes), but 7 ways to roll a sum of 6.
    # roll_sum_counts is a map from the sum (the key) to the number of ways it can be rolled (the value).
    roll_sum_counts = {}
    for rs in roll_sums:
        if rs not in roll_sum_counts:
            roll_sum_counts[rs] = 1
        else:
            roll_sum_counts[rs] = roll_sum_counts[rs] + 1

    player = 0
    parents = set()
    parents.add(initial_state)

    while True:
        new_children = set()
        for p in parents:
            opponent = 1 - player  # a fun trick to toggle between 0 and 1 without the ol' if/else
            player_state = p[player]
            player_pos = player_state[0]
            player_score = player_state[1]
            opponent_state = p[opponent]
            opponent_pos = opponent_state[0]
            opponent_score = opponent_state[1]

            # If someone already won, nothing else to do for this parent, move on to the next one
            if player_score >= 21 or opponent_score >= 21:
                continue

            for roll_sum in roll_sum_counts:
                count = roll_sum_counts[roll_sum]

                # get the new state based on the roll sum and whose turn it is
                new_position = (((player_pos - 1) + roll_sum) % 10) + 1
                new_score = player_score + new_position

                if player == 0:
                    new_state = ((new_position, new_score), opponent_state)
                else:
                    new_state = (opponent_state, (new_position, new_score))

                new_children.add(new_state)

                # the number of new universes in which that new state occurs is the roll sum count 
                # times the number of universes in which the parent occurs (because we can get that
                # roll sum many different ways)
                if new_state in num_universes:
                    num_universes[new_state] = num_universes[new_state] + (num_universes[p] * count)
                else:
                    num_universes[new_state] = num_universes[p] * count

        # the set of new children will be the parents on the next turn. If there aren't any, we're done!
        parents = new_children
        if len(parents) == 0:
            break

        # toggle whose turn will be next
        player = 1 - player

    p0_win_states = filter(lambda x: x[0][1] >= 21, num_universes.keys())
    p1_win_states = filter(lambda x: x[1][1] >= 21, num_universes.keys())
    
    num_p0_wins = sum([num_universes[i] for i in p0_win_states])
    num_p1_wins = sum([num_universes[i] for i in p1_win_states])

    print('P0 wins in {0} universes. P1 wins in {1} universes. {2} universes total.'.format(num_p0_wins, num_p1_wins, num_p0_wins + num_p1_wins))


def main():
    player1_pos, player2_pos = read_input('./input.txt')
    solve_a([player1_pos, player2_pos])
    player1_pos, player2_pos = read_input('./input-test.txt')
    solve_b(player1_pos, player2_pos)


if __name__ == '__main__':
    main()
