import pyglet
import smart_snake.src.game.map as Map
import smart_snake.src.game.snake as Snake
import smart_snake.src.game.food as Food


class Game:
    def __init__(self, width, height, x=0, y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map = Map.Map(width, height, self.x, self.y)
        self.snake = Snake.Snake(self.map.rows // 2, self.map.cols // 2, self.map.tile_width, self.x, self.y)
        self.food = Food.Food(len(self.map.grid), len(self.map.grid), self.map.tile_width, self.x, self.y)
        self.score_label = pyglet.text.Label(text="Score: 0", x=25, y=5, font_size=20)
        self.frame_iteration = 0

    def reset(self):
        self.snake.reset()
        self.food.respawn(self.snake)
        self.frame_iteration = 0

    def draw(self, score=True):
        self.map.draw()
        self.snake.draw()
        if score:
            self.score_label.draw()
        self.food.draw()

    def update_direction(self, direction):
        if self.snake.len == len(self.map.get_valid_tiles()):
            self.game_won()

        self.snake.set_dir(direction)
        self.snake.update()
        if self.snake.check_collisions(self.map):
            return

        if self.snake.eat(self.food):
            self.snake.grow()
            self.food.respawn(self.snake)

        self.score_label.text = f"Score: {self.snake.len}"
        self.frame_iteration += 1

    def update_action_reward(self, action):
        reward = 0
        game_over = False
        if self.snake.len == len(self.map.get_valid_tiles()):
            self.game_won()

        self.snake.execute_action(action)
        self.snake.update()

        if self.snake.check_collisions(self.map) or self.frame_iteration > 100 * self.snake.len:
            game_over = True
            reward = -10
            return reward, game_over, self.snake.len

        if self.snake.eat(self.food):
            self.snake.grow()
            self.food.respawn(self.snake)
            reward = 10

        self.score_label.text = f"Score: {self.snake.len}"
        self.frame_iteration += 1
        return reward, game_over, self.snake.len

    def update_action(self, action):
        if self.snake.len == len(self.map.get_valid_tiles()):
            self.game_won()

        self.snake.execute_action(action)
        self.snake.update()
        if self.snake.check_collisions(self.map) or self.frame_iteration > 100 * self.snake.len:
            return True

        if self.snake.eat(self.food):
            self.snake.grow()
            self.food.respawn(self.snake)

        self.score_label.text = f"Score: {self.snake.len}"
        self.frame_iteration += 1
        return False

    def is_collision(self, tile):
        return self.map.is_wall(tile) or self.snake.is_present(tile)

    def game_won(self):
        print("GAME WON")
        self.reset()
