from landscape import Landscape


def generate_neighbor_map(num_rows, num_cols):
    neighbors = {}
    for c in range(num_cols):
        for r in range(num_rows):
            coord = (r, c)
            neighbors[coord] = []
            if r > 0:
                neighbors[coord].append((r - 1, c))
            if r < num_rows - 1:
                neighbors[coord].append((r + 1, c))
            if c > 0:
                neighbors[coord].append((r, c - 1))
            if c < num_cols - 1:
                neighbors[coord].append((r, c + 1))
    
    return neighbors


def generate_map(preprocessed_lines, num_rows, num_cols):    
    heightmap = {}
    current = None
    dest = None
    for c in range(num_cols):
        for r in range(num_rows):
            elev = preprocessed_lines[r][c]
            if elev == 'S':
                heightmap[(r, c)] = 0
                current = (r, c)
            elif elev == 'E':
                heightmap[(r, c)] = ord('z') - ord('a')
                dest = (r, c)
            else:
                heightmap[(r, c)] = ord(elev) - ord('a')

    return heightmap, current, dest


def preprocess_lines(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    all_lines = [line.strip() for line in all_lines]
    all_lines = [[i for i in line] for line in all_lines]
    num_rows = len(all_lines)
    num_cols = len(all_lines[0])
    
    return all_lines, num_rows, num_cols


if __name__ == '__main__':
    preprocessed_lines, num_rows, num_cols = preprocess_lines('./input.txt')
    heightmap, start_coord, dest_coord = generate_map(preprocessed_lines, num_rows, num_cols)
    neighbor_map = generate_neighbor_map(num_rows, num_cols)

    landscape = Landscape(num_rows, num_cols, heightmap, neighbor_map)
    
    part1 = landscape.shortest_route(start_coord, dest_coord)
    print(f'Shortest path is {part1} steps')
