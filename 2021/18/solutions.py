import re

class SfNumber:
    def __init__(self, string_representation, parent=None) -> None:
        self.parent = parent

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
            self.left = SfNumber(left_str, self)

        try:
            self.right = int(right_str)
        except ValueError:
            self.right = SfNumber(right_str, self)
    

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

    def magnitude(self):
        mag = 0
        if isinstance(self.left, int):
            mag = mag + (3 * self.left)
        else:
            mag = mag + (3 * self.left.magnitude())
        
        if isinstance(self.right, int):
            mag = mag + (2 * self.right)
        else:
            mag = mag + (2 * self.right.magnitude())
        
        return mag

    def reduce(self):
        while True:
            if self.check_explode():
                continue
            if self.check_split():
                continue
            break
    
    def check_explode(self, depth=0):
        if depth >= 4 and isinstance(self.left, int) and isinstance(self.right, int):
            self.explode()
            return True
        
        left_result = False
        if isinstance(self.left, SfNumber):
            left_result = self.left.check_explode(depth=depth + 1)
        if left_result is True:
            return True

        if isinstance(self.right, SfNumber):
            return self.right.check_explode(depth=depth + 1)

        return False

    def explode(self):
        left_val = self.left
        right_val = self.right

        # The left value gets added to the next value to the left.
        # Keep going up nodes until the parent is None or until the node we're
        # on is its parent's right node. Once that happens, go down the left side
        # and look for the right-most int.
        current = self
        while True:
            p = current.parent
            if p is None:
                # We went all the way up to the root of the tree. Must not be anything to
                # the left, so we do nothing.
                break

            if current is p.right:
                branch = p.left
                if isinstance(branch, int):
                    p.left = branch + left_val
                else:
                    while isinstance(branch, SfNumber):
                        p = branch
                        branch = branch.right
                    p.right = branch + left_val
                break

            else:
                current = p

        # The right value gets added to the next value to the right.
        # Keep going up nodes until the parent is None or until the node we're
        # on is its parent's left node. Once that happens, go down the right side
        # and look for the left-most int.
        current = self
        while True:
            p = current.parent
            if p is None:
                # We went all the way up to the root of the tree. Must not be anything to
                # the right, so we do nothing.
                break

            if current is p.left:
                branch = p.right
                if isinstance(branch, int):
                    p.right = branch + right_val
                else:
                    while isinstance(branch, SfNumber):
                        p = branch
                        branch = branch.left
                    p.left = branch + right_val
                break

            else:
                current = p
        
        # Now that all of that is done, we replace the parent's reference to
        # the exploded node with a scalar zero.
        p = self.parent
        if self is p.left:
            p.left = 0
        else:
            p.right = 0

    def check_split(self):
        if isinstance(self.left, int) and self.left > 9:
            self.split_left()
            return True
        
        if isinstance(self.right, int) and self.right > 9:
            self.split_right()
            return True

        left_result = False
        if isinstance(self.left, SfNumber):
            left_result = self.left.check_split()
        if left_result is True:
            return left_result
        
        if isinstance(self.right, SfNumber):
            return self.right.check_split()
        
        return False

    def split_number_to_str(self, num):
        new_left = num // 2
        new_right = num - new_left
        return '[{0},{1}]'.format(new_left, new_right)

    def split_left(self):
        new_node_str = self.split_number_to_str(self.left)
        new_node = SfNumber(new_node_str, self)
        self.left = new_node

    def split_right(self):
        new_node_str = self.split_number_to_str(self.right)
        new_node = SfNumber(new_node_str, self)
        self.right = new_node


def add_sfns(sfn1, sfn2):
    result_str = '[' + sfn1.get_string_repr() + ',' + sfn2.get_string_repr() + ']'
    result_sfn = SfNumber(result_str)
    result_sfn.reduce()
    return result_sfn


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    return [SfNumber(line.strip()) for line in all_lines]


def solve_a(sfns):
    result = sfns[0]
    for sfn in sfns[1:]:
        result = add_sfns(result, sfn)

    print('Final magnitude {0}'.format(result.magnitude()))


def solve_b(sfns):
    combos = [(a, b) for a in sfns for b in sfns]
    mags = []
    for combo in combos:
        a = combo[0]
        b = combo[1]
        result = add_sfns(a, b)
        mags.append(result.magnitude())

    print('Largest magnitude of any combination is {0}'.format(max(mags)))

def main():
    sfnumbers = read_input('./input.txt')
    solve_a(sfnumbers)
    solve_b(sfnumbers)


if __name__ == '__main__':
    main()
