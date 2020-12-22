#!/usr/bin/env python3
import re


def get_next_operand(expr):
    r = re.match('^([0-9]+)', expr)
    op = r.group(1)

    span = r.span(1)
    span_end = span[1]
    remaining_expr = expr[span_end:]
    remaining_expr = remaining_expr.strip()

    return int(op), remaining_expr


def get_next_operator(expr):
    r = re.match('^([\*\+])', expr)
    operator = r.group(1)

    span = r.span(1)
    span_end = span[1]
    remaining_expr = expr[span_end:]
    remaining_expr = remaining_expr.strip()

    return operator, remaining_expr


def find_innermost_parenthetical(expr):
    """
    Given the expression expr, find the innermost parenthetical expression.
    Return a tuple containing the index and length.
    """
    # First find a closing parenthesis
    close_paren_idx = expr.index(')')

    # From there, backtrack until you find the nearest opening parenthesis before it
    open_offset = expr[:close_paren_idx][::-1].index('(')
    open_idx = close_paren_idx - open_offset - 1
    length = close_paren_idx - open_idx + 1

    return open_idx, length


def replace_parenthetical(expr, index, length):
    pre = expr[:index]
    post = expr[index + length:]

    parenthetical = expr[index:index + length]

    # Strip off the enclosing parentheses
    contents = parenthetical.strip('()')

    flattened = pre + str(flat_evaluate(contents)) + post
    return flattened


def flatten_expr(expr):
    expr = expr.strip()
    while expr.count('(') != 0:
        paren = find_innermost_parenthetical(expr)
        expr = replace_parenthetical(expr, paren[0], paren[1])

    return expr


def flat_evaluate(expr):
    """
    Chew through the expression from left to right.
    We expect that there are no parentheses in the flat evaluation,
    and that we start with an operand.
    """
    result, remaining_expr = get_next_operand(expr)
    while remaining_expr != '':
        operator, remaining_expr = get_next_operator(remaining_expr)
        operand2, remaining_expr = get_next_operand(remaining_expr)

        if operator == '+':
            result = result + operand2
        elif operator == '*':
            result = result * operand2
        else:
            print('"{0}" is not a valid operator'.format(operator))
            return 0

    return result


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    expressions = [i.strip() for i in all_lines]

    sum_of_exprs = 0
    for expr in expressions:
        flattened_expr = flatten_expr(expr)
        result = flat_evaluate(flattened_expr)
        sum_of_exprs = sum_of_exprs + result

    print(sum_of_exprs)


if __name__ == '__main__':
    main()
