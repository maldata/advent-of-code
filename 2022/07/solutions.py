import re


class Node:
    def __init__(self, name, parent=None):
        self._parent = parent
        self._name = name

        if parent is None:
            self._full_name = self._name
        else:
            self._full_name = parent.get_full_name() + '/' + self._name

    def get_parent(self):
        return self._parent

    def get_name(self):
        return self._name

    def get_full_name(self):
        return self._full_name

    def get_size(self):
        raise NotImplementedError


class DirNode(Node):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self._children = []
    
    def get_size(self):
        if len(self._children) == 0:
            return 0
        else:
            return sum([c.get_size() for c in self._children])

    def add_child(self, child):
        self._children.append(child)

    def get_child_by_name(self, child_name):
        for c in self._children:
            if c.get_name() == child_name:
                return c


class FileNode(Node):
    def __init__(self, size, name, parent):
        super().__init__(name, parent)
        self._size = size

    def get_size(self):
        return self._size


def part1():
    with open('input.txt', 'r') as f:
        all_lines = f.readlines()

    terminal = [l.strip() for l in all_lines]
    terminal = terminal[1:] # The first line just puts us in / so ignore it.

    root_node = DirNode('/')
    current_node = root_node
    while len(terminal) > 0:
        cmd = terminal.pop(0)
        if re.match('^\$\s+ls', cmd):
            while len(terminal) > 0:
                output = terminal[0]
                if output[0] == '$':
                    break
                elif output[0:4] == 'dir ':
                    new_dir_node = DirNode(output[4:], current_node)
                    current_node.add_child(new_dir_node)
                else:
                    parts = output.split(' ')
                    new_file_node = FileNode(int(parts[0]), parts[1], current_node)
                    current_node.add_child(new_file_node)
                
                terminal.pop(0)

        elif re.match('^\$\s+cd\s+([a-z]+)', cmd):
            m = re.match('^\$\s+cd\s+([a-z]+)', cmd)
            child_name = m.group(1)
            child_dir = current_node.get_child_by_name(child_name)
            if child_dir is None:
                print(f'Failed to find child {child_name} of {current_node.get_full_name()}')
            current_node = child_dir
        elif re.match('\$\s+cd\s+\.\.', cmd):
            p = current_node.get_parent()
            if p is None:
                print('Null parent... uh oh!')
            current_node = p
        else:
            print('Something terrible has happened!')
            break

    root_node.get_size()

def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
