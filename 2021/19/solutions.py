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
    def __init__(self, orig_points) -> None:
        self.orientations = []

        # Getting all the orientations is weird. There are 24 ways the axes can be rotated...
        # Think about rolling a 6-sided die. It can land with each of the 6 faces up, and that
        # face can be rotated 4 ways on the plane. So basically, we rotate each axis (and
        # its negative) into the "upward" orientation, then rotate 4 times around that axis.
        #
        # So, first, the 6 rotations to get the "upward faces":
        # No rotation, x90, x180, x270, y90, y270
        #
        # Remember, x is 0, y is 1, and z is 2. radians are in units of pi/2.
        # Then, for each of those upward faces, we do all four z rotations. So, the sequences are:
        face_rotations = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 3)]
        plane_rotations = [(2, 0), (2, 1), (2, 2), (2, 3)]

        for f in face_rotations:
            for p in plane_rotations:
                rotated_points = [rotate(pt, f, p) for pt in orig_points]
                self.orientations.append(rotated_points)


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    all_scanners = []
    scanner_coords = []
    for line in all_lines:
        line = line.strip()
        m = re.match('--- scanner ([0-9]+) ---', line)
        if m:
            all_scanners.append(scanner_coords)
            scanner_coords = []
            continue

        if len(line) == 0:
            continue

        tmp_coords = [int(i) for i in line.split(',')]
        scanner_coords.append((tmp_coords[0], tmp_coords[1], tmp_coords[2]))
    
    # The first element of the list will be an empty list, so drop it
    return all_scanners[1:]


def main():
    all_scanner_coords = read_input('./input-test.txt')
    all_scanners = []
    for coords in all_scanner_coords:
        all_scanners.append(Scanner(coords))
    pass


if __name__ == '__main__':
    main()
