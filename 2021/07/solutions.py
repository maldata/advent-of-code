from math import floor, ceil

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


def calculate_fuel(positions, align_pos):
    pos_diff = [abs(p - align_pos) for p in positions]
    fuel_costs = [sum(range(p + 1)) for p in pos_diff]
    return sum(fuel_costs)


def solve_b(pos):
    avg_pos = sum(pos) / len(pos)
    avg_floor = floor(avg_pos)
    avg_ceil = ceil(avg_pos)

    fuel_floor = calculate_fuel(pos, avg_floor)
    fuel_ceil = calculate_fuel(pos, avg_ceil)

    print('Testing floor. Position {0}, fuel cost {1}'.format(avg_floor, fuel_floor))
    print('Testing ceiling. Position {0}, fuel cost {1}'.format(avg_ceil, fuel_ceil))

    min_fuel = min([fuel_floor, fuel_ceil])
    
    if min_fuel == fuel_floor:
        min_pos = avg_floor
    else:
        min_pos = avg_ceil
    print('The position {0} has the lowest fuel cost ({1}).'.format(min_pos, min_fuel))


def main():
    positions = read_input('./input.txt')
    solve_a(positions)
    solve_b(positions)


if __name__ == '__main__':
    main()
