class Tile:
    def __init__(self, x, y, width, height, wall, i: int, j: int):
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self.wall = wall
        self.dist = 0
        self.manhattan_dist = 0

    def __lt__(self, other):
        return (self.dist + self.manhattan_dist) < (other.dist + other.manhattan_dist)

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash(str(self))
