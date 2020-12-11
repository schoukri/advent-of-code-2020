#!/usr/bin/env python3

import sys, re

class Grid:
    _toggle = {'L': '#', '#': 'L'}
    _offsets = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1, 0)]

    def __init__(self, lines):
        self.data = []
        for y in range(len(lines)):
            self.data.append(list(lines[y][x] for x in range(len(lines[y]))))
        self.maxy = len(self.data) - 1
        self.maxx = len(self.data[0]) - 1

    def __repr__(self):
        return "\n".join(list(''.join(row) for row in self.data))

    def rearrange(self, adjacent_only, flip_occupied_min):
        flip = list()
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                status = self.data[y][x]
                if status == '.':
                    continue
                count = self.visible_occupied(x, y, adjacent_only)
                if status == 'L' and count == 0:
                    flip.append((x, y))
                elif status == '#' and count >= flip_occupied_min:
                    flip.append((x, y))
        for (x, y) in flip:
            self.data[y][x] = self._toggle[self.data[y][x]]
        return len(flip)

    def visible_occupied(self, x, y, adjacent_only=True):
        count = 0
        for (dx, dy) in self._offsets:
            (ax, ay) = (x, y)
            while True:
                ax += dx
                ay += dy
                if ax < 0 or ax > self.maxx or ay < 0 or ay > self.maxy:
                    break
                if self.data[ay][ax] == '#':
                    count += 1
                    break
                elif self.data[ay][ax] == 'L':
                    break
                if adjacent_only:
                    break
        return count

    def total_occupied(self):
        total = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                if self.data[y][x] == '#':
                    total += 1
        return total


if __name__ == '__main__':
    lines = list(line for line in re.split("\n", sys.stdin.read().rstrip()))

    grid1 = Grid(lines)
    while grid1.rearrange(True, 4) > 0:
        pass
    print("PART 1:", grid1.total_occupied())

    grid2 = Grid(lines)
    while grid2.rearrange(False, 5) > 0:
        pass
    print("PART 2:", grid2.total_occupied())
