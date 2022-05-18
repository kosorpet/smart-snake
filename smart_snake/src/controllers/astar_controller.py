import queue
import pyglet
from pyglet import window

from smart_snake.src.game.game import Game
from smart_snake.src.helper.helpers import Direction, plot


def heuristic(tile, end):
    return abs(tile.i - end.i) + abs(tile.j - end.j)


class AStarController:
    def __init__(self):
        self.game_window = window.Window(800, 800, "Smart snake (A*)")
        self.game = Game(self.game_window.width, self.game_window.height)
        self.tiles = self.game.map.tiles
        self.path = []
        self.direction = Direction.LEFT
        self.plot_scores = []
        self.average_scores = []
        self.total_games = 0
        self.total_score = 0

        @self.game_window.event
        def on_draw():
            self.game_window.clear()
            self.game.draw()
            self.game.food.draw()

    def reconstruct_path(self, came_from, start, end):
        current = end
        path = []
        while current != start:
            if current not in came_from:
                return []
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def find_path(self):
        pq = queue.PriorityQueue()
        # set the head of the snake as a start point, food as the end point
        start = self.tiles[self.game.snake.body[-1].i][self.game.snake.body[-1].j]
        end = self.tiles[self.game.food.i][self.game.food.j]
        pq.put(start)
        closed_tiles = set()
        came_from = {start: None}

        while not pq.empty():
            current = pq.get()

            if current == end:
                break

            for next_tile in self.game.map.neighbors(current.i, current.j):
                if not self.game.snake.is_present(next_tile) and next_tile not in pq.queue \
                        and next_tile not in closed_tiles:
                    next_tile.dist = current.dist + 1
                    came_from[next_tile] = current
                    next_tile.manhattan_dist = heuristic(next_tile, end)
                    pq.put(next_tile)
            closed_tiles.add(current)

        return came_from

    def freestep(self):
        # freestep is used when no viable path is found, freestep tries to find next empty tile to step on
        row_adj = [-1, 0, 0, 1]
        col_adj = [0, -1, 1, 0]
        for side in range(4):
            head = self.tiles[self.game.snake.body[-1].i][self.game.snake.body[-1].j]
            i = head.i + col_adj[side]
            j = head.j + row_adj[side]
            next_tile = self.tiles[i][j]
            if not self.game.snake.is_present(next_tile) and not next_tile.wall:
                xdir = next_tile.i - self.game.snake.body[-1].i
                ydir = next_tile.j - self.game.snake.body[-1].j
                if xdir == 1:
                    self.direction = Direction.RIGHT
                if xdir == -1:
                    self.direction = Direction.LEFT
                if ydir == 1:
                    self.direction = Direction.UP
                if ydir == -1:
                    self.direction = Direction.DOWN
                return
        # if no empty tile was found arbitrarily step left
        self.direction = Direction.LEFT
        return

    def follow_path(self, path):
        # follow the found path, if no path was found (len 0), freestep
        if len(path) == 0:
            self.freestep()
        else:
            next_tile = path[0]
            xdir = next_tile.i - self.game.snake.body[-1].i
            ydir = next_tile.j - self.game.snake.body[-1].j
            if xdir == 1:
                self.direction = Direction.RIGHT
            if xdir == -1:
                self.direction = Direction.LEFT
            if ydir == 1:
                self.direction = Direction.UP
            if ydir == -1:
                self.direction = Direction.DOWN

    def find_step(self):
        came_from = self.find_path()
        self.path = self.reconstruct_path(came_from, self.tiles[self.game.snake.body[-1].i][self.game.snake.body[-1].j],
                                          self.tiles[self.game.food.i][self.game.food.j])
        self.follow_path(self.path)
        self.game.map.reset_tiles()

    def run(self):
        pyglet.clock.schedule_interval(self.game_loop, 1 / 30)
        pyglet.app.run()

    def game_loop(self, dt):
        self.find_step()
        self.game.update_direction(self.direction)
        if self.game.snake.crashed:
            self.plot_scores.append(self.game.snake.len)
            self.total_games += 1
            self.total_score += self.game.snake.len
            self.average_scores.append(self.total_score / self.total_games)
            self.game.reset()
            plot(self.plot_scores, self.average_scores, title="A* performance", xlabel="Games", ylabel="Score")
