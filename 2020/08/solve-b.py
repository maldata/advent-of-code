#!/usr/bin/env python3
def execute_until_repeat_or_end(program):
    """
    Return a tuple of 'ended successfully' and the accumulator.
    If 'ended successfully' is false, then it hit an infinite loop.
    """
    pc = 0
    accumulator = 0
    while True:
        if pc >= len(program):
            return True, accumulator

        next_command = program[pc]
        number_of_executions = next_command[1]
        operation = next_command[2]
        argument = int(next_command[3])
        
        if number_of_executions > 0:
            return False, accumulator

        # Make a new tuple and replace the number of executions
        new_state = (pc, number_of_executions + 1, operation, argument)
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
            return False, accumulator

def mutate_at_index(program, index):
    """
    Start at index and try to do a mutation. If it can't be done, advance index until it can
    """
    while True:
        if index >= len(program):
            return index
        
        command_to_mutate = program[index]
        number_of_executions = command_to_mutate[1]
        operation = command_to_mutate[2]
        argument = command_to_mutate[3]
        
        if operation == 'jmp':
            mutated_command = (index, number_of_executions, 'nop', argument)
            break
        elif operation == 'nop':
            mutated_command = (index, number_of_executions, 'jmp', argument)
            break
        else:
            # If it's an acc, just advance until we hit a nop or jmp
            index = index + 1

    # Once a mutation has happened, set the new tuple into the program and
    # return the index of the tuple that changed.
    program[index] = mutated_command
    return index


def try_all_mutations(program):
    mutated_index = 0
    successful = False
    accumulator = 0

    while True:
        edited_program = list(program)
        if mutated_index >= len(program):
            return successful, accumulator
        
        mutated_index = mutate_at_index(edited_program, mutated_index)        
        successful, accumulator = execute_until_repeat_or_end(edited_program)
        if successful:
            return successful, accumulator
        else:
            # Change the command back, then advance the index
            mutated_index = mutate_at_index(edited_program, mutated_index)
            mutated_index = mutated_index + 1
            
        
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    full_program = [line.strip() for line in all_lines]

    # The tuples in the list are
    # (command index, number of executions, mutated, operation, argument)
    command_states = [(i, 0, j.split(' ')[0], j.split(' ')[1]) for i, j in enumerate(full_program)]

    successful, accumulator = try_all_mutations(command_states)
    print('When the program ends correctly, the accumulator is {0}'.format(accumulator))


if __name__ == '__main__':
    main()
