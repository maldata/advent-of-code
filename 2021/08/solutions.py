class Sample:
    def __init__(self, raw_text) -> None:
        raw_text = raw_text.strip()
        parts = raw_text.split('|')
        raw_signals = parts[0].strip()
        raw_values = parts[1].strip()

        self.signals = raw_signals.split(' ')
        self.values = raw_values.split(' ')

        self.signal_length_map = {}
        for signal in self.signals:
            if len(signal) in self.signal_length_map:
                self.signal_length_map[len(signal)].append(signal)
            else:
                self.signal_length_map[len(signal)] = [signal]

        #  ---               top
        # |   |  top left         top right
        #  ---              middle
        # |   |  bottom left     bottom right
        #  ---              bottom
        self.char_map = {}
        self.char_map_inv = {}
    
    def decode(self) -> None:
        self.identify_top()
        self.identify_bottom_left()
        self.identify_top_right()
        pass

    def _string_to_set(self, string) -> None:
        exploded_str = [i for i in string]
        return set(exploded_str)

    def identify_top(self) -> None:
        # Take the 1 and 7 (the only ones with 2 and 3 segments respectively)
        # and find the diff. The different segment is the top.
        set1 = self._string_to_set(self.signal_length_map[2][0])
        set7 = self._string_to_set(self.signal_length_map[3][0])
        diff = set7 - set1
        top_char = list(diff)[0]
        self.char_map['top'] = top_char
        self.char_map_inv[top_char] = 'top'
    
    def identify_bottom_left(self) -> None:
        set1 = self._string_to_set(self.signal_length_map[2][0])
        six_chars = [self._string_to_set(s) for s in self.signal_length_map[6]]

        # Take the intersection of the segments in the 1 and each of the
        # six-segment digits. If there's only one segment in the intersection,
        # then that's the bottom-right.
        for s in six_chars:
            isect = set1.intersection(s)
            if len(list(isect)) == 1:
                btmright = list(isect)[0]
                self.char_map['bottom-right'] = btmright
                self.char_map_inv[btmright] = 'bottom-right'
                break
    
    def identify_top_right(self) -> None:
        # Just remove the bottom-right segment from the 1 digit's two segments
        pass

    def identify_top_left(self) -> None:
        # Diff 5 and 2, remove 1, remove bottom left
        pass

    def identify_bottom_right(self) -> None:
        # Look at 5 & 2 again
        pass


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
    for s in segment_data:
        value_lengths = [len(i) for i in s.values]
        values_with_unique_lengths = filter(lambda x: x in num_segments_in_singles, value_lengths)
        num_vals_unique_len = len(list(values_with_unique_lengths))
        num_outputs_with_unique_segments = num_outputs_with_unique_segments + num_vals_unique_len
    
    print("{0} of the output values have the 'unique' lengths".format(num_outputs_with_unique_segments))

def solve_b(segment_data):
    for s in segment_data:
        s.decode()


def main():
    num_segments = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
    segment_data = read_input('./input.txt')
    solve_a(num_segments, segment_data)
    solve_b(segment_data)


if __name__ == '__main__':
    main()
