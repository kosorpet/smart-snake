from enum import Enum
import matplotlib.pyplot as plt
from IPython import display
import numpy as np


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


def plot(line1, line2=None, title='', xlabel='', ylabel=''):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(line1)
    if line2:
        plt.plot(line2)
    plt.ylim(ymin=0)
    plt.text(len(line1) - 1, line1[-1], str(line1[-1]))
    if line2:
        plt.text(len(line2) - 1, line2[-1], str(line2[-1]))
    plt.show(block=False)
    plt.pause(.1)


def get_state(game):
    head = game.snake.body[-1]
    point_l = game.map.get_tile(head.i - 1, head.j)
    point_r = game.map.get_tile(head.i + 1, head.j)
    point_u = game.map.get_tile(head.i, head.j + 1)
    point_d = game.map.get_tile(head.i, head.j - 1)

    dir_l = game.snake.dir == Direction.LEFT
    dir_r = game.snake.dir == Direction.RIGHT
    dir_u = game.snake.dir == Direction.UP
    dir_d = game.snake.dir == Direction.DOWN

    state = [
        # Danger straight
        (dir_r and game.is_collision(point_r)) or
        (dir_l and game.is_collision(point_l)) or
        (dir_u and game.is_collision(point_u)) or
        (dir_d and game.is_collision(point_d)),

        # Danger right
        (dir_u and game.is_collision(point_r)) or
        (dir_d and game.is_collision(point_l)) or
        (dir_l and game.is_collision(point_u)) or
        (dir_r and game.is_collision(point_d)),

        # Danger left
        (dir_d and game.is_collision(point_r)) or
        (dir_u and game.is_collision(point_l)) or
        (dir_r and game.is_collision(point_u)) or
        (dir_l and game.is_collision(point_d)),

        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,

        # Food location
        game.food.i < game.snake.body[-1].i,  # food left
        game.food.i > game.snake.body[-1].i,  # food right
        game.food.j < game.snake.body[-1].j,  # food up
        game.food.j > game.snake.body[-1].j  # food down
    ]
    # convert true/false values to int
    return np.array(state, dtype=int)
