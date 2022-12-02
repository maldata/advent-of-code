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


def get_all_quantum_rolls(die_faces, num_rolls):
    """
    Returns a list of lists describing every possible outcome of num_rolls rolls of a die_faces-sided die.
    This won't ever change, so we should only use this once and then cache the result.
    """
    if num_rolls == 1:
        return [[i] for i in range(1, die_faces + 1)]
    
    agg = []
    for i in get_all_quantum_rolls(die_faces, num_rolls - 1):
        for j in range(1, die_faces + 1):
            aug = i[:]
            aug.append(j)
            agg.append(aug)
    return agg


def get_num_wins(roll_dist, s, outcome_cache):
    """
    Given the distribution of rolls (i.e., a map from the sum of the dice to the number of possible ways to get
    that sum), the state, and a cache of pre-calculated outcomes, get the outcome for state s. The outcome is a
    tuple (number of universes in which player 0 wins from state s, ditto for player 1).

    This function doesn't return anything, it just gloms it all together in the outcome cache dictionary.
    We could do the same thing without even calling this function by using memoization (like functools.lru_cache),
    but it's fun to implent things oneself, so I did.
    """
    # If we've already seen this state, we're done.
    if s in outcome_cache:
        return

    p0_state = s[0]
    p1_state = s[1]
    player_idx = s[2]
    
    # If player 0 has 21 or more points, there's only one way for things to end: p0 wins once, p1 wins 0 times.
    # Same if player 1 has 21 or more points.
    if p0_state[1] >= 21:
        outcome = (1, 0)
        outcome_cache[s] = outcome
        return
    if p1_state[1] >= 21:
        outcome = (0, 1)
        outcome_cache[s] = outcome
        return
    
    # In any other case, use the roll distribution to figure out what the next states will be (and in how many
    # universes we'll see them). Get the outcome for each state, multiply the outcomes by the count of each state,
    # aggregate them, and we're all set.
    opponent_idx = 1 - player_idx  # a fun trick to toggle between 0 & 1
    player_state = p0_state if player_idx == 0 else p1_state
    opponent_state = p0_state if player_idx == 1 else p1_state
    player_pos = player_state[0]
    player_score = player_state[1]

    total_p0_wins = 0
    total_p1_wins = 0
    for roll_sum in roll_dist:
        count = roll_dist[roll_sum]

        # get the new state based on the roll sum and whose turn it is
        new_position = (((player_pos - 1) + roll_sum) % 10) + 1
        new_score = player_score + new_position

        if player_idx == 0:
            new_state = ((new_position, new_score), opponent_state, opponent_idx)
        else:
            new_state = (opponent_state, (new_position, new_score), opponent_idx)

        get_num_wins(roll_dist, new_state, outcome_cache)
        child_p0_wins, child_p1_wins = outcome_cache[new_state]
        total_p0_wins = total_p0_wins + (count * child_p0_wins)
        total_p1_wins = total_p1_wins + (count * child_p1_wins)
    
    outcome = (total_p0_wins, total_p1_wins)
    outcome_cache[s] = outcome


def solve_b(p0_pos, p1_pos):
    # We'll call a "state" ((p0_pos, p0_score), (p1_pos, p1_score), next_player)

    # We'll also keep track of the outcome given a particular state. As we spawn new universes,
    # we might encounter a state that has already been solved. So, we won't bother solving them again.
    # Key is a state, value is a tuple (games won by p0, games won by p1).
    outcomes = {}
    initial_state = ((p0_pos, 0), (p1_pos, 0), 0)

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

    get_num_wins(roll_sum_counts, initial_state, outcomes)
    num_p0_wins, num_p1_wins = outcomes[initial_state]

    print('P0 wins in {0} universes. P1 wins in {1} universes. {2} universes total.'.format(num_p0_wins, num_p1_wins, num_p0_wins + num_p1_wins))
    if num_p0_wins > num_p1_wins:
        print('P0 wins more: {0}'.format(num_p0_wins))
    else:
        print('P1 wins more: {0}'.format(num_p1_wins))


def main():
    player1_pos, player2_pos = read_input('./input.txt')
    solve_a([player1_pos, player2_pos])
    player1_pos, player2_pos = read_input('./input.txt')
    solve_b(player1_pos, player2_pos)


if __name__ == '__main__':
    main()
