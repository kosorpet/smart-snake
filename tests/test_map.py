import random
import pytest
from smart_snake.src.game.map import Map


@pytest.fixture
def map_20():
    return Map(20, 20)


def test_neigbors_free(map_20):
    neighbors = map_20.neighbors(10, 10)
    for n in neighbors:
        assert not n.wall


def test_neighbors_wall(map_20):
    neighbors = map_20.neighbors(18, 18)
    assert not neighbors[0].wall
    assert not neighbors[1].wall
    assert neighbors[0].i == 17 and neighbors[0].j == 18
    assert neighbors[1].i == 18 and neighbors[1].j == 17


def test_reset(map_20):
    for row in map_20.tiles:
        for tile in row:
            tile.closed = random.choice([True, False])
            tile.opened = random.choice([True, False])
    map_20.reset_tiles()
    for row in map_20.tiles:
        for tile in row:
            assert not tile.closed
            assert not tile.opened


def test_valid(map_20):
    valid = map_20.get_valid_tiles()
    assert len(valid) == (map_20.cols - 2) * (map_20.rows - 2)
    assert all([not t.wall for t in map_20.get_valid_tiles()])


def test_get_tile(map_20):
    assert map_20.get_tile(19, 19).wall
    assert not map_20.get_tile(1, 1).wall
    assert map_20.get_tile(30, 30).wall
