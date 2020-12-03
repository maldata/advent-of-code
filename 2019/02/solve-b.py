#!/usr/bin/env python3
def execute(program, pc):
    word_size = 4
    if program[pc] == 99:
        print("Halted at pc {0}".format(pc))
        return True, pc, program

    if len(program) < pc+word_size:
        print("There isn't a full word left starting at pc {0}".format(pc))
        return True, pc, program

    word = program[pc:pc + word_size]
    opcode = word[0]
    arg1 = word[1]
    arg2 = word[2]
    arg3 = word[3]

    value1 = program[arg1]
    value2 = program[arg2]

    if opcode == 1:
        result = value1 + value2
    elif opcode == 2:
        result = value1 * value2
    else:
        print('Invalid opcode {0} at pc {1}'.format(opcode, pc))
        return True, pc, program

    program[arg3] = result
    pc = pc + word_size
    return False, pc, program


def run_program(program):
    program = list(program)
    halted = False
    pc = 0
    while not halted:
        halted, pc, program = execute(program, pc)

    return program


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    program = all_lines[0].strip()
    program = program.split(',')
    program = [int(i) for i in program]

    # Find the noun (program[1]) and verb (program[2]) that result in an output of 19690720
    target = 19690720
    output_addr = 0
    found = False
    all_combos = [(i, j) for i in range(99) for j in range(99)]
    for n, v in all_combos:
        program[1] = n
        program[2] = v
        new_state = run_program(program)
        if new_state[output_addr] == target:
            print(program)
            print(new_state)
            found = True
            break

    if found:
        print('The value in index 0 is {0} for noun {1} and verb {2}'.format(new_state[output_addr], n, v))
        print('100 * noun + verb = {0}'.format(100 * n + v))
    else:
        print('Exhausted all combinations. Did not find a result.')


if __name__ == '__main__':
    main()
