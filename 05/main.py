import sys
import math
import re

def main():
    ids = []
    for line in sys.stdin:
        seat = get_seat(line.rstrip())
        ids.append(seat["id"])
    ids.sort()
    print("PART 1:", ids[-1])
    for i in range(len(ids)):
        if ids[i+1] - ids[i] > 1:
            print("PART 2:", ids[i]+1)
            break

def decode(token):
    """Convert the token to a valid binary string, then cast it to an int."""
    token = re.sub(r'[BR]', '1', token)
    token = re.sub(r'[FL]', '0', token)
    return int(token, 2)

def decode_bitset(token):
    """The token strings are just binary numbers in disguise: B and R are where the bits are set"""
    (num, bit) = (0, len(token)-1)
    for c in token:
        if c == 'B' or c == 'R':
            num |= (1<<bit)
        bit -= 1
    return num

def decode_binary_search(token):
    """Use a binary search method to decode the token."""
    (low, high) = (0, 2**len(token)-1)
    for c in token:
        mid = (low + high) / 2
        if c == 'B' or c == 'R':
            low = math.ceil(mid)
        elif c == 'F' or c == 'L':
            high = math.floor(mid)
        #print("c={}, low={}, mid={}, high={}".format(c, low, mid, high))
    return low

def get_seat(token):
    row = decode(token[0:7])
    col = decode(token[7:])
    id = (row * 8) + col
    return {"id": id, "row": row, "col": col}

if __name__ == '__main__':
    main()
