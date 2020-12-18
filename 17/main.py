#!/usr/bin/env python3

import numpy as np
from typing import List
from itertools import product

class Cube:
    def __init__(self, lines: list, cycles: int):
        self.cycles = cycles
        self.y = len(lines) + (cycles * 2)
        self.x = len(lines[0]) + (cycles * 2)
        self.z = 1 + (cycles * 2)
        self.data = np.zeros([self.y, self.x, self.z], dtype=np.bool)
        for (y, line) in enumerate(lines):
            for (x, cell) in enumerate(line):
                if cell == '#':
                    self.data[y+cycles, x+cycles, 0+cycles] = True

    def active_count(self):
        return np.count_nonzero(self.data)

    def neighbors(self, coords: tuple) -> List[tuple]:
        neighbors = []
        for offset in product((-1, 0, 1), repeat=self.data.ndim):
            neighbor = tuple(map(sum, zip(coords, offset)))
            if coords == neighbor or -1 in neighbor:
                # skip if neighbor equals input coord or if it has any negative index values
                continue
            if len(list(filter(lambda x: x[0] >= x[1], zip(neighbor, self.data.shape)))):
                # skip if neighbor has an index values greater than the max dimenions
                continue
            neighbors.append(neighbor)
        return neighbors

    def run_cycles(self):
        for n in range(self.cycles):
            flips = []
            it = np.nditer(self.data, flags=['multi_index'])
            for item in it:
                coords = it.multi_index
                active_count = sum(1 for n in self.neighbors(coords) if self.data[n])
                if item == True and active_count not in (2,3):
                    flips.append(coords)
                elif item == False and active_count == 3:
                    flips.append(coords)
            for coords in flips:
                self.data[coords] = not self.data[coords]


class HyperCube(Cube):
    def __init__(self, lines: list, cycles: int):
        super().__init__(lines, cycles)
        self.w = 1 + (cycles * 2)
        self.data = np.zeros([self.y, self.x, self.z, self.w], dtype=np.bool)
        for (y, line) in enumerate(lines):
            for (x, cell) in enumerate(line):
                if cell == '#':
                    self.data[y+cycles, x+cycles, 0+cycles, 0+cycles] = True


if __name__ == '__main__':
    lines = [line.rstrip("\n") for line in open('input.txt').readlines()]

    cycles = 6
    cube1 = Cube(lines, cycles)
    cube1.run_cycles()
    print("PART 1:", cube1.active_count())

    cube2 = HyperCube(lines, cycles)
    cube2.run_cycles()
    print("PART 2:", cube2.active_count())
