import curses
import os
import time
from collections import deque
from random import choice, randint
from typing import Dict, List, Tuple, Union


class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Vector({self.x}, {self.y})'

    def __add__(self, other: object) -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


class Particle:
    def __init__(self, pos: Vector,
                 velocity: Vector,
                 radius: int,
                 lifespan: int):
        self.pos = pos
        self.velocity = velocity
        self.age = 1
        self.lifespan = lifespan

    @classmethod
    def new_random(cls, max_x: int, max_y: int) -> 'Particle':
        pos = Vector(max_x, randint(0, max_y))
        vel = Vector(randint(-4, 0), 0)
        rad = randint(max_y//50, max_y//5)
        lifespan = randint(max_x//4, max_x//3)
        return cls(pos, vel, rad, lifespan)

    @property
    def radius(self) -> int:
        return self.lifespan - self.age


class Buffer:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.buffer: dict = {}
        self.partcles: List[Particle] = []
        for _ in range(self.columns):
            self.partcles.append(Particle.new_random(self.rows, self.columns))

    def valid_particle(self, p: Particle) -> bool:
        return (p.lifespan > p.age)

    def draw_tick(self, tick: int) -> Dict[Tuple[int, int], Tuple[str, int]]:
        buffer: Dict[Tuple[int, int], Tuple[str, int]] = {}
        for idx, p in enumerate(self.partcles):
            p.pos = p.pos + p.velocity
            p.age += 1
            if not self.valid_particle(p):
                self.partcles[idx] = Particle.new_random(
                    self.rows, self.columns)

        for p in self.partcles:
            radius = p.radius
            for x_ in range(-radius, radius + 1):
                for y_ in range(-radius, radius + 1):
                    if (x_*x_ + y_*y_) <= (radius * radius):
                        x = x_ + p.pos.x
                        y = y_ + p.pos.y
                        if ((x, y) in buffer
                            or x < 0 or x >= self.rows
                                or y < 0 or y >= self.columns):
                            continue
                        if p.age <= NUM_COLORS:
                            color = p.age
                        else:
                            color = NUM_COLORS
                        buffer[(x, y)] = '#', color
        return buffer


NUM_COLORS = 12


def main(stdscr) -> None:  # type: ignore
    curses.curs_set(False)
    curses.use_default_colors()
    for i, c in enumerate((15, 228, 192, 191, 190, 184, 178, 172, 166, 202, 130, 242), start=1):
        curses.init_pair(i, c, curses.COLOR_BLACK)

    rows, columns = stdscr.getmaxyx()
    buffer = Buffer(rows - 1, columns)
    tick = 0
    time_redraw = time.time_ns()
    FPS = 15
    while True:
        # handle resize
        rows, columns = stdscr.getmaxyx()
        if (rows, columns) != (buffer.rows + 1, buffer.columns):
            buffer = Buffer(rows - 1, columns)

        stdscr.clear()
        if time.time_ns() < time_redraw:
            time.sleep((time_redraw - time.time_ns())/1e9)

        time_redraw = time.time_ns() + int(1e9/FPS)

        for (row, column), (value, color) in buffer.draw_tick(tick).items():
            stdscr.addstr(row, column, value, curses.color_pair(color))
        stdscr.refresh()
        tick += 1


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        exit(0)
