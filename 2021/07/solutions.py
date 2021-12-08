def read_input(file_path):
    with open(file_path, 'r') as f:
        all_data = f.read()

    all_data = all_data.strip()
    all_data = all_data.split(',')
    return [int(i) for i in all_data]


def solve_a(pos):
    pos.sort()
    median_idx = len(pos) // 2
    median_pos = pos[median_idx]
    print('Median position is {0}'.format(median_pos))
    fuel_costs = [abs(p - median_pos) for p in pos]
    total_fuel_cost = sum(fuel_costs)
    print('Total fuel cost is {0}'.format(total_fuel_cost))


def main():
    positions = read_input('./input.txt')
    # solve_a([16,1,2,0,4,2,7,1,2,14])
    solve_a(positions)


if __name__ == '__main__':
    main()
