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


class TwiceVisitableCave(Cave):
    def __init__(self, name):
        super().__init__(name)
    
    def can_be_visited(self, visited_caves):
        """
        Allow one small cave to be visited twice
        """
        # If it's a big cave, you can always visit it
        if self.big:
            return True

        # The start and end caves can only ever be visited once
        if self.name == 'start' or self.name == 'end':
            return self.name not in visited_caves
        
        # Is there already a small cave that has been visited twice?
        # If so, then this one can only be visited if it hasn't been visited before.
        f = filter(lambda x: x == x.lower(), visited_caves)
        visited_small_caves = list(set(f))
        times_visited = [visited_caves.count(i) for i in visited_small_caves]
        any_visited_twice = any([t > 1 for t in times_visited])

        if any_visited_twice:
            return self.name not in visited_caves

        return True


def read_input(file_path, class_name):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    stripped = [line.strip() for line in all_lines]
    caves = {}
    for s in stripped:
        r = re.match("([a-zA-Z]+)-([a-zA-Z]+)", s)
        cave1 = r.group(1)
        cave2 = r.group(2)

        if cave1 not in caves:
            caves[cave1] = class_name(cave1)
        if cave2 not in caves:
            caves[cave2] = class_name(cave2)

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
    caves = read_input('./input.txt', Cave)
    solve_a(caves)

    caves = read_input('./input.txt', TwiceVisitableCave)
    solve_b(caves)


if __name__ == '__main__':
    main()
