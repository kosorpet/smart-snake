import pytest

from smart_snake.src.controllers.genetic_controller import GeneticController, POPULATION_SIZE


@pytest.fixture
def contr():
    return GeneticController()


def test_init(contr):
    assert len(contr.population) == POPULATION_SIZE
    assert len(contr.games) == POPULATION_SIZE
    assert all([not ind.done for ind in contr.population])
    assert all([g.frame_iteration == 0 for g in contr.games])


def test_new_generation(contr):
    contr.new_generation()
    assert len(contr.population) == POPULATION_SIZE


def test_reset(contr):
    contr.reset()
    assert all([not ind.done for ind in contr.population])
