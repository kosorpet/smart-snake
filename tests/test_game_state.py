import pytest
from smart_snake.src.game.game import Game
from smart_snake.src.helper.helpers import get_state
from numpy.testing import assert_equal


@pytest.fixture
def game_food_10_12():
    g = Game(100, 100)
    g.food.i = 10
    g.food.j = 12
    return g


@pytest.fixture
def game_food_10_8():
    g = Game(100, 100)
    g.food.i = 10
    g.food.j = 8
    return g


@pytest.fixture
def game_food_12_10():
    g = Game(100, 100)
    g.food.i = 12
    g.food.j = 10
    return g


@pytest.fixture
def game_food_8_12():
    g = Game(100, 100)
    g.food.i = 8
    g.food.j = 12
    return g


@pytest.fixture
def game_food_8_8():
    g = Game(100, 100)
    g.food.i = 8
    g.food.j = 8
    return g


@pytest.fixture
def game_food_12_8():
    g = Game(100, 100)
    g.food.i = 12
    g.food.j = 8
    return g


@pytest.fixture
def game_food_12_12():
    g = Game(100, 100)
    g.food.i = 12
    g.food.j = 12
    return g


@pytest.fixture
def game_food_8_10():
    g = Game(100, 100)
    g.food.i = 8
    g.food.j = 10
    return g


def test_state_below(game_food_10_8):
    assert_equal(get_state(game_food_10_8), [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0])


def test_state_right(game_food_12_10):
    assert_equal(get_state(game_food_12_10), [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0])


def test_state_above(game_food_10_12):
    assert_equal(get_state(game_food_10_12), [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1])


def test_state_left(game_food_8_10):
    assert_equal(get_state(game_food_8_10), [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0])


def test_state_above_right(game_food_12_12):
    assert_equal(get_state(game_food_12_12), [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1])


def test_state_above_left(game_food_8_12):
    assert_equal(get_state(game_food_8_12), [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1])


def test_state_below_left(game_food_8_8):
    assert_equal(get_state(game_food_8_8), [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0])


def test_state_below_right(game_food_12_8):
    assert_equal(get_state(game_food_12_8), [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0])
