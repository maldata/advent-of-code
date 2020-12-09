import instruction
from instruction_factory import InstructionFactory


class Program:
    def __init__(self, program_text):
        self._program_text = program_text
        factory = InstructionFactory()
        self._program = factory.build(self._program_text)
        self._pc = 0

    def execute(self):
        # TODO: run the program
        pass