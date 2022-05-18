import copy

import pytest
import torch

from smart_snake.src.game.game import Game
from smart_snake.src.helper.helpers import get_state
from smart_snake.src.models.individual import Individual


@pytest.fixture
def game():
    return Game(100, 100)


def test_get_action(game):
    ind = Individual()
    assert ind.get_action(get_state(game)) == [0, 0, 1] or [0, 1, 0] or [1, 0, 0]


def test_mutate_param():
    ind = Individual()
    for param in ind.brain.parameters():
        mutated = copy.deepcopy(param)
        ind.mutate_param(mutated)
        assert not torch.all(torch.eq(mutated, param))
