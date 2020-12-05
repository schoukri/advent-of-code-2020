import sys
import math

def main():
    ids = []
    for line in sys.stdin:
        seat = get_seat(line.rstrip())
        ids.append(seat["id"])
    ids.sort()
    print("PART 1: {}".format(ids[-1]))
    for i in range(len(ids)):
        if ids[i+1] - ids[i] > 1:
            print("PART 2: {}".format(ids[i]+1))
            break


def decode(token):
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
