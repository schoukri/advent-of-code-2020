#!/usr/bin/env python3

from __future__ import annotations
import re, copy
from more_itertools import split_at
from typing import List, Tuple, Optional

def reverse(value: str) -> str:
    return value[::-1]

class Tile:
    def __init__(self, lines: List[str]):
        match = re.match(r'Tile (\d+):', lines[0])
        self.num = int(match.group(1))
        self.flipped = False
        self.rotation = 0
        top = lines[1]
        right = ''.join([line[-1] for line in lines[1:]])
        bottom = reverse(lines[-1])
        left = reverse(''.join([line[0] for line in lines[1:]]))
        self.sides = [top, right, bottom, left]
    def __repr__(self):
        return f'Num={self.num}, sides={self.sides}, rotation={self.rotation}, flipped={self.flipped}'
    def top(self) -> str:
        side = self.sides[0 - self.rotation]
        return reverse(side) if self.flipped else side
    def right(self) -> str:
        if self.flipped:
            return reverse(self.sides[3 - self.rotation])
        else:
            return self.sides[1 - self.rotation]
    def bottom(self) -> str:
        side = self.sides[2 - self.rotation]
        return reverse(side) if self.flipped else side
    def left(self) -> str:
        if self.flipped:
            return reverse(self.sides[1 - self.rotation])
        else:
            return self.sides[3 - self.rotation]
    def is_valid(self, above_tile: Optional[Tile], left_tile: Optional[Tile]) -> bool:
        if above_tile != None and self.top() != reverse(above_tile.bottom()):
                return False
        if left_tile != None and self.left() != reverse(left_tile.right()):
                return False
        return True

class Grid:
    def __init__(self, size: int):
        self.size = size
        self.seen = set()
        self.data = list()
        for y in range(self.size):
            self.data.append([])
            for x in range(self.size):
                self.data[y].append(None)
    def get_tile(self, x: int, y: int):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.data[y][x]
        return None
    def add_tile(self, x: int, y: int, tile: Tile):
        self.data[y][x] = tile
        self.seen.add(tile.num)
    def is_filled(self) -> bool:
        return self.data[self.size-1][self.size-1] != None
    def contains(self, tile: Tile) -> bool:
        return tile.num in self.seen
    def next_spot(self) -> Tuple[int, int]:
        for y in range(self.size):
            for x in range(self.size):
                if self.data[y][x] == None:
                    return (x, y)
        return None

class TileSet:
    def __init__(self, lines: List[str]):
        self.tiles = []
        for block in split_at(lines, lambda x: x == ''):
            self.tiles.append(Tile(block))
        self.size = int(len(self.tiles) ** 0.5)
    def process(self, grid: Grid):
        # find the coords of the first available spot in the grid
        spot = grid.next_spot()
        above_tile = grid.get_tile(spot[0], spot[1]-1)
        left_tile = grid.get_tile(spot[0]-1, spot[1])

        for tile in self.tiles:
            if grid.contains(tile):
                continue
            for rotation in range(4):
                for flipped in [False, True]:
                    tile.rotation = rotation
                    tile.flipped = flipped
                    if tile.is_valid(above_tile, left_tile):
                        gridcopy = copy.deepcopy(grid)
                        gridcopy.add_tile(spot[0], spot[1], tile)
                        if gridcopy.is_filled():
                            return gridcopy
                        else:
                            newgrid = self.process(gridcopy)
                            if newgrid != None and newgrid.is_filled():
                                return newgrid
        return None
    def part_1(self) -> int:
        grid = Grid(self.size)
        final = self.process(grid)
        last = self.size - 1
        return final.get_tile(0, 0).num * final.get_tile(0, last).num * final.get_tile(last, 0).num * final.get_tile(last, last).num

if __name__ == '__main__':
    lines = [line.rstrip("\n") for line in open('input.txt').readlines()]

    ts = TileSet(lines)
    part_1 = ts.part_1()
    print("PART 1:", part_1)
    assert(part_1 == 18262194216271) # input.txt
    #assert(part_1 == 20899048083289) # sample.txt
