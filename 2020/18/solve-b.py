#!/usr/bin/env python3
import re


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
    Evaluate addition BEFORE multiplication.
    We expect that there are no parentheses in the flat evaluation.
    """
    while True:
        m = re.search('([0-9]+)\s*\+\s*([0-9]+)', expr)
        if m is None:
            break

        op1 = int(m.group(1))
        op2 = int(m.group(2))
        result = op1 + op2

        s1 = m.span(1)
        s2 = m.span(2)
        start_idx = s1[0]
        end_idx = s2[1]

        pre = expr[:start_idx]
        post = expr[end_idx:]

        expr = pre + str(result) + post

    while True:
        m = re.search('([0-9]+)\s*\*\s*([0-9]+)', expr)
        if m is None:
            break

        op1 = int(m.group(1))
        op2 = int(m.group(2))
        result = op1 * op2

        s1 = m.span(1)
        s2 = m.span(2)
        start_idx = s1[0]
        end_idx = s2[1]

        pre = expr[:start_idx]
        post = expr[end_idx:]

        expr = pre + str(result) + post

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
