def read_input(file_path):
    with open(file_path, 'r') as f:
        all_data = f.read()

    all_data = all_data.strip()
    all_data = all_data.split(',')
    return [int(i) for i in all_data]


def get_next_fish_state(start_state):
    # First, we decrement each element
    new_state = [f - 1 for f in start_state]

    # Next, we count the number of -1s
    num_rollovers = new_state.count(-1)

    # Then we circle those -1s back around to 6s
    new_state = [6 if f < 0 else f for f in new_state]

    # And finally, add another fish for each rollover
    new_state.extend(num_rollovers*[8])
    return new_state


def solve_a(fish_state, days):
    num_fish = len(fish_state)
    days_remaining = days

    while days_remaining > 0:
        fish_state = get_next_fish_state(fish_state)
        # print(fish_state)
        num_fish = len(fish_state)
        days_remaining = days_remaining - 1

    print('After {0} days, there are {1} fish.'.format(days, num_fish))

def get_next_fish_state_dict(fish_state):
    new_fish_state = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    # First, we decrement each element (except -1, which better be zero...)
    if fish_state[-1] != 0:
        print("Something terrible has happened! We've got non-zero -1 timers!")

    for k in fish_state:
        if k == -1:
            continue
        new_fish_state[k - 1] = fish_state[k]

    # Next, we count the number of -1s
    num_rollovers = new_fish_state[-1]

    # Then we circle those -1s back around to 6s
    new_fish_state[6] = new_fish_state[6] + num_rollovers
    new_fish_state[-1] = 0

    # And finally, add another fish for each rollover
    new_fish_state[8] = num_rollovers
    return new_fish_state


def solve_b(fish_state, days):
    # Let's make a dictionary where the key is the timer value and the
    # value is the number of fish with that timer value
    counts = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    for f in fish_state:
        counts[f] = counts[f] + 1
    
    days_remaining = days
    while days_remaining > 0:
        counts = get_next_fish_state_dict(counts)
        # print(counts)
        num_fish = 0
        for k in counts:
            num_fish = num_fish + counts[k]

        days_remaining = days_remaining - 1
    
    print('After {0} days, there are {1} fish.'.format(days, num_fish))


def main():
    fish_state = read_input('./input.txt')
    copy_of_fish_state = [f for f in fish_state]
    solve_a(copy_of_fish_state, 80)
    copy_of_fish_state = [f for f in fish_state]
    solve_b(copy_of_fish_state, 256)


if __name__ == '__main__':
    main()
