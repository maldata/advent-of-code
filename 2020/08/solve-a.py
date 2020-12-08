#!/usr/bin/env python3
def execute_until_repeat(program):
    pc = 0
    accumulator = 0
    while True:
        next_command = program[pc]
        if next_command[1] > 0:
            break

        operation = next_command[2]
        argument = int(next_command[3])

        # Make a new tuple and replace the number of executions
        new_state = (pc, next_command[1] + 1, operation, argument)
        program[pc] = new_state

        if operation == 'jmp':
            pc = pc + argument
        elif operation == 'acc':
            accumulator = accumulator + argument
            pc = pc + 1
        elif operation == 'nop':
            pc = pc + 1
        else:
            print('Operation {0} not permitted'.format(operation))
            break

    return accumulator


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    full_program = [line.strip() for line in all_lines]

    # The tuples in the list are (command index, number of executions, operation, argument)
    command_states = [(i, 0, j.split(' ')[0], j.split(' ')[1]) for i, j in enumerate(full_program)]
    print(command_states)

    accumulator = execute_until_repeat(command_states)
    print('Before any commands are executed a second time, the accumulator is {0}'.format(accumulator))


if __name__ == '__main__':
    main()
