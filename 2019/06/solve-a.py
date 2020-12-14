#!/usr/bin/env python3
class Mass:
    def __init__(self, name):
        self._name = name
        self._children = []
        self._parent = None

    def add_child_orbit(self, child):
        self._children.append(child)

    def set_parent(self, parent):
        self._parent = parent
        
    def get_path_length(self):
        if self._name == 'COM':
            return 0

        return 1 + self._parent.get_path_length()
        

def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_orbits = [i.strip() for i in all_lines]
    all_masses = {}

    # Link all orbits into a tree
    for orbit in all_orbits:
        masses = orbit.split(')')
        m0 = masses[0]
        m1 = masses[1]
        if m0 not in all_masses:
            all_masses[m0] = Mass(m0)
        if m1 not in all_masses:
            all_masses[m1] = Mass(m1)

        all_masses[m0].add_child_orbit(all_masses[m1])
        all_masses[m1].set_parent(all_masses[m0])

    # Now go through all the masses and measure the length of
    # the path to the center of mass (mass named 'COM')
    path_length_sum = 0
    for mass in all_masses:
        m = all_masses[mass]
        path_length_sum = path_length_sum + m.get_path_length()

    print('Total orbits: {0}'.format(path_length_sum))

    
if __name__ == '__main__':
    main()
