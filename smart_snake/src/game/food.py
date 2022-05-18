import random
from pyglet import shapes


class Food:
    def __init__(self, rows: int, cols: int, size, x, y):
        self.offset_x = x
        self.offset_y = y
        self.size = size
        self.rows = rows
        self.cols = cols
        self.i = random.randint(1, rows - 2)
        self.j = random.randint(1, cols - 2)
        self.x = self.i * self.size + self.offset_x
        self.y = self.j * self.size + self.offset_y

    def draw(self):
        food = shapes.Rectangle(self.x, self.y, self.size, self.size, color=(255, 0, 0))
        food.draw()

    def respawn(self, snake):
        self.i = random.randint(1, self.rows - 2)
        self.j = random.randint(1, self.cols - 2)
        self.x = self.i * self.size + self.offset_x
        self.y = self.j * self.size + self.offset_y
        for part in snake.body:
            if self.i == part.i and self.j == part.j:
                self.respawn(snake)
