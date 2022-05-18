import pytest
from smart_snake.src.controllers.astar_controller import AStarController


@pytest.fixture
def contr():
    return AStarController()


def test_shortest_path(contr):
    came_from = contr.find_path()
    path = contr.reconstruct_path(came_from, contr.tiles[contr.game.snake.body[-1].i][contr.game.snake.body[-1].j],
                                  contr.tiles[contr.game.food.i][contr.game.food.j])
    # check if shortest path is found
    dist = abs(contr.game.snake.body[-1].i - contr.game.food.i) + abs(contr.game.snake.body[-1].j - contr.game.food.j)
    assert dist == len(path)
