def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    return [row.strip() for row in all_lines]
    

def line_is_corrupt(line):
    closers = {'(': ')', '[': ']', '{': '}', '<': '>'}

    chars = [c for c in line]
    char_stack = []
    for c in chars:
        if c in ['(', '[', '{', '<']:
            char_stack.append(c)
        else:
            most_recent_opener = char_stack.pop()
            if c != closers[most_recent_opener]:
                return c


def solve_a(all_lines):
    points = {')': 3, ']': 57, '}': 1197, '>': 25137}
    results = [line_is_corrupt(l) for l in all_lines]
    errors = filter(lambda x: x is not None, results)
    print('Total error score is {0}'.format(sum([points[e] for e in errors])))


def solve_b(all_lines):
    pass


def main():
    all_lines = read_input('./input.txt')
    solve_a(all_lines)
    solve_b(all_lines)


if __name__ == '__main__':
    main()
