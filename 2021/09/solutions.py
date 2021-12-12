def read_map(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    all_rows = [row.strip() for row in all_lines]
    height_map = []
    for row in all_rows:
        height_map.append([int(r) for r in row])
    
    return height_map


def solve_a(height_map) -> None:
    low_points = []
    num_rows = len(height_map)
    num_cols = len(height_map[0])
    for r in range(num_rows):
        for c in range(num_cols):
            row = height_map[r]
            current = row[c]
            neighbors = []

            if r > 0:
                neighbors.append(height_map[r-1][c])
            
            if r < num_rows-1 :
                neighbors.append(height_map[r+1][c])
            
            if c > 0:
                neighbors.append(row[c-1])

            if c < num_cols-1:
                neighbors.append(row[c+1])

            if current < min(neighbors):
                low_points.append(current)

    risk_level = [l+1 for l in low_points]
    print('Total risk level is {0}'.format(sum(risk_level)))


def basin_search(height_map, num_rows, num_cols, basins, r, c, basin_num):
    neighbors = []
    if r > 0:
        neighbors.append((r-1, c))
            
    if r < num_rows-1 :
        neighbors.append((r+1, c))
    
    if c > 0:
        neighbors.append((r, c-1))

    if c < num_cols-1:
        neighbors.append((r, c+1))

    for n in neighbors:
        if n not in basins:
            basins[n] = basin_num
            basin_search(height_map, num_rows, num_cols, basins, n[0], n[1], basin_num)


def solve_b(height_map) -> None:
    # keys are coordinates (row, col), values are basin number.
    # all 9s go in basin number -1. 
    basins = {}
    num_rows = len(height_map)
    num_cols = len(height_map[0])
    for r in range(num_rows):
        for c in range(num_cols):
            current = height_map[r][c]
            if current == 9:
                basins[(r,c)] = -1
    
    basin_num = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if (r,c) in basins:
                continue
            else:
                basins[(r,c)] = basin_num
                basin_search(height_map, num_rows, num_cols, basins, r, c, basin_num)
                basin_num = basin_num + 1
    
    inv_map = {}
    for r in range(num_rows):
        for c in range(num_cols):
            if (r,c) not in basins:
                print('Somehow ({0}, {1}) is not in a basin'.format(r,c))
            else:
                basin_num = basins[(r,c)]
                if basin_num in inv_map:
                    inv_map[basin_num] = inv_map[basin_num] + [(r,c)]
                else:
                    inv_map[basin_num] = [(r,c)]
    
    basin_sizes = []
    for k in inv_map:
        if k >= 0:
            basin_sizes.append((k, len(inv_map[k])))
    basin_sizes.sort(key=lambda x: x[1], reverse=True)
    
    p = basin_sizes[0][1] * basin_sizes[1][1] * basin_sizes[2][1]
    print('The product of the sizes of the three largest basins is {0}'.format(p))


def main():
    height_map = read_map('./input.txt')
    solve_a(height_map)
    solve_b(height_map)


if __name__ == '__main__':
    main()
