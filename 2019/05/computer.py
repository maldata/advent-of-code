import instruction


class Computer:
    def __init__(self, program):
        self._program = program
        self._pc = 0
        self._halted = False

        self._opcode_map = {
            1: instruction.AddInstruction,
            2: instruction.MultiplyInstruction,
            3: instruction.ReadInputInstruction,
            4: instruction.PrintOutputInstruction,
            5: instruction.JumpIfTrueInstruction,
            6: instruction.JumpIfFalseInstruction,
            7: instruction.LessThanInstruction,
            8: instruction.EqualsInstruction,
            99: instruction.HaltInstruction
        }

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

        try:
            instr_class = self._opcode_map[opcode]
            instr = instr_class(self._program)
        except KeyError:
            print('Unknown opcode {0} at pc {1}'.format(opcode, self._pc))
            self._halted = True
            return
            
#        if opcode == 1:
#            instr = instruction.AddInstruction(self._program)
#        elif opcode == 2:
#            instr = instruction.MultiplyInstruction(self._program)
#        elif opcode == 3:
#            instr = instruction.ReadInputInstruction(self._program)
#        elif opcode == 4:
#            instr = instruction.PrintOutputInstruction(self._program)
#        elif opcode == 5:
#            instr = instruction.JumpIfTrueInstruction(self._program)
#        elif opcode == 6:
#            instr = instruction.JumpIfFalseInstruction(self._program)
#        elif opcode == 7:
#            instr = instruction.LessThanInstruction(self._program)
#        elif opcode == 8:
#            instr = instruction.EqualsInstruction(self._program)
#        elif opcode == 99:
#            instr = instruction.HaltInstruction(self._program)
#        else:
#            print('Unknown opcode {0} at pc {1}'.format(opcode, self._pc))
#            self._halted = True
#            return

        self._halted, self._pc = instr.execute(self._pc)
