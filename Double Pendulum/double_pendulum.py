import arcade
import math
from functools import partial
from random import random
from collections import deque


class Pendulum:
    def __init__(self, length, mass, angle=0, velocity=0, parent: "Pendulum" = None):
        self.length = length
        self.mass = mass
        self.angle = angle
        self.parent = parent
        self.velocity = velocity

    def __repr__(self):
        args = ", ".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({args})"

    def update(self, acceletation):
        # some magic empirical constants, that looks right at 600px window
        if acceletation > 0.1:
            acceletation = 0.1
        self.velocity += acceletation
        if self.velocity > 0.1:
            self.velocity = 0.1
        self.angle += self.velocity
        self.angle %= 2 * math.pi

    def draw(self):
        arcade.draw_line(
            self.head_x, self.head_y, self.tail_x, self.tail_y, arcade.color.BLACK
        )

        arcade.draw_circle_filled(
            self.tail_x, self.tail_y, self.mass, arcade.color.BLACK
        )

    @property
    def head_x(self):
        if self.parent:
            return self.parent.tail_x
        else:
            return 0

    @property
    def head_y(self):
        if self.parent:
            return self.parent.tail_y
        else:
            return 0

    @property
    def tail_x(self):
        return self.head_x + self.length * math.sin(self.angle)

    @property
    def tail_y(self):
        return self.head_y - self.length * math.cos(self.angle)


path = deque(maxlen=200)


class myWindow(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self, p1: "Pendulum", p2: "Pendulum"):
        self.p1 = p1
        self.p2 = p2

    def on_draw(self):
        p1 = self.p1
        p2 = self.p2
        arcade.start_render()

        arcade.set_viewport(-300, 300, -300, 300)
        arcade.draw_text(
            "Press arrow keys to push pendulums", -300, 285, arcade.color.BLACK
        )

        G_CONST = 9.8 / 100
        denom = 2 * p1.mass + p2.mass - p2.mass * math.cos(2 * p1.angle - 2 * p2.angle)
        accel_1 = (
            -G_CONST * (2 * p1.mass + p2.mass) * math.sin(p1.angle)
            - G_CONST * p2.mass * math.sin(p1.angle - 2 * p2.angle)
            - 2
            * math.sin(p1.angle - p2.angle)
            * p2.mass
            * (
                p2.velocity ** 2 * p2.length
                + p1.velocity ** 2 * p1.length * math.cos(p1.angle - p2.angle)
            )
        ) / (denom * p1.length)
        accel_2 = (
            2
            * math.sin(p1.angle - p2.angle)
            * (
                p1.velocity ** 2 * p1.length * (p1.mass + p2.mass)
                + G_CONST * (p1.mass + p2.mass) * math.cos(p1.angle)
                + p2.velocity ** 2 * p2.length * p2.mass * math.cos(p1.angle - p2.angle)
            )
        ) / (denom * p2.length)
        p1.update(accel_1)
        p2.update(accel_2)

        path.append((p2.tail_x, p2.tail_y))
        for i, point in enumerate(path):
            color = 255 - int(255 / len(path) * i)
            arcade.draw_point(*point, (color, color, color), 1)

        p1.draw()
        p2.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.p1.velocity *= 2
        elif symbol == arcade.key.DOWN:
            self.p1.velocity /= 2
        elif symbol == arcade.key.RIGHT:
            self.p2.velocity *= 2
        elif symbol == arcade.key.LEFT:
            self.p2.velocity /= 2

        return super().on_key_press(symbol, modifiers)


def main():

    windows = myWindow(600, 600, "Double Pendulum")

    p1 = Pendulum(length=100, mass=8, angle=math.pi / 3)
    p2 = Pendulum(length=100, mass=10, angle=math.pi / 4, parent=p1)

    windows.setup(p1, p2)
    arcade.set_background_color(arcade.color.WHITE)

    arcade.run()
    arcade.close_window()


if __name__ == "__main__":
    main()
