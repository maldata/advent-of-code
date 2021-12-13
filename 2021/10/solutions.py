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

    return char_stack


def solve_a(all_lines):
    points = {')': 3, ']': 57, '}': 1197, '>': 25137}
    results = [line_is_corrupt(l) for l in all_lines]
    errors = filter(lambda x: isinstance(x, str), results)
    print('Total error score is {0}'.format(sum([points[e] for e in errors])))


def calc_auto_score(remaining_stack):
    points = {'(': 1, '[': 2, '{': 3, '<': 4}
    multiplier = 5
    score = 0

    for char in remaining_stack[::-1]:
        score = (score * multiplier) + points[char] 

    return score


def solve_b(all_lines):
    results = [line_is_corrupt(l) for l in all_lines]
    incompletes = filter(lambda x: isinstance(x, list), results)
    scores = [calc_auto_score(i) for i in incompletes]
    scores = [(scores[i], i) for i in range(len(scores))]
    scores.sort()  # uses the first element of the tuple by default
    num_incompletes = len(scores)

    middle_idx = num_incompletes // 2
    print('The middle score is {0}'.format(scores[middle_idx]))
    

def main():
    all_lines = read_input('./input.txt')
    solve_a(all_lines)
    solve_b(all_lines)


if __name__ == '__main__':
    main()
