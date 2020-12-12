#!/usr/bin/env python3

import sys, re

class Grid:

    _toggle = {'L': '#', '#': 'L'}
    _offsets = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1, 0)]

    def __init__(self, lines):
        self.data = list([char for char in row] for row in lines)
        self.maxy = len(self.data) - 1
        self.maxx = max(len(row) for row in self.data) - 1

    def __repr__(self):
        return "\n".join(''.join(row) for row in self.data)

    def rearrange(self, adjacent_only, flip_occupied_min):
        flip = list()
        for (y, row) in enumerate(self.data):
            for (x, cell) in enumerate(row):
                if cell == '.':
                    continue
                count = self.visible_occupied(x, y, adjacent_only)
                if cell == 'L' and count == 0:
                    flip.append((x, y))
                elif cell == '#' and count >= flip_occupied_min:
                    flip.append((x, y))
        for (x, y) in flip:
            self.data[y][x] = self._toggle[self.data[y][x]]
        return len(flip)

    def visible_occupied(self, x, y, adjacent_only=True):
        count = 0
        for (dx, dy) in self._offsets:
            (ax, ay) = (x + dx, y + dy)
            while 0 <= ax <= self.maxx and 0 <= ay <= self.maxy:
                if self.data[ay][ax] == '#':
                    count += 1
                    break
                elif self.data[ay][ax] == 'L':
                    break
                if adjacent_only:
                    break
                ax += dx
                ay += dy
        return count

    def total_occupied(self):
        return sum(1 for row in self.data for seat in row if seat == '#')

if __name__ == '__main__':
    lines = list(line for line in re.split("\n", sys.stdin.read().rstrip()))

    grid1 = Grid(lines)
    while grid1.rearrange(adjacent_only=True, flip_occupied_min=4) > 0:
        pass
    print("PART 1:", grid1.total_occupied())

    grid2 = Grid(lines)
    while grid2.rearrange(adjacent_only=False, flip_occupied_min=5) > 0:
        pass
    print("PART 2:", grid2.total_occupied())
