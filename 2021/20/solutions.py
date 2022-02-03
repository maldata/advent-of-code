def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    algorithm_line = all_lines[0].strip()

    prepared_lines = [i.strip() for i in all_lines[2:]]
    num_rows = len(prepared_lines)
    num_cols = len(prepared_lines[0])

    image = {}
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            coords = (col_idx, row_idx)
            image[coords] = prepared_lines[row_idx][col_idx]

    return algorithm_line, image


def _get_neighbor_coords(coord):
    """
    Returns the 3x3 neighbor coordinates in left -> right, top -> bottom order
    """
    x = coord[0]
    y = coord[1]
    return [(j, i) for i in range(y - 1, y + 2) for j in range(x - 1, x + 2)]


def _get_pixel_string(neighbors, image, outside_value):
    pixel_string = ''
    for n in neighbors:
        if n in image:
            pixel_string = pixel_string + image[n]
        else:
            pixel_string = pixel_string + outside_value
    
    return pixel_string


def _get_new_pixel(pixel_string, algorithm):
    translation_table = str.maketrans('.#', '01')
    binary_string = pixel_string.translate(translation_table)
    addr = int(binary_string, 2)
    return algorithm[addr]


def enhance(algorithm, image, outside_value):
    zipped = list(zip(*list(image.keys())))
    x_min = min(zipped[0]) - 1
    x_max = max(zipped[0]) + 1
    y_min = min(zipped[1]) - 1
    y_max = max(zipped[1]) + 1

    new_image = {}
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            coord = (x, y)
            neighbors = _get_neighbor_coords(coord)
            pixel_string = _get_pixel_string(neighbors, image, outside_value)
            new_pixel = _get_new_pixel(pixel_string, algorithm)
            new_image[coord] = new_pixel
    
    return new_image


def solve_a(algorithm, image, num_iterations):
    outside_value = '.'
    for iteration in range(num_iterations):
        image = enhance(algorithm, image, outside_value)
        if outside_value == '#':
            outside_value = '.'
        else:
            outside_value = '#'

    num_lit_pixels = 0
    for k in image:
        if image[k] == '#':
            num_lit_pixels = num_lit_pixels + 1
    
    print('There are {0} lit pixels'.format(num_lit_pixels))


def main():
    algorithm, image = read_input('./input.txt')
    solve_a(algorithm, image, 2)

    algorithm, image = read_input('./input.txt')
    solve_a(algorithm, image, 50)


if __name__ == '__main__':
    main()
