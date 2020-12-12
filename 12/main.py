#!/usr/bin/env python3

import sys, re
from collections import namedtuple

class Position:
    def __init__(self, x, y, heading=90):
        self.x = x
        self.y = y
        self.heading = heading
    def turn(self, direction, value):
        if direction == 'R':
            self.heading = (self.heading + value) % 360
        elif direction == 'L':
            self.heading = (self.heading - value) % 360
    def move(self, direction, value):
        if direction == 'N':
            self.y -= value
        elif direction == 'E':
            self.x += value
        elif direction == 'S':
            self.y += value
        elif direction == 'W':
            self.x -= value
    def forward(self, value):
        if self.heading == 0:
            self.y -= value
        elif self.heading == 90:
            self.x += value
        elif self.heading == 180:
            self.y += value
        elif self.heading == 270:
            self.x -= value
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


def part_2(steps):
    ship = Position(x=0, y=0, heading=90)
    waypt = Position(x=10, y=-1)
    for step in steps:
        if step.action in ('R', 'L'):
            waypt.rotate_around(ship, step.action, step.value)
        elif step.action in ('N', 'E', 'S', 'W'):
            waypt.move(step.action, step.value)
        elif step.action == 'F':
            dx = waypt.x - ship.x
            dy = waypt.y - ship.y
            ship.x += dx * step.value
            ship.y += dy * step.value
            waypt.x = ship.x + dx
            waypt.y = ship.y + dy
    return abs(ship.x) + abs(ship.y)

def part_1(steps):
    #degrees = {'N': 0, 'E': 90, 'S': 180, 'W': 270}
    ship = Position(x=0, y=0, heading=90)
    for step in steps:
        if step.action in ('R', 'L'):
            ship.turn(step.action, step.value)
        elif step.action == 'N':
            ship.y -= step.value
        elif step.action == 'E':
            ship.x += step.value
        elif step.action == 'S':
            ship.y += step.value
        elif step.action == 'W':
            ship.x -= step.value
        elif step.action == 'F':
            ship.forward(step.value)
    return abs(ship.x) + abs(ship.y)

if __name__ == '__main__':
    lines = open('input.txt').readlines()

    Step = namedtuple('Step', ['action', 'value'])
    steps = []
    for line in lines:
            matches = re.match("(\w)(\d+)", line)
            steps.append(Step(matches.group(1), int(matches.group(2))))

    print("PART 1:", part_1(steps))
    print("PART 2:", part_2(steps))
