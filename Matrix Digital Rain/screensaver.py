import os
import time
from random import randint, choice

import curses


class CharDrop:
    def __init__(self, init_x, init_y, velocity, tick, lifespan):
        self.init_x = init_x
        self.init_y = init_y
        self.velocity = velocity
        self.lifespan = lifespan
        self.tick = tick
        self.chars = {}

    @staticmethod
    def get_char():
        chars = "一九七二人入八力十下三千上口土夕大女子小山川木水火犬王正出本右"
        return choice(chars)

    def alive(self, tick):
        return (tick - self.tick) < self.lifespan

    def get_tick(self, tick):
        '''
        returns position and color of characters  tail
        color from 1 to lifespan
        '''
        steps = tick - self.tick
        trace = dict()
        # self.chars.append(self.get_char())
        for age in range(steps):
            time = tick - self.tick - age
            for step in range(self.velocity):
                x = self.init_x + self.velocity * time - step
                if x not in self.chars:
                    self.chars[x] = self.get_char()
                trace[(x, self.init_y)] = self.chars[x], age + 1
        return trace


class Buffer:
    def __init__(self, rows, columns, colors):
        self.rows = rows
        self.columns = columns//2
        self.density = self.columns//3
        self.buffer = {}
        self.colors = colors
        self.drops = []

    def draw_tick(self, tick):
        traces = dict()
        for drop in self.drops:
            traces.update(drop.get_tick(tick))
        self.buffer = {}
        for x in range(self.rows):
            for y in range(self.columns):
                char, color = traces.get((x, y), ('  ', 1))
                if color > self.colors:
                    color = self.colors
                self.buffer[(x, y)] = char, color
        num_chars = randint(1, self.density + 1)
        for _ in range(num_chars):
            chars = "一九七二人入八力十下三千上口土夕大女子小山川木水火犬王正出本右"
            char = choice(chars)
            init_x = randint(0, self.rows//2)
            init_y = randint(0, self.columns)
            velocity = randint(1, 5)
            lifespan = randint(self.rows//2, self.rows)
            self.drops.append(CharDrop(init_x, init_y, velocity, tick, lifespan))
        self.drops = [drop for drop in self.drops if drop.alive(tick)]


def main(stdscr):
    # Clear screen
    curses.curs_set(0)
    curses.cbreak()
    curses.noecho()

    stdscr.clear()
    stdscr.refresh()

    # white
    curses.init_pair(1, 15, curses.COLOR_BLACK)
    # shades of green
    curses.init_pair(2, 76, curses.COLOR_BLACK)
    curses.init_pair(3, 70, curses.COLOR_BLACK)
    curses.init_pair(4, 64, curses.COLOR_BLACK)
    curses.init_pair(5, 28, curses.COLOR_BLACK)
    curses.init_pair(6, 22, curses.COLOR_BLACK)

    num_colors = 6

    rows, columns = stdscr.getmaxyx()
    rows -= 1
    columns -= 1
    buffer = Buffer(rows, columns, colors=num_colors)
    tick = 0
    while True:
        buffer.draw_tick(tick)
        for x in range(buffer.rows):
            for y in range(buffer.columns):
                value, color = buffer.buffer[(x, y)]
                stdscr.addstr(x, y*2, value, curses.color_pair(color))

        tick += 1
        stdscr.refresh()
        time.sleep(0.1)


if __name__ == "__main__":
    curses.wrapper(main)
