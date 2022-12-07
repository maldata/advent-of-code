def part1(num_unique):
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    data = all_lines[0].strip()

    start = num_unique - 1
    for idx in range(start, len(data)):
        subset = data[idx - start : idx + 1]
        subset_chars = set([s for s in subset])
        if len(subset_chars) == num_unique:
            print(f'Start of packet at {idx + 1}')
            break


if __name__ == '__main__':
    part1(4)
    part1(14)
