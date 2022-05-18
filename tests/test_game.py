import pytest

from smart_snake.src.game.food import Food
from smart_snake.src.game.game import Game
from smart_snake.src.helper.helpers import Direction


@pytest.fixture
def game():
    return Game(100, 100)


def test_update_direction(game):
    # Test eating food
    game.food.i = 11
    game.food.j = 10
    game.update_direction(Direction.RIGHT)
    assert game.snake.len == 2
    assert game.snake.dir == Direction.RIGHT

    game.food.i = 11
    game.food.j = 11
    game.update_direction(Direction.UP)
    assert game.snake.len == 3
    assert game.snake.dir == Direction.UP

    game.food.i = 10
    game.food.j = 11
    # right turn
    game.update_direction(Direction.LEFT)
    assert game.snake.len == 4
    assert game.snake.dir == Direction.LEFT


def test_update_action(game):
    game.food.i = 11
    game.food.j = 10
    # straight
    game.update_action([1, 0, 0])
    assert game.snake.len == 2
    assert game.snake.dir == Direction.RIGHT

    game.food.i = 11
    game.food.j = 11
    # left turn
    game.update_action([0, 0, 1])
    assert game.snake.len == 3
    assert game.snake.dir == Direction.UP

    game.food.i = 12
    game.food.j = 11
    # right turn
    game.update_action([0, 1, 0])
    assert game.snake.len == 4
    assert game.snake.dir == Direction.RIGHT


def test_update_action_reward(game):
    game.food.i = 11
    game.food.j = 10
    # straight
    reward, game_over, len = game.update_action_reward([1, 0, 0])
    assert len == 2
    assert not game_over
    assert game.snake.dir == Direction.RIGHT
    assert reward == 10

    game.food.i = 11
    game.food.j = 11
    # left turn
    reward, game_over, len = game.update_action_reward([0, 0, 1])
    assert len == 3
    assert not game_over
    assert reward == 10
    assert game.snake.dir == Direction.UP

    # straight
    reward, game_over, len = game.update_action_reward([1, 0, 0])
    assert reward == 0
    assert not game_over
    assert len == 3

    # travel to edge of map
    for _ in range(17):
        game.update_action_reward([1, 0, 0])

    reward, game_over, len = game.update_action_reward([1, 0, 0])
    assert reward == -10
    assert game_over
