import curses
import os
import time
from random import choice, randint
from typing import Dict, List, Tuple


class CharDrop:
    def __init__(self, init_x: int,
                 init_y: int, velocity: int,
                 tick: int, lifespan: int) -> None:
        self.init_x = init_x
        self.init_y = init_y
        self.velocity = velocity
        self.lifespan = lifespan
        self.tick = tick
        self.chars: Dict[int, str] = {}

    @staticmethod
    def get_char() -> str:
        chars = "一九七二人入八力十下三千上口土夕大女子小山川木水火犬王正出本右"
        return choice(chars)

    def alive(self, tick: int) -> bool:
        return (tick - self.tick) < self.lifespan

    def get_tick(self, tick: int) -> Dict[Tuple[int, int], Tuple[str, int]]:
        steps = tick - self.tick
        trace = dict()
        for age in range(steps):
            time = tick - self.tick - age
            for step in range(self.velocity):
                x = self.init_x + self.velocity * time - step
                if x not in self.chars:
                    self.chars[x] = self.get_char()
                trace[(x, self.init_y)] = self.chars[x], age + 1
        return trace


class Buffer:
    def __init__(self, rows: int = 0, cols: int = 0) -> None:
        self.rows = rows
        self.cols = cols
        self.density = self.cols//3
        self.drops: List[CharDrop] = []

    def draw_tick(self, tick: int) -> Dict[Tuple[int, int], Tuple[str, int]]:
        traces: Dict[Tuple[int, int], Tuple[str, int]] = {}
        for drop in self.drops:
            traces.update(drop.get_tick(tick))

        buffer: Dict[Tuple[int, int], Tuple[str, int]] = {}
        for x in range(self.rows):
            for y in range(self.cols):
                char, color = traces.get((x, y), ('  ', 1))
                if color > NUM_COLORS:
                    color = NUM_COLORS
                buffer[(x, y)] = char, color
        num_chars = randint(1, self.density + 1)
        for _ in range(num_chars):
            chars = "一九七二人入八力十下三千上口土夕大女子小山川木水火犬王正出本右"
            char = choice(chars)
            init_x = randint(0, self.rows//2)
            init_y = randint(0, self.cols)
            velocity = randint(1, 5)
            lifespan = randint(self.rows//2, self.rows)
            self.drops.append(
                CharDrop(init_x, init_y, velocity, tick, lifespan))
        self.drops = [drop for drop in self.drops if drop.alive(tick)]
        return buffer


NUM_COLORS = 6


def main(stdscr) -> None:  # type: ignore
    curses.curs_set(0)
    curses.use_default_colors()

    curses.init_pair(1, 15, -1)
    curses.init_pair(2, 76, -1)
    curses.init_pair(3, 70, -1)
    curses.init_pair(4, 64, -1)
    curses.init_pair(5, 28, -1)
    curses.init_pair(6, 22, -1)

    tick = 0
    buffer = Buffer()
    while True:
        rows, cols = stdscr.getmaxyx()
        cols //= 2
        if (rows, cols) != (buffer.rows, buffer.cols):
            buffer = Buffer(rows, cols)

        for (x, y), (value, color) in buffer.draw_tick(tick).items():
            try:
                stdscr.addstr(x, y*2, value, curses.color_pair(color))
            except curses.error:  # skip trailing character at last line
                continue
        tick += 1
        stdscr.refresh()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        exit(0)
