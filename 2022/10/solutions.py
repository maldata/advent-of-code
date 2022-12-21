def part1():
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()
    
    x_reg_at_cycle_start = [1]
    for line in all_lines:
        line = line.strip()
        parts = line.split(' ')

        # For noop, just keep the latest x_register for one more cycle
        if parts[0] == 'noop':
            x_reg_at_cycle_start.append(x_reg_at_cycle_start[-1])
        
        # For addx, keep the latest x_register for one cycle, then add
        # the value to the register on the next cycle.
        elif parts[0] == 'addx':
            value_to_add = int(parts[1])
            x_reg_at_cycle_start.append(x_reg_at_cycle_start[-1])
            x_reg_at_cycle_start.append(x_reg_at_cycle_start[-1] + value_to_add)

        else:
            print('OH NO.')

    # Now we calculate the signal strengths on certain cycles. Note that we
    # decrement the cycle number by one to account for our zero index.
    target_cycles = [20, 60, 100, 140, 180, 220]
    strengths = [x_reg_at_cycle_start[i-1] * i for i in target_cycles]

    print(f'Sum of signal strengths is {sum(strengths)}.')
    return x_reg_at_cycle_start


def part2(x_reg):
    pixels = ['.'] * len(x_reg)
    for cycle, sprite_pos in enumerate(x_reg):
        #if (cycle % 40) == sprite_pos or (cycle % 40) == sprite_pos - 1 or (cycle % 40) == sprite_pos + 1:
        if abs((cycle % 40) - sprite_pos) <= 1:
            pixels[cycle] = '#'
    
    for line_idx in range(6):
        line_pixels = pixels[line_idx * 40 : (line_idx + 1) * 40]
        print(''.join(line_pixels))


if __name__ == '__main__':
    x_register_history = part1()
    part2(x_register_history)
