def correct_order(left, right) -> bool|None:
    if type(left) is int and type(right) is list:
        return correct_order([left], right)
    if type(left) is list and type(right) is int:
        return correct_order(left, [right])
    if type(left) is int and type(right) is int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    if type(left) is list and type(right) is list:
        if len(left) == 0 and len(right) == 0:
            return None
        elif len(left) == 0 and len(right) > 0:
            return True
        elif len(left) > 0 and len(right) == 0:
            return False
        else:
            order_of_first_elements = correct_order(left[0], right[0])
            if order_of_first_elements is None:
                return correct_order(left[1:], right[1:])
            else:
                return order_of_first_elements


def part1():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    all_lines = [line.strip() for line in all_lines]
    nonblank_lines = list(filter(lambda x: x != '', all_lines))
    pairs = list(zip(nonblank_lines[::2], nonblank_lines[1::2]))

    p1 = []
    p2 = []
    results = []
    for p1text, p2text in pairs:
        p1 = eval(p1text)
        p2 = eval(p2text)
        result = correct_order(p1, p2)
        results.append(result)
    
    indexed = enumerate(results)
    pairs_in_correct_order = filter(lambda x: x[1], indexed)
    index_sum = sum([i[0] + 1 for i in pairs_in_correct_order])
    print(f'Index sum of pairs in the correct order: {index_sum}')


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
