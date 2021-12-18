import re


class Cave:
    def __init__(self, name):
        self.name = name
        self.big = self.name == self.name.upper()
        self.neighbors = []
        self.visited = False
    
    def add_neighbor(self, new_neighbor):
        if new_neighbor not in self.neighbors:
            self.neighbors.append(new_neighbor)
    
    def can_be_visited(self, visited_caves):
        """
        If it's a small cave that has already been visited, it can't be visited again
        """
        if not self.big and self.name in visited_caves:
            return False
        
        return True


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    stripped = [line.strip() for line in all_lines]
    caves = {}
    for s in stripped:
        r = re.match("([a-zA-Z]+)-([a-zA-Z]+)", s)
        cave1 = r.group(1)
        cave2 = r.group(2)

        if cave1 not in caves:
            caves[cave1] = Cave(cave1)
        if cave2 not in caves:
            caves[cave2] = Cave(cave2)

        caves[cave1].add_neighbor(cave2)
        caves[cave2].add_neighbor(cave1)

    return caves


def get_paths(caves, visited_names, dest_name):
    current_name = visited_names[-1]
    if current_name == dest_name:
        return [visited_names]

    current_cave = caves[current_name]
    output_paths = []
    for n in current_cave.neighbors:
        c = caves[n]

        if not c.can_be_visited(visited_names):
            continue

        # If this neighbor is large or hasn't been visited yet,
        # find a path from there to the destination.
        visited_copy = [v for v in visited_names]
        visited_copy.append(n)
        next_paths = get_paths(caves, visited_copy, dest_name)
        for np in next_paths:
            output_paths.append(np)

    return output_paths

def solve_a(caves):
    all_paths = get_paths(caves, ['start'], 'end')
    print(len(all_paths))


def solve_b(caves):
    all_paths = get_paths(caves, ['start'], 'end')
    print(len(all_paths))


def main():
    caves = read_input('./input.txt')
    solve_a(caves)
    solve_b(caves)


if __name__ == '__main__':
    main()
