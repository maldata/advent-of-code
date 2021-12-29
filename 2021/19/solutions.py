import re


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
        scanner_coords.append(tmp_coords)
    
    # The first element of the list will be an empty list, so drop it
    return all_scanners[1:]


def main():
    all_scanner_coords = read_input('./input.txt')
    pass


if __name__ == '__main__':
    main()
