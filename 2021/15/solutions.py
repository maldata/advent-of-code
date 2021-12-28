class Node:
    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.visited = False
        self.dist = None
        self.prev = None


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    all_lines = [line.strip() for line in all_lines]
    num_rows = len(all_lines)
    num_cols = len(all_lines[0])
    
    all_coords = [(r, c) for r in range(num_rows) for c in range(num_cols)]
    risks = {}
    nodes = {}
    for coord in all_coords:
        row = coord[0]
        col = coord[1]
        risks[coord] = int(all_lines[row][col])
        nodes[coord] = Node(row, col)
    
    return risks, nodes, num_rows, num_cols


def get_neighbors(coord, num_rows, num_cols):
    r = coord[0]
    c = coord[1]
    neighbors = []
    if r - 1 >= 0:
        neighbors.append((r - 1, c))
    if r + 1 < num_rows:
        neighbors.append((r + 1, c))
    if c - 1 >= 0:
        neighbors.append((r, c - 1))
    if c + 1 < num_cols:
        neighbors.append((r, c + 1))
    
    return neighbors


def get_unvisited_node_with_smallest_dist(nodes, num_rows, num_cols):
    all_coords = [(r, c) for r in range(num_rows) for c in range(num_cols)]
    unvisited_coords = filter(lambda x: not nodes[x].visited and nodes[x].dist is not None, all_coords)
    min_dist = None
    min_coord = None
    for coord in unvisited_coords:
        node = nodes[coord]

        if min_dist is None or node.dist < min_dist:
            min_dist = node.dist
            min_coord = coord
    
    return min_coord


def get_path(nodes, start, end):
    path = [end]
    current_node = nodes[end]

    while current_node != nodes[start]:
        current_node = current_node.prev
        path.append((current_node.row, current_node.col))

    path.reverse()
    return path


def solve_a(risks, nodes, num_rows, num_cols):
    start = (0, 0)
    end = (num_rows - 1, num_cols - 1)
    current_coords = start
    current_node = nodes[current_coords]
    current_node.dist = 0

    while not nodes[end].visited:
        current_node = nodes[current_coords]

        nbrs = get_neighbors(current_coords, num_rows, num_cols)
        unvisited_nbrs = filter(lambda x: not nodes[x].visited, nbrs)
        min_dist = None
        for nbr in unvisited_nbrs:
            nbr_node = nodes[nbr]
            temp_dist = current_node.dist + risks[nbr]

            # Update the neighbor's tentative distance if it's smaller along
            # this path than it was the last time we checked that neighbor
            if nbr_node.dist is None or nbr_node.dist > temp_dist:
                nbr_node.dist = temp_dist
                nbr_node.prev = current_node
            
            # Keep track of the smallest distance among ALL nodes
            if min_dist is None or nbr_node.dist < min_dist:
                min_dist = nbr_node.dist
        
        current_node.visited = True
        current_coords = get_unvisited_node_with_smallest_dist(nodes, num_rows, num_cols)
    
    end_node = nodes[end]
    print('Destination node has distance {0}'.format(end_node.dist))

    # This isn't part of the puzzle, it's just for funsies.
    path = get_path(nodes, start, end)
    print(path)


def make_map_bigger(risks, factor, num_rows, num_cols):
    bigger_map = {}
    bigger_nodes = {}
    big_grid_coords = [(r, c) for r in range(factor) for c in range(factor)]
    for big_grid_coord in big_grid_coords:
        big_grid_row = big_grid_coord[0]
        big_grid_col = big_grid_coord[1]
        adder = big_grid_row + big_grid_col

        for k in risks:
            r = k[0]
            c = k[1]
            original_value = risks[k]
            new_value = (((original_value - 1) + adder) % 9) + 1  # wrap from 9 around to 1 (not 0)
            new_r = big_grid_row * num_rows + r
            new_c = big_grid_col * num_cols + c

            bigger_map[(new_r, new_c)] = new_value
            bigger_nodes[(new_r, new_c)] = Node(new_r, new_c)
    
    return bigger_map, bigger_nodes, num_rows * factor, num_cols * factor


def main():
    print('Reading input...')
    risks, nodes, num_rows, num_cols = read_input('./input.txt')
    print('Solving part A...')
    solve_a(risks, nodes, num_rows, num_cols)

    print('Making the larger map...')
    big_risks, big_nodes, big_num_rows, big_num_cols = make_map_bigger(risks, 5, num_rows, num_cols)
    print('Solving part B...')
    solve_a(big_risks, big_nodes, big_num_rows, big_num_cols)


if __name__ == '__main__':
    main()
