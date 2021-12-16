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
    
    def set_visited(self, visited):
        self.visited = visited


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
        return visited_names

    current_cave = caves[current_name]
    for n in current_cave.neighbors:
        c = caves[n]

        # If this neighbor is a small cave that has already been visited, skip it
        if not c.big and c.name in visited_names:
            continue

        # If this neighbor is large or hasn't been visited yet, stick it on the
        # visited list and find a path from there to the destination
        
        # TODO: this isn't gonna work... append mutates the shared list...
        visited_names.append(n)

        # TODO: the return value... what do we do with that?
        #  maybe we concatenate the visited list to the returned list?
        p = get_paths(caves, visited_names, dest_name)


def solve_a(caves):
    all_paths = get_paths(caves, ['start'], 'end')


def main():
    caves = read_input('./input.txt')
    solve_a(caves)


if __name__ == '__main__':
    main()
