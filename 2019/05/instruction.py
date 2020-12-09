#!/usr/bin/env python3
from enum import Enum


class InstructionMode(Enum):
    POSITION = 0,
    IMMEDIATE = 1


class Instruction:
    def __init__(self):
        self._num_params = 0
        self._parameters = []
        self._parameter_modes = []

    def parse_word(self, word_strs):
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

    @property
    def num_params(self):
        return self._num_params

    def execute(self):
        raise NotImplementedError


class AddInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self._num_params = 3

    def execute(self):
        # TODO: given the parameters and their modes, do addition and put it where it goes
        pass

class MultiplyInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self._num_params = 3


class ReadInputInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self._num_params = 1


class PrintOutputInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self._num_params = 1


class HaltInstruction(Instruction):
    def __init__(self):
        super().__init__()
