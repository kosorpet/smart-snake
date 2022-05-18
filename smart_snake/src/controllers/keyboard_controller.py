import pyglet
from pyglet import window
from pyglet.window import key
from smart_snake.src.helper.helpers import Direction, plot
import smart_snake.src.game.game as Game


class KeyboardController:
    def __init__(self):
        self.game_window = window.Window(800, 800, "Smart snake (Keyboard)")
        self.game = Game.Game(self.game_window.width, self.game_window.height)
        self.input_handler = key.KeyStateHandler()
        self.game_window.push_handlers(self.input_handler)
        self.direction = Direction.RIGHT
        self.plot_scores = []
        self.average_scores = []
        self.total_games = 0
        self.total_score = 0

        @self.game_window.event
        def on_draw():
            self.game_window.clear()
            self.game.draw()

    def get_input(self):
        if self.input_handler[key.LEFT]:
            if self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
        if self.input_handler[key.RIGHT]:
            if self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
        if self.input_handler[key.UP]:
            if self.direction != Direction.DOWN:
                self.direction = Direction.UP
        if self.input_handler[key.DOWN]:
            if self.direction != Direction.UP:
                self.direction = Direction.DOWN

    def run(self):
        pyglet.clock.schedule_interval(self.game_loop, 1 / 15)
        pyglet.app.run()

    def game_loop(self, dt):
        self.get_input()
        self.game.update_direction(self.direction)
        if self.game.snake.crashed:
            self.plot_scores.append(self.game.snake.len)
            self.total_games += 1
            self.total_score += self.game.snake.len
            self.average_scores.append(self.total_score / self.total_games)
            plot(self.plot_scores, self.average_scores, title="Keyboard game", xlabel="Games", ylabel="Score")
            self.game.reset()
