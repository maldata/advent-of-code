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


def flatten_expr(expr):
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
    with open('./test-input1.txt', 'r') as f:
        expr = f.readlines()

    expr = expr[0]
    expr = expr.strip()

    flattened_expr = flatten_expr(expr)
    result = flat_evaluate(flattened_expr)
    print(result)


if __name__ == '__main__':
    main()
