import re

class SfNumber:
    def __init__(self, string_representation) -> None:
        # I'm sure some kinda regex would get this done, but... yikes.
        m = re.match('\[(.+)\]', string_representation)
        inner = m.group(1)
        exploded = [i for i in inner]
        closings = 0
        for e_idx in range(len(exploded)):
            e = exploded[e_idx]
            if e == '[':
                closings = closings + 1
            elif e == ']':
                closings = closings - 1
            elif e == ',' and closings == 0:
                break

        left_str = inner[:e_idx]
        right_str = inner[e_idx + 1:]

        try:
            self.left = int(left_str)
        except ValueError:
            self.left = SfNumber(left_str)

        try:
            self.right = int(right_str)
        except ValueError:
            self.right = SfNumber(right_str)
    
    def copy(self):
        new_sfn = SfNumber(self.get_string_repr())

    def get_string_repr(self):
        if isinstance(self.left, int):
            left_str = str(self.left)
        else:
            left_str = self.left.get_string_repr()
        
        if isinstance(self.right, int):
            right_str = str(self.right)
        else:
            right_str = self.right.get_string_repr()
        return '[{0},{1}]'.format(left_str, right_str)

    def reduce(self):
        while True:
            if self.check_explode():
                continue
            if self.check_split():
                continue
            break
    
    def check_explode(self, depth=0):
        left_exploded = False
        right_exploded = False

        if not isinstance(self.left, int):
            left_exploded = self.left.check_explode(depth=depth + 1)


def add_sfns(sfn1, sfn2):
    result_str = '[' + sfn1.get_string_repr() + ',' + sfn2.get_string_repr() + ']'
    result_sfn = SfNumber(result_str)
    result_sfn.reduce()
    return result_sfn


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    return [SfNumber(line.strip()) for line in all_lines]


def main():
    sfnumbers = read_input('./input.txt')
    result = add_sfns(sfnumbers[0], sfnumbers[1])
    pass


if __name__ == '__main__':
    main()
