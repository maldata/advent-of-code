


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    algorithm_line = all_lines[0].strip()
    return algorithm_line, [i.strip() for i in all_lines[2:]]


def inflate_image(img):
    """
    Surround the whole image with a border of 3 more rows/columns of dark pixels (.)
    """
    orig_img_row_len = len(img[0])
    new_img_row_len = orig_img_row_len + 6
    all_dark = '.' * new_img_row_len
    
    new_image = [all_dark, all_dark, all_dark]
    for row in img:
        new_image.append('...' + row + '...')
    
    new_image.extend([all_dark, all_dark, all_dark])
    return new_image


def enhance(algorithm, image):
    num_rows = len(image)
    num_cols = len(image[0])

    for row_idx in range(num_rows):
        if row_idx == 0 or row_idx == num_rows - 1:
            continue

        for col_idx in range(len(num_cols)):
            if col_idx == 0 or col_idx == num_cols - 1:
                continue

            # TODO: get the 3x3 pixels around the current position
            # TODO: assemble the binary value
            # TODO: look up the 9-bit address in the algorithm string
            


def strip_border(image):
    """
    Remove a one-pixel-wide border from the image
    """
    new_image = []
    for line in image:
        new_image.append(line[1:-1])
    
    return new_image[1:-1]


def solve_a(algorithm, image):
    inflated_img = inflate_image(image)
    enhanced_img = enhance(algorithm, inflated_img)
    stripped_img = strip_border(enhanced_img)
    pass


def main():
    algorithm, image = read_input('./input.txt')
    solve_a(algorithm, image)


if __name__ == '__main__':
    main()
