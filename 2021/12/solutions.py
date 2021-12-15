import re

def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    stripped = [line.strip() for line in all_lines]
    edges = []
    for s in stripped:
        r = re.match("([a-zA-Z]+)-([a-zA-Z]+)", s)
        edges.append((r.group(1), r.group(2)))

    return edges


def solve_a(edges):
    pass


def main():
    edges = read_input('./input.txt')
    solve_a(edges)


if __name__ == '__main__':
    main()
