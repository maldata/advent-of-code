class Sample:
    def __init__(self, raw_text) -> None:
        raw_text = raw_text.strip()
        parts = raw_text.split('|')
        raw_signals = parts[0].strip()
        raw_values = parts[1].strip()

        self.signals = raw_signals.split(' ')
        self.values = raw_values.split(' ')
        self._alphabetize_strings()

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
        self.string_to_integer = {}
    
    def decode(self) -> None:
        self.identify_all()

        d = {
            0: ['top', 'top-left', 'top-right', 'bottom', 'bottom-left', 'bottom-right'],
            1: ['top-right', 'bottom-right'],
            2: ['top', 'top-right', 'middle', 'bottom', 'bottom-left'],
            3: ['top', 'top-right', 'middle', 'bottom', 'bottom-right'],
            4: ['top-left', 'top-right', 'middle', 'bottom-right'],
            5: ['top', 'top-left', 'middle', 'bottom', 'bottom-right'],
            6: ['top', 'top-left', 'middle', 'bottom', 'bottom-left', 'bottom-right'],
            7: ['top', 'top-right', 'bottom-right'],
            8: ['top', 'top-left', 'top-right', 'middle', 'bottom', 'bottom-left', 'bottom-right'],
            9: ['top', 'top-left', 'top-right', 'middle', 'bottom', 'bottom-right']
        }

        for k in d:
            segments = d[k]
            chars = [self.char_map[s] for s in segments]
            chars.sort()
            self.string_to_integer[''.join(chars)] = k
        
        digits = [self.string_to_integer[v] for v in self.values]
        digits_as_chars = [str(d) for d in digits]
        final_value_str = ''.join(digits_as_chars)
        return int(final_value_str)

    def identify_all(self) -> None:
        self.identify_top()
        self.identify_bottom_right()
        self.identify_top_right()
        self.identify_middle()
        self.identify_top_left()
        self.identify_bottom()
        self.identify_bottom_left()

    def _string_to_set(self, string) -> None:
        exploded_str = [i for i in string]
        return set(exploded_str)

    def _alphabetize_string(self, string) -> None:
        exploded = [i for i in string]
        exploded.sort()
        return ''.join(exploded)

    def _alphabetize_strings(self) -> None:
        self.signals = [self._alphabetize_string(s) for s in self.signals]
        self.values = [self._alphabetize_string(v) for v in self.values]

    def identify_top(self) -> None:
        # Take the 1 and 7 (the only ones with 2 and 3 segments respectively)
        # and find the diff. The different segment is the top.
        set1 = self._string_to_set(self.signal_length_map[2][0])
        set7 = self._string_to_set(self.signal_length_map[3][0])
        diff = set7 - set1
        top_char = list(diff)[0]
        self.char_map['top'] = top_char
        self.char_map_inv[top_char] = 'top'
    
    def identify_bottom_right(self) -> None:
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
        set1 = self._string_to_set(self.signal_length_map[2][0])
        btmright = self.char_map['bottom-right']
        topright = set1 - set(btmright)
        topright = list(topright)[0]
        self.char_map['top-right'] = topright
        self.char_map_inv[topright] = 'top-right'

    def identify_middle(self) -> None:
        # Get the intersection of all 5-segment digits (to get top, middle, and bottom)
        # and the single 4-segment digit
        five_chars = [self._string_to_set(s) for s in self.signal_length_map[5]]
        four_chars = self._string_to_set(self.signal_length_map[4][0])
        isect = four_chars.intersection(*five_chars)
        middle = list(isect)[0]
        self.char_map['middle'] = middle
        self.char_map_inv[middle] = 'middle'
        
    def identify_top_left(self) -> None:
        # Take the four (the only thing with 4 segments) and remove the 
        # top right, bottom right, and middle
        four_char_string = [c for c in self.signal_length_map[4][0]]
        for f in four_char_string:
            if f not in self.char_map_inv:
                self.char_map['top-left'] = f
                self.char_map_inv[f] = 'top-left'

    def identify_bottom(self) -> None:
        # Get the intersection of all 5-segment digits (to get top, middle, and bottom)
        # and then remove the top and middle
        five_chars = [self._string_to_set(s) for s in self.signal_length_map[5]]
        all_segments = self._string_to_set(self.signal_length_map[7][0])
        isect = all_segments.intersection(*five_chars)
        top_and_middle = set([self.char_map['top'], self.char_map['middle']])
        diff = isect - top_and_middle
        bottom = list(diff)[0]
        self.char_map['bottom'] = bottom
        self.char_map_inv[bottom] = 'bottom'

    def identify_bottom_left(self) -> None:
        # Get all the segments and remove everything we know already.
        all_segments = self._string_to_set(self.signal_length_map[7][0])
        for i in self.char_map_inv:
            all_segments.discard(i)
        btmleft = list(all_segments)[0]
        self.char_map['bottom-left'] = btmleft
        self.char_map_inv[btmleft] = 'bottom-left'


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
    total = 0
    for s in segment_data:
        total = total + s.decode()
    print('The total is {0}'.format(total))

def main():
    num_segments = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
    segment_data = read_input('./input.txt')
    solve_a(num_segments, segment_data)
    solve_b(segment_data)


if __name__ == '__main__':
    main()
