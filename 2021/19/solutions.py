import re


def single_rotation(point, axis, rotation):
    # sines and cosines for 0, pi/2, pi, 3pi/2, 2pi
    cosines = [1, 0, -1, 0]
    sines = [0, 1, 0, -1]

    cos = cosines[rotation]
    sin = sines[rotation]

    x = point[0]
    y = point[1]
    z = point[2]

    if axis == 0:
        # x-axis rotation
        new_point = (x, y*cos-z*sin, y*sin+z*cos)
    elif axis == 1:
        # y-axis rotation
        new_point = (x*cos+z*sin, y, -x*sin+z*cos)
    else:
        # z-axis rotation
        new_point = (x*cos-y*sin, x*sin+y*cos, z)

    return new_point


def rotate(pt, fr, pr):
    # First do the face rotation
    face_rotated = single_rotation(pt, fr[0], fr[1])

    # Now do the plane rotation on that rotated point
    return single_rotation(face_rotated, pr[0], pr[1])


class Scanner:
    def __init__(self, scanner_num, orig_points) -> None:
        self.id = scanner_num
        self.relative_beacon_pos = orig_points
        self.global_position = None
        self.orientations = []
        self.locked_orientation_idx = None
        self.position_known = False

        # Getting all the orientations is weird. There are 24 ways the axes can be rotated...
        # Think about rolling a 6-sided die. It can land with each of the 6 faces up, and that
        # face can be rotated 4 ways on the plane. So basically, we rotate each axis (and
        # its negative) into the "upward" orientation, then rotate 4 times around that axis.
        #
        # So, first, the 6 rotations to get the "upward faces":
        # No rotation, x90, x180, x270, z90, z270
        #
        # Remember, x is 0, y is 1, and z is 2. radians are in units of pi/2.
        # Then, for each of those upward faces, we do all four z rotations. So, the sequences are:
        face_rotations = [(0, 0), (0, 1), (0, 2), (0, 3), (2, 1), (2, 3)]
        plane_rotations = [(1, 0), (1, 1), (1, 2), (1, 3)]

        for f in face_rotations:
            for p in plane_rotations:
                rotated_points = [rotate(pt, f, p) for pt in orig_points]
                self.orientations.append(rotated_points)
    
    def get_global_beacon_positions(self):
        if not self.position_known:
            return []

        rotated_points = self.orientations[self.locked_orientation_idx]
        return [(pt[0] + self.global_position[0],
                 pt[1] + self.global_position[1],
                 pt[2] + self.global_position[2]) for pt in rotated_points]

    def lock_global_position(self, scanner_pos, orientation_idx):
        self.position_known = True
        self.global_position = scanner_pos
        self.locked_orientation_idx = orientation_idx

        msg_template = 'Scanner {0} locked at {1} and orientation {2}'
        print(msg_template.format(self.id, self.global_position, self.locked_orientation_idx))
        
    def try_to_match_beacons(self, other):
        if not self.position_known:
            return False

        locked_global_pos = None
        locked_orientation_index = None
        max_overlaps = 0

        for o_idx in range(len(other.orientations)):
            o = other.orientations[o_idx]
            num_overlaps, offset = get_offset_and_overlaps(o, self.get_global_beacon_positions())
            # print('({0} and {1}, orientation {2}) : {3}'.format(self.id, other.id, o_idx, num_overlaps))

            if num_overlaps >= 12 and num_overlaps > max_overlaps:
                print('Match found for scanner {0}'.format(self.id))
                max_overlaps = num_overlaps
                locked_global_pos = (self.global_position[0] - offset[0],
                                     self.global_position[1] - offset[1],
                                     self.global_position[2] - offset[2])
                locked_orientation_index = o_idx
                locked_global_pos = offset
        
        if max_overlaps >= 12:
            other.lock_global_position(locked_global_pos, locked_orientation_index)
            return True

        return False


def get_offset_and_overlaps(unknown_relative_coords, known_global_coords):
    """
    Given two sets of coordinates, find the offset that maximizes the number
    of overlapping points (then return the number of overlaps and the offset).
    """
    max_overlaps = 0
    offset_with_max_overlaps = (0, 0, 0)

    num_urc = len(unknown_relative_coords)
    num_kgc = len(known_global_coords)

    indices_to_align = [(i,j) for i in range(num_urc) for j in range(num_kgc)]
    for combo in indices_to_align:
        mobile = unknown_relative_coords[combo[0]]
        fixed = known_global_coords[combo[1]]

        # Find the offset between the two aligned points
        offset = (fixed[0] - mobile[0], fixed[1] - mobile[1], fixed[2] - mobile[2])

        # Move all the "mobile" points by the offset and see if that
        # shifted position is in the list of "fixed" points
        shifted_globals = [(kgc[0] - offset[0], kgc[1] - offset[1], kgc[2] - offset[2]) for kgc in known_global_coords]
        overlapping_pts = filter(lambda sg: sg in unknown_relative_coords, shifted_globals)
        num_overlaps = len(list(overlapping_pts))
        
        if num_overlaps > max_overlaps:
            max_overlaps = num_overlaps
            offset_with_max_overlaps = offset

    return max_overlaps, offset_with_max_overlaps


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    all_scanners = []
    scanner_coords = []
    for line in all_lines:
        line = line.strip()
        m = re.match('--- scanner ([0-9]+) ---', line)
        if m:
            # Every time we match the scanner line, take whatever coordinate lines
            # we've buffered up and glom them together into one entry in all_scanners.
            # If there are no coordinates, it's because it's the first one we hit.
            if len(scanner_coords) > 0:
                all_scanners.append(scanner_coords)
                scanner_coords = []
            continue

        if len(line) == 0:
            continue

        tmp_coords = [int(i) for i in line.split(',')]
        scanner_coords.append((tmp_coords[0], tmp_coords[1], tmp_coords[2]))
    
    all_scanners.append(scanner_coords)
    return all_scanners


def solve_a(scanners):
    # We'll arbitrarily choose the first one in the list 
    # and declare that it's in the global reference frame.
    scanner0 = scanners[0]
    scanner0.lock_global_position((0, 0, 0), 0)

    num_prev_known = 0
    while True:
        # Get the lists of known and unknown scanners
        all_known = list(filter(lambda x: x.position_known, scanners))
        all_unknown = list(filter(lambda x: not x.position_known, scanners))

        num_known = len(all_known)
        if num_known == len(scanners) or num_known == num_prev_known:
            print('Done looping. There are {0} known scanners.'.format(num_known))
            break

        num_prev_known = num_known
        
        all_combos = [(k, u) for k in range(len(all_known)) for u in range(len(all_unknown))]
        for combo in all_combos:
            known = all_known[combo[0]]
            unknown = all_unknown[combo[1]]

            result = known.try_to_match_beacons(unknown)
            if result:
                break

    # All scanner positions are now known. Count up the number of unique beacon positions
    unique_beacons = set()
    for scanner in scanners:
        for beacon in scanner.get_global_beacon_positions():
            unique_beacons.add(beacon)
    
    print('There are {0} unique beacons'.format(len(unique_beacons)))


def solve_b(scanners):
    num_scanners = len(scanners)
    combos = [(i, j) for i in range(num_scanners) for j in range(i + 1, num_scanners)]
    max_dist = 0
    for combo in combos:
        s1 = scanners[combo[0]].global_position
        s2 = scanners[combo[1]].global_position

        dist = abs(s2[0] - s1[0]) + abs(s2[1] - s1[1]) + abs(s2[2] - s1[2])
        max_dist = max(dist, max_dist)


def main():
    all_scanner_coords = read_input('./input.txt')
    num_scanners = len(all_scanner_coords)
    all_scanners = []
    for idx in range(num_scanners):
        coords = all_scanner_coords[idx]
        all_scanners.append(Scanner(idx, coords))

    solve_a(all_scanners)
    solve_b(all_scanners)


if __name__ == '__main__':
    main()
