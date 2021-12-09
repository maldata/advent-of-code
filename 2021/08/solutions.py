class Sample:
    def __init__(self, raw_text) -> None:
        raw_text = raw_text.strip()
        parts = raw_text.split('|')
        raw_signals = parts[0].strip()
        raw_values = parts[1].strip()

        self.signals = raw_signals.split(' ')
        self.values = raw_values.split(' ')


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()

    all_samples = [Sample(i) for i in all_lines]
    return all_samples


def solve_a(num_segments, segment_data):
    # Find the values in the dictionary that are only in there once
    values = [num_segments[k] for k in num_segments]
    num_occurrences = [values.count(v) for v in values]
    singles = filter(lambda x: num_occurrences[x] == 1, range(len(values)))
    num_segments_in_singles = [num_segments[i] for i in singles]
    
    num_outputs_with_unique_segments = 0        


def solve_b(pos):
    pass


def main():
    num_segments = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
    segment_data = read_input('./input.txt')
    solve_a(num_segments, segment_data)
    # solve_b(positions)


if __name__ == '__main__':
    main()
