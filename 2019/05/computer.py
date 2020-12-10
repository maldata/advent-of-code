import instruction


class Computer:
    def __init__(self, program):
        self._program = program
        self._pc = 0
        self._halted = False

    def compute(self):
        while not self._halted:
            self._iterate()

    def _iterate(self):
        # We make the assumption that the program counter is on an
        # instruction, so we start by getting the instruction and
        # using that to figure out how many parameters follow it.
        instr_str = self._program[self._pc]

        # The instruction part is the rightmost two characters
        # (leading zeros might not be present!)
        if len(instr_str) <= 2:
            opcode = int(instr_str)
        else:
            opcode = int(instr_str[-2:])

        if opcode == 1:
            instr = instruction.AddInstruction(self._program)
        elif opcode == 2:
            instr = instruction.MultiplyInstruction(self._program)
        elif opcode == 3:
            instr = instruction.ReadInputInstruction(self._program)
        elif opcode == 4:
            instr = instruction.PrintOutputInstruction(self._program)
        elif opcode == 99:
            instr = instruction.HaltInstruction(self._program)
        else:
            print('Unknown opcode {0} at pc {1}'.format(opcode, self._pc))
            self._halted = True
            return

        self._halted, self._pc = instr.execute(self._pc)
