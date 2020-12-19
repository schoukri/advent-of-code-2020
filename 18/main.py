#!/usr/bin/env python3

import re
from typing import List

def main():
    #tests()
    lines = [line.rstrip("\n") for line in open('input.txt').readlines()]
    part1 = sum([evaluate(1, line) for line in lines])
    print("PART 1:", part1)
    part2 = sum([evaluate(2, line) for line in lines])
    print("PART 2:", part2)

def get_replacements(part: int) -> List[tuple]:
    # compiled regexps and their replacement values (string or callable function)
    pair_add = (re.compile(r'(\d+) (\+) (\d+)'), pair_replace)
    pair_add_or_mult = (re.compile(r'(\d+) ([*+]) (\d+)'), pair_replace)
    parens_add = (re.compile(r'(\()(\d+) (\+) (\d+)([^\)]*\))'), parens_replace)
    parens_add_or_mult = (re.compile(r'(\()(\d+) ([+*]) (\d+)([^\(\)]*\))'), parens_replace)
    parens_single = (re.compile(r'\((\d+)\)'), r'\g<1>')

    # order is important: each pattern is run in the specified order
    if part == 1:
        return [
            parens_single,
            parens_add_or_mult,
            pair_add_or_mult,
        ]
    elif part == 2:
        return [
            parens_single,
            parens_add,
            pair_add,
            parens_add_or_mult,
            pair_add_or_mult,
        ]

def evaluate(part: int, expression: str) -> int:
    final_re = re.compile(r'^\d+$')
    replacements = get_replacements(part)
    (curr, last) = (expression, '')
    while True:
        for (pattern_re, replacement) in replacements:
            last = pattern_re.sub(replacement, curr, count=1)
            if last != curr:
                break
        if last != curr:
            curr = last
            continue
        if final_re.match(curr):
            return int(curr)
        break

def parens_replace(match: re.Match) -> str:
    opening = match.group(1)
    a = int(match.group(2))
    op = match.group(3)
    b = int(match.group(4))
    closing = match.group(5)
    return opening + str(calc(a, b, op)) + closing

def pair_replace(match: re.Match) -> str:
    a = int(match.group(1))
    op = match.group(2)
    b = int(match.group(3))
    return str(calc(a, b, op))

def calc(a: int, b: int, op: str) -> int:
    if op == '+':
        return a + b
    elif op == '*':
        return a * b


def tests():
    # input expression => tuple of expected values for part 1 and part2
    tests = {
        '1 + 2 * 3 + 4 * 5 + 6': (71, 231),
        '1 + (2 * 3) + (4 * (5 + 6))': (51, 51),
        '2 * 3 + (4 * 5)': (26, 46),
        '5 + (8 * 3 + 9 + 3 * 4 * 3)': (437, 1445),
        '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))': (12240, 669060),
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2': (13632, 23340),
    }
    for part in [1, 2]:
        for (expression, expected) in tests.items():
            assert(evaluate(part, expression) == expected[part-1])


if __name__ == '__main__':
    main()
