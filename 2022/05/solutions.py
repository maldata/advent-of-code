import re


def part1():
    with open('initial_stacks.txt', 'r') as f:
        stack_lines = f.readlines()

    stacks = {}
    line_num = 1
    for stack in stack_lines:
        stacks[line_num] = [i for i in stack.strip()]
        line_num = line_num + 1

    with open('sequence.txt', 'r') as f:
        steps = f.readlines()

    pattern = re.compile('move ([0-9]+) from ([0-9]+) to ([0-9]+)')
    for step in steps:
        result = pattern.match(step.strip())
        num_to_move = int(result.group(1))
        move_src = int(result.group(2))
        move_dest = int(result.group(3))

        for move in range(num_to_move):
            letter = stacks[move_src].pop(-1)
            stacks[move_dest].append(letter)

    num_stacks = len(stacks)
    top_crates = ''
    for s in range(1, num_stacks + 1):
        top_crates = top_crates + stacks[s][-1]

    print(f'Part 1 - top crates: {top_crates}')

def part2():
    with open('initial_stacks.txt', 'r') as f:
        stack_lines = f.readlines()

    stacks = {}
    line_num = 1
    for stack in stack_lines:
        stacks[line_num] = [i for i in stack.strip()]
        line_num = line_num + 1

    with open('sequence.txt', 'r') as f:
        steps = f.readlines()

    pattern = re.compile('move ([0-9]+) from ([0-9]+) to ([0-9]+)')
    for step in steps:
        result = pattern.match(step.strip())
        num_to_move = int(result.group(1))
        move_src = int(result.group(2))
        move_dest = int(result.group(3))

        letters_to_move = stacks[move_src][-num_to_move:]
        stacks[move_src] = stacks[move_src][:-num_to_move]
        stacks[move_dest] = stacks[move_dest] + letters_to_move

    num_stacks = len(stacks)
    top_crates = ''
    for s in range(1, num_stacks + 1):
        top_crates = top_crates + stacks[s][-1]

    print(f'Part 2 - top crates: {top_crates}')


if __name__ == '__main__':
    part1()
    part2()
