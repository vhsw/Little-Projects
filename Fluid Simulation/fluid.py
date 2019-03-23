from dataclasses import dataclass, field
from typing import List
from math import floor


@dataclass
class Fluid:
    dt: float
    diffusion: float
    viscosity: float
    size: int = 256

    s: List[List[float]] = field(init=False)
    density: List[List[float]] = field(init=False)

    Vx: List[List[float]] = field(init=False)
    Vy: List[List[float]] = field(init=False)

    Vx0: List[List[float]] = field(init=False)
    Vy0: List[List[float]] = field(init=False)

    def __post_init__(self):
        def zeros(N): return [[0. for _ in range(N)] for _ in range(N)]
        self.s = zeros(self.size)
        self.density = zeros(self.size)

        self.Vx = zeros(self.size)
        self.Vy = zeros(self.size)

        self.Vx0 = zeros(self.size)
        self.Vy0 = zeros(self.size)

    def add_density(self, x: int, y: int, amount: float) -> None:
        self.density[x][y] += amount

    def add_velocity(self, x: int, y: int, amount_x: float = 0., amount_y: float = 0.) -> None:
        self.Vx[x][y] += amount_x
        self.Vy[x][y] += amount_y

    # TODO: @staticmethod?
    def diffuse(self, b: int, x: List[List[float]], x0: List[List[float]], diff: float, dt: float, it: int = 10):
        a = dt * diff * (self.size - 2) ** 2
        self.lin_solve(b, x, x0, a, 1 + 6 * a, it)

    def lin_solve(self, b: int, x: List[List[float]], x0: List[List[float]], a: float, c: float, it: int):
        c_recip = 1/c
        for _ in range(it):
            for i in range(1, self.size - 1):
                for j in range(1, self.size - 1):
                    x[i][j] = (x0[i][j] + a * (x[i+1][j]
                                               + x[i-1][j]
                                               + x[i][j+1]
                                               + x[i][j-1])) * c_recip
        self.set_bnd(b, x)

    def project(self, vel_x: List[List[float]], vel_y: List[List[float]], p: List[List[float]], div: List[List[float]],  it: int):
        '''This function is also somewhat mysterious as to exactly how it
        works, but it does some more running through the data and setting
        values, with some calls to lin_solve thrown in for fun.'''
        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                div[i][j] = -0.5 * (vel_x[i+1][j]
                                    - vel_x[i-1][j]
                                    + vel_y[i][j+1]
                                    - vel_y[i][j-1]
                                    )/self.size
                p[i][j] = 0

        self.set_bnd(0, div)
        self.set_bnd(0, p)
        self.lin_solve(0, p, div, 1, 6, it)

        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                vel_x[i][j] -= 0.5 * (p[i+1][j] - p[i-1][j]) * self.size
                vel_y[i][j] -= 0.5 * (p[i][j+1] - p[i][j-1]) * self.size

        self.set_bnd(1, vel_x)
        self.set_bnd(2, vel_y)

    def advect(self, b: int, d: List[List[float]], d0: List[List[float]],  vel_x: List[List[float]], vel_y: List[List[float]], dt: float):
        '''This function is responsible for actually moving things around.
        To that end, it looks at each cell in turn. In that cell, it grabs
        the velocity, follows that velocity back in time, and sees where
        it lands. It then takes a weighted average of the cells around the
        spot where it lands, then applies that value to the current cell.
        '''
        dtx = dt * (self.size - 2)
        dty = dt * (self.size - 2)

        for j in range(1, self.size-1):
            for i in range(1, self.size-1):
                tmp1 = dtx * vel_x[i][j]
                tmp2 = dty * vel_y[i][j]
                x = i - tmp1
                y = j - tmp2

                if x < 0.5:
                    x = 0.5
                if x > self.size + 0.5:
                    x = self.size + 0.5
                i0 = floor(x)
                i1 = i0 + 1

                if y < 0.5:
                    y = 0.5
                if y > self.size + 0.5:
                    y = self.size + 0.5
                j0 = floor(y)
                j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                # TODO: check this
                d[i][j] = (s0 * (t0 * d0[i0][j0] + t1 * d0[i0][j1])
                           + s1 * (t0 * d0[i1][j0] + t1 * d0[i1][j1]))

        self.set_bnd(b, d)

    def set_bnd(self, b: int, x: List[List[float]]):
        '''This is short for "set bounds", and it's a way to keep fluid from
        leaking out of your box.'''

        for i in range(1, self.size-1):
            x[i][0] = -x[i][1] if b == 2 else x[i][1]
            x[i][-1] = -x[i][-2] if b == 2 else x[i][-2]

        for j in range(1, self.size-1):
            x[0][j] = -x[1][j] if b == 1 else x[1][j]
            x[-1][j] = -x[-2][j] if b == 1 else x[-2][j]

        x[0][0] = 0.5 * (x[1][0] + x[0][1])
        x[0][-1] = 0.5 * (x[1][-1] + x[0][-2])
        x[-1][0] = 0.5 * (x[-2][0] + x[-1][1])
        x[-1][-1] = 0.5 * (x[-2][-1] + x[-1][-2])


    def step(self):
        self.diffuse(1, self.Vx0, self.Vx, self.viscosity, self.dt, 4)
        self.diffuse(2, self.Vy0, self.Vy, self.viscosity, self.dt, 4)

        self.project(self.Vx0, self.Vy0, self.Vx, self.Vy, 4)

        self.advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0, self.dt)
        self.advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0, self.dt)

        self.project(self.Vx, self.Vy, self.Vx0, self.Vy0, 4)

        self.diffuse(0, self.s, self.density, self.diffusion, self.dt, 4)
        self.advect(0, self.density, self.s, self.Vx, self.Vy, self.dt)
