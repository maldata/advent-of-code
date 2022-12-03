def part1_calculate_score(opponent_play, self_play):
    opponent_map = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
    self_map = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}
    shape_score = {'rock': 1, 'paper': 2, 'scissors': 3}

    # First calculate the outcome score, 0 if I lose, 3 if it's a draw, 6 if I win
    opponents_pick = opponent_map[opponent_play]
    my_pick = self_map[self_play]
    outcome_score = 0

    # If we picked the same thing, it's a draw
    if opponents_pick == my_pick:
        outcome_score = 3
        
    # Combos where I win
    elif (my_pick == 'rock' and opponents_pick == 'scissors') or \
         (my_pick == 'paper' and opponents_pick == 'rock') or \
         (my_pick == 'scissors' and opponents_pick == 'paper'):
         outcome_score = 6

    return outcome_score + shape_score[my_pick]
    

def part1():
    all_lines = []
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    total_score = 0
    for line in all_lines:
        plays = line.strip().split(' ')
        round_score = part1_calculate_score(plays[0], plays[1])
        total_score = total_score + round_score
        
    print(f'Part one - total score: {total_score}')


def part2_calculate_score(opponent_play, outcome_code):
    opponent_map = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
    opponents_pick = opponent_map[opponent_play]

    outcome_map = {'X': 'lose', 'Y': 'draw', 'Z': 'win'}
    outcome_score_map = {'lose': 0, 'draw': 3, 'win': 6}

    my_pick = opponents_pick
    outcome = outcome_map[outcome_code]
    outcome_score = outcome_score_map[outcome]
    
    if (opponents_pick == 'rock' and outcome == 'draw') or \
       (opponents_pick == 'paper' and outcome == 'lose') or \
       (opponents_pick == 'scissors' and outcome == 'win'):
        my_pick = 'rock'
    elif (opponents_pick == 'rock' and outcome == 'win') or \
       (opponents_pick == 'paper' and outcome == 'draw') or \
       (opponents_pick == 'scissors' and outcome == 'lose'):
        my_pick = 'paper'
    else:
        my_pick = 'scissors'

    shape_score = {'rock': 1, 'paper': 2, 'scissors': 3}
    return outcome_score + shape_score[my_pick]

    
def part2():
    all_lines = []
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    total_score = 0
    for line in all_lines:
        round_parts = line.strip().split(' ')
        round_score = part2_calculate_score(round_parts[0], round_parts[1])
        total_score = total_score + round_score
        
    print(f'Part two - total score: {total_score}')


if __name__ == '__main__':
    part1()
    part2()
