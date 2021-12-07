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

def main():
    fish_state = read_input('./input.txt')
    solve_a(fish_state, 80)


if __name__ == '__main__':
    main()
