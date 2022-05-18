import pyglet
import smart_snake.src.game.tile as Tile
from pyglet import shapes


class Map:
    def __init__(self, width, height, x=0, y=0):
        self.x = x
        self.y = y
        self.grid = []
        self.tiles = []
        self.rows = 20
        self.cols = 20
        self.main_batch = pyglet.graphics.Batch()

        self.tile_height = height / self.cols
        self.tile_width = width / self.cols

        self.fill_batch()

    def draw(self):
        self.main_batch.draw()

    def neighbors(self, tile_i, tile_j):
        neighbors = []
        row_adj = [-1, 0, 0, 1]
        col_adj = [0, -1, 1, 0]

        for side in range(4):
            i = tile_i + row_adj[side]
            j = tile_j + col_adj[side]
            if not self.tiles[i][j].wall:
                neighbors.append(self.tiles[i][j])
        return neighbors

    def fill_batch(self):
        for i in range(self.rows):
            grid_row = []
            tile_row = []
            for j in range(self.cols):
                color = (100, 100, 100) if (j == 0 or j == self.cols - 1 or i == 0 or i == self.rows - 1) else (
                    255, 255, 255)
                grid_row.append(
                    shapes.Rectangle(i * self.tile_width + self.x, j * self.tile_height + self.y, self.tile_width,
                                     self.tile_height,
                                     color=color, batch=self.main_batch))
                tile_row.append(Tile.Tile(i * self.tile_width, j * self.tile_height, self.tile_width, self.tile_height,
                                          (j == 0 or j == self.cols - 1 or i == 0 or i == self.rows - 1), i, j))
            self.grid.append(grid_row)
            self.tiles.append(tile_row)

    def reset_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.closed = False
                tile.opened = False

    def get_valid_tiles(self):
        valid_tiles = []
        for row in self.tiles:
            for tile in row:
                if not tile.wall:
                    valid_tiles.append(tile)
        return valid_tiles

    def is_wall(self, tile):
        return self.tiles[tile.i][tile.j].wall

    def get_tile(self, i, j):
        if i < 0 or i > self.cols - 1:
            return Tile.Tile(-1, -1, -1, -1, True, -1, -1)
        if j < 0 or j > self.rows - 1:
            return Tile.Tile(-1, -1, -1, -1, True, -1, -1)
        return self.tiles[i][j]
