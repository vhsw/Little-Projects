import os
import time
from random import randint, choice
import numbers
import curses
from collections import deque


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return self.__class__(self.x * other, self.y * other)
        elif isinstance(other, self.__class__):
            return self.__class__(self.x * other.x, self.y * other.y)
        else:
            raise TypeError(
                f'cannot multiply {self.__class__.__name__} on {other.__class__.__name__}')

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)
        else:
            raise TypeError(
                f'cannot add {self.__class__.__name__} to    {other.__class__.__name__}')

    def __eq__(self, other):
        return self.x, self.y == other.x, other.y


class Particle:
    def __init__(self, pos: 'Vector',
                 velocity: 'Vector',
                 radius: int,
                 lifespan: int):
        self.pos = pos
        self.velocity = velocity
        self.age = 1
        self.lifespan = lifespan

    @classmethod
    def new_random(cls, max_x, max_y, wind=0):
        pos = Vector(max_x, randint(0, max_y))
        vel = Vector(randint(-3, 0), wind)
        rad = randint(max_y//50, max_y//5)
        lifespan = randint(max_x//3, max_x//2)
        return cls(pos, vel, rad, lifespan)


class Buffer:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.buffer = {}
        self.partcles = []
        for _ in range(self.columns):
            self.partcles.append(Particle.new_random(self.rows, self.columns))

    def valid_particle(self, partcle: 'Particle'):
        return partcle.lifespan > partcle.age and 0 <= partcle.pos.x < self.rows and 0 <= partcle.pos.y < self.columns

    def draw_tick(self, tick):
        for p in self.partcles:
            radius = p.lifespan - p.age
            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    if x*x + y*y <= radius * radius:
                        x_ = x + p.pos.x
                        y_ = y + p.pos.y
                        if 0 <= x_ < self.rows and 0 <= y_ < self.columns:
                            self.buffer[(x_, y_)] = ' ', 1

        for idx, p in enumerate(self.partcles):
            p.pos = p.pos + p.velocity
            p.age += 1
            wind = 0
            if not self.valid_particle(p):
                self.partcles[idx] = Particle.new_random(
                    self.rows, self.columns, wind)

        for p in self.partcles:
            radius = p.lifespan - p.age
            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    if x*x + y*y <= radius * radius:
                        x_ = x + p.pos.x
                        y_ = y + p.pos.y
                        if 0 <= x_ < self.rows and 0 <= y_ < self.columns:
                            self.buffer[(x_, y_)] = '#', min(p.age, NUM_COLORS)


NUM_COLORS = 12


def main(stdscr):
    # Clear screen
    curses.curs_set(0)
    curses.cbreak()
    curses.noecho()
    stdscr.clear()
    stdscr.refresh()
    for i, c in enumerate((15, 228, 192, 191, 190, 184, 178, 172, 166, 202, 130, 242), start=1):
        curses.init_pair(i, c, curses.COLOR_BLACK)

    rows, columns = stdscr.getmaxyx()
    buffer = Buffer(rows - 1, columns)
    tick = 0
    time_redraw = time.time_ns()
    FPS = 24
    while True:
        if time.time_ns() <= time_redraw:
            time.sleep((time_redraw - time.time_ns())/1e9)

        time_redraw = time.time_ns() + 1e9/FPS

        # handle resize
        rows, columns = stdscr.getmaxyx()
        if (rows, columns) != (buffer.rows + 1, buffer.columns):
            buffer = Buffer(rows - 1, columns)
            stdscr.clear()
            stdscr.refresh()

        buffer.draw_tick(tick)
        for (row, column), (value, color) in buffer.buffer.items():
            stdscr.addstr(row, column, value, curses.color_pair(color))
        tick += 1
        stdscr.refresh()
        # time.sleep(1/30)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
