#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    raw_buses = all_lines[1].strip().split(',')
    int_buses = filter(lambda x: x != 'x', raw_buses)
    int_buses = [int(b) for b in int_buses]

    # We're looking to find a place where the buses come in on subsequent
    # minutes (skipping the x-ed out ones). So the index of the bus ID is
    # the offset in minutes from the time the first one in the list comes in.
    time_offsets = [raw_buses.index(str(i)) for i in int_buses]

    first_bus_id = int_buses[0]

    # We are told that this won't happen until after time 100000000000000,
    # so we'll go there and then rewind until a time when the first bus ID hits
    current_time = 100000000000000
    offset = current_time % first_bus_id
    current_time = current_time - offset

    # Now we just go minute by minute until we find the time when each bus
    # comes in offset by the number of minutes in the time_offsets list

    while True:
        moduli = [(current_time + time_offsets[i]) % int_buses[i] for i in range(len(int_buses))]
        mod0 = [m == 0 for m in moduli]
        if all(mod0):
            break
        current_time = current_time + first_bus_id

    print('The buses line up sequentially by minute starting at time {0}'.format(current_time))


if __name__ == '__main__':
    main()
