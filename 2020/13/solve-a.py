#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    min_time = int(all_lines[0].strip())
    raw_buses = all_lines[1].strip().split(',')
    buses = filter(lambda x: x != 'x', raw_buses)
    buses = [int(b) for b in buses]

    current_time = min_time
    while True:
        matches = [current_time % b for b in buses]
        if any([m == 0 for m in matches]):
            bus_idx = matches.index(0)
            bus_ID = buses[bus_idx]
            print('Take bus ID {0} at time {1}!'.format(bus_ID, current_time))
            break
        current_time = current_time + 1

    wait_time = current_time - min_time
    print('Bus ID {0} * wait time {1} = {2}'.format(bus_ID, wait_time, bus_ID * wait_time))


if __name__ == '__main__':
    main()
