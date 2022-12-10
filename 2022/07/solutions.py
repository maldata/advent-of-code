import re


class Node:
    def __init__(self, name, parent=None):
        self._parent = parent
        self._name = name

    def get_parent(self):
        return self._parent

    def get_name(self):
        return self._name

    def get_full_name(self):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError


class DirNode(Node):
    dir_register = {}

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self._children = []
    
    def get_size(self):
        if len(self._children) == 0:
            return 0
        else:
            return sum([c.get_size() for c in self._children])
        
    def add_child(self, child):
        already_in = False
        for c in self._children:
            already_in = already_in or c.get_name() == child.get_name()

        if not already_in:
            self._children.append(child)
            DirNode.dir_register[self.get_full_name()] = self

    def get_child_by_name(self, child_name):
        for c in self._children:
            if c.get_name() == child_name:
                return c
    
    def get_full_name(self):
        if self._parent is None:
            return '/'
        else:
            return self._parent.get_full_name() + self._name + '/'


class FileNode(Node):
    def __init__(self, size, name, parent):
        super().__init__(name, parent)
        self._size = size

    def get_size(self):
        return self._size
    
    def get_full_name(self):
        if self._parent is None:
            print('File with no parent!!!')
            return None
        else:
            return self._parent.get_full_name() + self._name


def load_tree():
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

    return root_node


def part1():
    total = 0
    for d_name in DirNode.dir_register:
        node = DirNode.dir_register[d_name]
        if node.get_size() <= 100000:
            total = total + node.get_size()

    print(f'Total sizes of all dirs under 100k: {total}')
    

def part2():
    used_size_before = DirNode.dir_register['/'].get_size()
    total_disk_size = 70000000
    required_free_space = 30000000
    min_dir_to_delete_size = used_size_before
    for d_name in DirNode.dir_register:
        node = DirNode.dir_register[d_name]
        dir_size = node.get_size()
        used_size_after = used_size_before - dir_size
        free_after = total_disk_size - used_size_after
        if free_after >= required_free_space and dir_size < min_dir_to_delete_size:
            min_dir_to_delete_size = dir_size
    
    print(f'The smallest directory we can delete is sized {min_dir_to_delete_size}')


if __name__ == '__main__':
    load_tree()    
    part1()
    part2()
