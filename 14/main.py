#!/usr/bin/env python3.8

import sys, re, itertools, collections

mask_re = re.compile(r'^mask = ([X01]{36})$')
mem_re = re.compile(r'^mem\[(\d+)\] = (\d+)$')

def part_1(lines: list) -> str:
    mem = collections.Counter()
    mask_ones = 0
    mask_zeros = 0
    for line in lines:
        if mask_match := mask_re.search(line):
            mask_str = mask_match.group(1)
            mask_ones = int(mask_str.replace('X', '0'), 2)
            mask_zeros = int(mask_str.replace('X', '1'), 2)
        elif mem_match := mem_re.search(line):
            address = int(mem_match.group(1))
            value = int(mem_match.group(2))
            value |= mask_ones
            value &= mask_zeros
            mem[address] = value
    return sum(mem.values())

def part_2(lines: list) -> int:
    mem = collections.Counter()
    mask_str = None
    for line in lines:
        if mask_match := mask_re.search(line):
            mask_str = mask_match.group(1)
        elif mem_match := mem_re.search(line):
            address = int(mem_match.group(1))
            value = int(mem_match.group(2))
            address_bits = to_bitstring(address)
            new_mask_list = [address_bits[i] if bit == '0' else bit for (i, bit) in enumerate(mask_str)]
            new_mask_str = ''.join(new_mask_list)
            for mask in combinations(new_mask_str):
                mem[mask] = value
    return sum(mem.values())


def combinations(mask_str: str) -> iter:
    xcount = mask_str.count('X')
    for combo in itertools.product('01', repeat=xcount):
        combo = iter(combo)
        mask_list = [c if c != 'X' else next(combo) for c in list(mask_str)]
        yield int(''.join(mask_list), 2)

def to_bitstring(n: int) -> str:
    return "{0:036b}".format(n)

if __name__ == '__main__':
    lines = open('input.txt').readlines()
    print("PART 1:", part_1(lines))
    print("PART 2:", part_2(lines))
