from fluid import Fluid
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


def main():
    fluid = Fluid(dt=0.001, diffusion=0.00001, viscosity=0.00001, size=64)
    fig, ax = plt.subplots()
    plot = plt.imshow(fluid.density, animated=True)

    def update(*args):
        from random import randint

        x, y = randint(0, 53), randint(0, 53)
        fluid.add_density(x, y, 100)
        fluid.add_velocity(x, y, 1000, 10000)
        fluid.step()
        plot.set_array(fluid.density)
        plot.autoscale()

        return (plot,)

    _ = animation.FuncAnimation(fig, update, interval=3, blit=True)
    plt.show()


if __name__ == "__main__":
    main()
