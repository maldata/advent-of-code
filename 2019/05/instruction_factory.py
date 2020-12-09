import instruction


class InstructionFactory:
    def __init__(self):
        pass

    def build(self, program_text):
        prgm_str = program_text.split(',')
        prgm = []
        idx = 0
        while idx < len(prgm_str):
            # The assumption is that we're reading instructions first,
            # then we'll know how many parameters we'll need to read.
            cmd = prgm_str[idx]

            # The instruction part is the rightmost two characters
            # (leading zeros might not be present!)
            if len(cmd) <= 2:
                opcode = int(cmd)
            else:
                opcode = int(cmd[-2:])

            if opcode == 1:
                instr = instruction.AddInstruction()
            elif opcode == 2:
                instr = instruction.MultiplyInstruction()
            elif opcode == 3:
                instr = instruction.ReadInputInstruction()
            elif opcode == 4:
                instr = instruction.PrintOutputInstruction()
            elif opcode == 99:
                instr = instruction.HaltInstruction()
            else:
                print('Opcode {0} cannot be built by the instruction factory!'.format(opcode))
                return []

            next_index = idx + instr.num_params + 1
            word_strs = prgm_str[idx:next_index]  # add one for the instruction itself
            idx = next_index
            instr.parse_word(word_strs)
            prgm.append(instr)

        return prgm
