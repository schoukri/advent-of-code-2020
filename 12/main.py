#!/usr/bin/env python3

import sys, re
from collections import namedtuple

class Position:
    def __init__(self, x, y, direction='E'):
        self.x = x
        self.y = y
        self.heading = self.to_degrees(direction)
    def turn(self, direction, value):
        if direction == 'R':
            self.heading = (self.heading + value) % 360
        elif direction == 'L':
            self.heading = (self.heading - value) % 360
    def move(self, heading, value):
        if heading == 0:
            self.y -= value
        elif heading == 90:
            self.x += value
        elif heading == 180:
            self.y += value
        elif heading == 270:
            self.x -= value
    def forward(self, value):
        self.move(self.heading, value)
    def rotate_around(self, origin, direction, value):
        # convert 'L' direction to equivalent value for 'R'
        if direction == 'L':
            value = 360 - value
        # rotate right 90 degrees at a time
        while value in (90, 180, 270):
            dx = self.x - origin.x
            dy = self.y - origin.y
            (dx, dy) = (-dy, dx)
            self.x = origin.x + dx
            self.y = origin.y + dy
            value -= 90

    @classmethod
    def to_degrees(self, direction):
        degrees = {'N': 0, 'E': 90, 'S': 180, 'W': 270}
        return degrees[direction]


def part_2(steps):
    ship = Position(x=0, y=0, direction='E')
    waypt = Position(x=10, y=-1)
    for step in steps:
        if step.action in 'RL':
            waypt.rotate_around(ship, step.action, step.value)
        elif step.action in 'NSEW':
            waypt.move(waypt.to_degrees(step.action), step.value)
        elif step.action == 'F':
            dx = waypt.x - ship.x
            dy = waypt.y - ship.y
            ship.x += dx * step.value
            ship.y += dy * step.value
            waypt.x = ship.x + dx
            waypt.y = ship.y + dy
    return abs(ship.x) + abs(ship.y)

def part_1(steps):
    ship = Position(x=0, y=0, direction='E')
    for step in steps:
        if step.action in 'RL':
            ship.turn(step.action, step.value)
        elif step.action in 'NSEW':
            ship.move(ship.to_degrees(step.action), step.value)
        elif step.action == 'F':
            ship.forward(step.value)
    return abs(ship.x) + abs(ship.y)

if __name__ == '__main__':
    lines = open('input.txt').readlines()
    Step = namedtuple('Step', ['action', 'value'])
    steps = list(Step(m.group(1), int(m.group(2))) for m in map(lambda x: re.match("(\w)(\d+)", x), lines))
    print("PART 1:", part_1(steps))
    print("PART 2:", part_2(steps))
