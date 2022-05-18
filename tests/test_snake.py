import pytest

from smart_snake.src.game.map import Map
from smart_snake.src.game.snake import Snake
from smart_snake.src.helper.helpers import Direction


@pytest.fixture
def snake_0():
    return Snake(0, 0, 10, 0, 0)


@pytest.fixture
def snake_10():
    return Snake(10, 10, 10, 0, 0)


@pytest.fixture
def map_20():
    return Map(20, 20)


def test_update(snake_0):
    # test snake movement
    snake_0.set_dir(Direction.RIGHT)
    snake_0.update()
    assert snake_0.body[0].i == 1
    assert snake_0.body[0].j == 0

    snake_0.set_dir(Direction.UP)
    snake_0.update()
    assert snake_0.body[0].i == 1
    assert snake_0.body[0].j == 1

    snake_0.set_dir(Direction.LEFT)
    snake_0.update()
    assert snake_0.body[0].i == 0
    assert snake_0.body[0].j == 1

    snake_0.set_dir(Direction.DOWN)
    snake_0.update()
    assert snake_0.body[0].i == 0
    assert snake_0.body[0].j == 0


def test_action(snake_0):
    assert snake_0.dir == Direction.RIGHT
    # Straight
    snake_0.execute_action([1, 0, 0])
    assert snake_0.dir == Direction.RIGHT

    # Left turn
    snake_0.execute_action([0, 0, 1])
    assert snake_0.dir == Direction.UP

    # Right turn
    snake_0.execute_action([0, 1, 0])
    assert snake_0.dir == Direction.RIGHT


def test_grow(snake_0):
    assert snake_0.len == 1
    snake_0.grow()
    snake_0.grow()
    assert snake_0.len == 3
    assert snake_0.body[0].i == 0
    assert snake_0.body[0].j == 0


def test_collision_map(map_20, snake_0, snake_10):
    # Check snake collision with wall
    assert snake_0.check_collisions(map_20) == True
    assert snake_10.check_collisions(map_20) == False
    # move snake to wall
    for _ in range(10):
        snake_10.update()

    assert snake_10.check_collisions(map_20) == True


def test_collision_self(snake_10, map_20):
    # Check collision with body
    # Grow snake
    for _ in range(5):
        snake_10.grow()
    # Loop the snake into its own body
    snake_10.update()
    snake_10.set_dir(Direction.DOWN)
    snake_10.update()
    snake_10.set_dir(Direction.LEFT)
    snake_10.update()
    snake_10.set_dir(Direction.UP)
    snake_10.update()
    assert snake_10.check_collisions(map_20)
