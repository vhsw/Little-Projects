#!/usr/bin/env python

import curses
import time
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass
from random import choice, randint

NUM_COLORS = 6

CHARS_POOL = "一九七二人入八力十下三千上口土夕大女子小山川木水火犬王正出本右"


@dataclass
class Drop:
    init_tick: int
    init_vel: int
    min_vel: int

    def __post_init__(self) -> None:
        self.chars: defaultdict[int, str] = defaultdict(lambda: choice(CHARS_POOL))

    def get_trace(self, tick: int) -> list[tuple[str, int]]:
        trace: list[tuple[str, int]] = []
        age = tick - self.init_tick
        for step in range(age):
            velocity = max(self.min_vel, self.init_vel - step)
            for vel_step in range(velocity):
                dx = velocity * step - vel_step
                color_offset = self.min_vel - 2
                color = min(NUM_COLORS, age - step - color_offset)
                trace.append((self.chars[dx], color))
        return trace


class Buffer:
    def __init__(self, cols: int, rows: int) -> None:
        self.cols = cols
        self.rows = rows
        self.density = max(1, self.rows // 20)
        self.drop_cols: list[dict[int, Drop]] = [{} for _ in range(cols)]

    def draw_tick(self, tick: int):
        for col, drop_col in enumerate(self.drop_cols):
            dead_drops = []
            for row, drop in drop_col.items():
                colors: set[int] = set()
                for d_row, (char, color) in enumerate(drop.get_trace(tick)):
                    if 0 <= row + d_row <= self.rows:
                        colors.add(color)
                        yield (col, row + d_row), (char, color)
                if all(color == NUM_COLORS for color in colors):
                    dead_drops.append(row)
            for row in dead_drops:
                del drop_col[row]
        self.spawn_new_drops(tick)

    def spawn_new_drops(self, tick, randomize=False):
        for drop_col in self.drop_cols:
            drops = len(drop_col)
            for _ in range(drops, self.density):
                row = randint(-self.rows // 2, self.rows // 2)
                drop_col[row] = Drop(
                    init_tick=randint(tick - self.rows, tick) if randomize else tick,
                    init_vel=randint(self.rows // 16, self.rows // 8),
                    min_vel=3 if randint(0, 5) == 0 else 1,
                )


def main(stdscr) -> None:  # type: ignore
    curses.curs_set(0)
    curses.use_default_colors()

    # see NUM_COLORS
    curses.init_pair(1, 15, -1)
    curses.init_pair(2, 76, -1)
    curses.init_pair(3, 70, -1)
    curses.init_pair(4, 64, -1)
    curses.init_pair(5, 28, -1)
    curses.init_pair(6, 22, -1)

    fps = 15
    tick = 0
    buffer = init(stdscr, tick)
    while True:
        start = time.time()
        cols, rows = get_cols_rows(stdscr)
        if (cols, rows) != (buffer.cols, buffer.rows):
            buffer = init(stdscr, tick)
        for (col, row), (char, color) in buffer.draw_tick(tick):
            with suppress(curses.error):
                stdscr.addch(row, col * 2, char, curses.color_pair(color))
        tick += 1
        stdscr.refresh()
        time.sleep(max(0, 1 / fps - (time.time() - start)))


def get_cols_rows(stdscr):
    rows, cols = stdscr.getmaxyx()
    return cols // 2, rows


def init(stdscr, tick):
    stdscr.clear()
    cols, rows = get_cols_rows(stdscr)
    buffer = Buffer(cols, rows)
    buffer.spawn_new_drops(tick, randomize=True)
    return buffer


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        curses.wrapper(main)
