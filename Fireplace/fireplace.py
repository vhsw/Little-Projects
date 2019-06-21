#!/usr/bin/env python3
import curses
import time
from operator import attrgetter
from random import randint


NUM_COLORS = 10
MAX_RADIUS = 12
MIN_RADIUS = 5
FPS = 15


class Vector:
    __slots__ = ['x', 'y']

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __iadd__(self, other: object) -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


class Particle:
    __slots__ = ['pos', 'velocity', 'radius']

    def __init__(self, max_x: int, max_y: int):
        self.pos = Vector(max_x, randint(0, max_y))
        self.velocity = Vector(randint(-2, 0), 0)
        self.radius = randint(MIN_RADIUS, MAX_RADIUS)

    def step(self) -> None:
        self.pos += self.velocity
        if self.velocity.x > -3:
            self.velocity.x -= 1
        self.pos.y += randint(-1, 1)
        self.radius -= 1

    @property
    def color(self) -> int:
        return self.radius if self.radius <= NUM_COLORS else NUM_COLORS


def main(stdscr) -> None:  # type: ignore
    curses.curs_set(0)
    curses.use_default_colors()
    for i, color in enumerate((242, 130, 202, 172, 178, 190, 191, 192, 228, 15), start=1):
        curses.init_pair(i, color, -1)

    circles = tuple(tuple((row, col) for row in range(-radius, radius + 1)
                          for col in range(-radius, radius + 1)
                          if (row ** 2 + col ** 2) <= (radius ** 2))
                    for radius in range(MAX_RADIUS + 1))

    next_redraw = time.time()
    rows, cols = -1, -1
    while True:
        if (rows, cols) != stdscr.getmaxyx():
            rows, cols = stdscr.getmaxyx()
            partcles = [Particle(rows, cols) for _ in range(cols)]

        for i, partcle in enumerate(partcles):
            partcle.step()
            if partcle.radius <= 0:
                partcles[i] = Particle(rows, cols)

        buffer = [[-1] * cols for _ in range(rows)]
        for partcle in sorted(partcles, key=attrgetter('radius')):
            color = partcle.color
            for x, y in circles[partcle.radius]:
                try:
                    buffer[x + partcle.pos.x][y + partcle.pos.y] = color
                except IndexError:
                    continue

        stdscr.clear()
        for row in range(rows):
            for col in range(cols):
                color = buffer[row][col]
                if color < 0:
                    continue
                try:
                    stdscr.addstr(row, col, str((row + col + color) % 2),
                                  curses.color_pair(color))
                except curses.error:  # skip characters off screen
                    pass
        if time.time() < next_redraw:
            time.sleep(next_redraw - time.time())
        next_redraw = time.time() + 1/FPS
        stdscr.refresh()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        exit(0)
