import re


class Monkey:
    def __init__(self, lines, relief_divisor) -> None:
        self._op_type = '+'
        self._op_arg = 0
        self._test_div = 1
        self._true_throw = 0
        self._false_throw = 0
        self._inspections = 0
        self._relief_divisor = relief_divisor

        for line in lines:
            parts = line.strip().split(':')
            key = parts[0].strip()
            value = parts[1].strip()

            if key.startswith('Monkey'):
                id_parts = key.split(' ')
                self._id = int(id_parts[1])
            elif key.startswith('Starting items'):
                self._items = [int(i) for i in value.split(',')]
            elif key.startswith('Operation'):
                m = re.match('new = old ([\+\*]) (old|[0-9]+)', value)
                self._op_type = m.group(1)
                self._op_arg = m.group(2)

                if self._op_type == '+' and self._op_arg == 'old':
                    self._op_type = '*'
                    self._op_arg = 2
                elif self._op_type == '*' and self._op_arg == 'old':
                    self._op_type = '**'
                    self._op_arg = 2
                else:
                    self._op_arg = int(self._op_arg)

            elif key.startswith('Test'):
                m = re.match('divisible by ([0-9]+)', value)
                self._test_div = int(m.group(1))
            elif key.startswith('If true'):
                m = re.match('throw to monkey ([0-9]+)', value)
                self._true_throw = int(m.group(1))
            elif key.startswith('If false'):
                m = re.match('throw to monkey ([0-9]+)', value)
                self._false_throw = int(m.group(1))

    def num_inspections(self) -> int:
        return self._inspections

    def num_items(self) -> int:
        return len(self._items)

    def inspect_first_item(self) -> tuple[int, int]:
        self._inspections = self._inspections + 1
        item = self._items.pop(0)
        if self._op_type == '+':
            item = item + self._op_arg
        elif self._op_type == '*':
            item = item * self._op_arg
        elif self._op_type == '**':
            item = item ** self._op_arg
        else:
            print(f'Unknown operator: {self._op_type}')
        
        test_val = item // self._relief_divisor
        if test_val % self._test_div == 0:
            return self._true_throw, test_val
        else:
            return self._false_throw, test_val

    def catch_item(self, item):
        self._items.append(item)


def load_monkeys(file_path, relief_divisor):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    monkeys = []
    line_buffer = []
    for line in all_lines:
        if line.strip() == '':
            monkeys.append(Monkey(line_buffer, relief_divisor))
            line_buffer = []
        else:
            line_buffer.append(line)
    
    # Make sure the last monkey gets built
    if len(line_buffer) > 0:
        monkeys.append(Monkey(line_buffer, relief_divisor))
        line_buffer = []

    return monkeys


def calc_monkey_business(file_path, rounds, relief_divisor):
    monkeys = load_monkeys(file_path, relief_divisor)    
    for round in range(rounds):
        #print(f'Starting round {round}')
        for m in monkeys:
            while m.num_items() > 0:
                target_idx, item = m.inspect_first_item()
                target_monkey = monkeys[target_idx]
                target_monkey.catch_item(item)
    
    inspections = [m.num_inspections() for m in monkeys]
    inspections.sort()
    monkey_business = inspections[-1] * inspections[-2]
    print(f'Amount of monkey business: {monkey_business}')


if __name__ == '__main__':
    calc_monkey_business('./input.txt', 20, 3)
    calc_monkey_business('./input.txt', 10000, 1)
