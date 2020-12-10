#!/usr/bin/env python3
from enum import Enum


class InstructionMode(Enum):
    POSITION = 0,
    IMMEDIATE = 1


class Instruction:
    def __init__(self, program):
        self._program = program
        self._num_params = 0
        self._parameters = []
        self._parameter_modes = []

    def _get_next_pc(self, pc):
        return pc + self.num_params + 1
        
    def _parse_word(self, pc, next_pc):
        word_strs = self._program[pc:next_pc]
        instr_str = word_strs[0]
        if len(instr_str) <= 2:
            self._parameter_modes = [InstructionMode.POSITION] * self.num_params
        else:
            modes = instr_str[:-2]
            if len(modes) < self.num_params:
                diff = self.num_params - len(modes)
                modes = '0' * diff + modes
            self._parameter_modes = [InstructionMode(i) for i in modes[::-1]]

        if self.num_params == 0:
            self._parameters = []
        else:
            self._parameters = [int(i) for i in word_strs[1:]]

    def _get_operand(self, op):
        param = self._parameters[op]
        mode = self._parameter_modes[op]

        if mode == InstructionMode.POSITION:
            return int(self._program[param])
        elif mode == InstructionMode.IMMEDIATE:
            return param
        else:
            raise ValueError
            
    @property
    def num_params(self):
        return self._num_params

    def execute(self):
        raise NotImplementedError


class AddInstruction(Instruction):
    def __init__(self, program):
        super().__init__(program)
        self._num_params = 3

    def execute(self, pc):
        next_pc = self._get_next_pc(pc)
        self._parse_word(pc, next_pc)

        operand1 = self._get_operand(0)
        operand2 = self._get_operand(1)
        operand3 = self._get_operand(2)

        self._program[operand3] = operand1 + operand2
        
        return False, next_pc

class MultiplyInstruction(Instruction):
    def __init__(self, program):
        super().__init__(program)
        self._num_params = 3

        def execute(self, pc):
            next_pc = self._get_next_pc(pc)
            self._parse_word(pc, next_pc)

            operand1 = self._get_operand(0)
            operand2 = self._get_operand(1)
            operand3 = self._get_operand(2)

            self._program[operand3] = operand1 * operand2
        
            return False, next_pc

class ReadInputInstruction(Instruction):
    def __init__(self, program):
        super().__init__(program)
        self._num_params = 1

    def execute(self, pc):
        next_pc = self._get_next_pc(pc)
        self._parse_word(pc, next_pc)

        operand1 = self._get_operand(0)

        print('==> Enter a value: ')
        i = input()
        self._program[operand1] = int(i)
        
        return False, next_pc

class PrintOutputInstruction(Instruction):
    def __init__(self, program):
        super().__init__(program)
        self._num_params = 1

    def execute(self, pc):
        next_pc = self._get_next_pc(pc)
        self._parse_word(pc, next_pc)

        operand1 = self._get_operand(0)

        print('==> {0}'.format(operand1))
        
        return False, next_pc


class HaltInstruction(Instruction):
    def __init__(self, program):
        super().__init__(program)

    def execute(self, pc):
        next_pc = self._get_next_pc(pc)
        self._parse_word(pc, next_pc)
        
        return True, next_pc
