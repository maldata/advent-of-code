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

    # Before running, we corrupt the program with a 1202
    program[1] = 12
    program[2] = 2
    new_state = run_program(program)

    print(program)
    print(new_state)

    output_addr = 0
    if len(new_state) > output_addr:
        print('The value in index 0 is {0}'.format(new_state[output_addr]))
    else:
        print("Output address {0} doesn't exist!".format(output_addr))


if __name__ == '__main__':
    main()
