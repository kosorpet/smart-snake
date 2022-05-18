import pyglet.shapes


class SnakePart(pyglet.shapes.Rectangle):
    def __init__(self, x, y, width, height, color, batch, i, j):
        super().__init__(x, y, width, height, color, batch)
        self.i = i
        self.j = j
