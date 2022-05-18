import numpy as np
import pyglet.graphics
import smart_snake.src.game.snake_part as SnakePart
from smart_snake.src.helper.helpers import Direction


class Snake:
    def __init__(self, i: int, j: int, size, x, y):
        self.x = x
        self.y = y
        self.start_i = i
        self.start_j = j
        self.size = size
        self.dir = Direction.RIGHT
        self.main_batch = pyglet.graphics.Batch()
        self.len = 1
        self.body = []
        self.color = (100, 0, 0)
        self.body.append(
            SnakePart.SnakePart(self.start_i * self.size + self.x, self.start_j * self.size + self.y, self.size,
                                self.size,
                                self.color, self.main_batch, i, j))
        self.crashed = False

    def draw(self):
        self.main_batch.draw()

    def update(self):
        head = self.body[-1]
        moved_head = SnakePart.SnakePart(head.x, head.y, head.width, head.height, head.color, self.main_batch, head.i,
                                         head.j)
        self.body.pop(0)
        if self.dir == Direction.RIGHT:
            moved_head.x += self.size
            moved_head.i += 1
        elif self.dir == Direction.LEFT:
            moved_head.x -= self.size
            moved_head.i -= 1
        elif self.dir == Direction.DOWN:
            moved_head.y -= self.size
            moved_head.j -= 1
        elif self.dir == Direction.UP:
            moved_head.y += self.size
            moved_head.j += 1

        self.body.append(moved_head)

    def set_dir(self, new_direction):
        self.dir = new_direction

    def execute_action(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.dir)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d
        self.set_dir(new_dir)

    def eat(self, food):
        if self.body[-1].i == food.i and self.body[-1].j == food.j:
            return True
        return False

    def grow(self):
        tail = self.body[0]
        new_part = SnakePart.SnakePart(tail.x, tail.y, tail.width, tail.height, tail.color, self.main_batch, tail.i,
                                       tail.j)
        self.len += 1
        self.body.insert(0, new_part)

    def check_collisions(self, game_map):
        if (self.body[-1].i >= len(game_map.grid) - 1 or self.body[-1].i <= 0) \
                or (self.body[-1].j >= len(game_map.grid[0]) - 1 or self.body[-1].j <= 0):
            self.crashed = True
            return True

        for part in self.body[:-1]:
            if part.position == self.body[len(self.body) - 1].position:
                self.crashed = True
                return True
        return False

    def reset(self):
        self.len = 1
        self.dir = Direction.RIGHT
        self.body = []
        self.body.append(
            SnakePart.SnakePart(self.start_i * self.size + self.x, self.start_j * self.size + self.y, self.size,
                                self.size, self.color,
                                self.main_batch, self.start_i, self.start_j))
        self.crashed = False

    def is_present(self, tile):
        for part in self.body:
            if part.i == tile.i and part.j == tile.j:
                return True
        return False
