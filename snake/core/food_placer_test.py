import random
from snake.core.food_placer import FoodPlacer
from snake.core.cell import Cell

FREE = [
    Cell(0, 0),
    Cell(0, 1),
    Cell(1, 0),
    Cell(1, 1),
]


def make_food_placer(seed: int = 42) -> FoodPlacer:
    return FoodPlacer(random.Random(seed))


def test_places_food_on_a_free_cell():
    sut = make_food_placer()
    for _ in range(50):
        assert sut.place_food(FREE) in FREE


def test_places_food_on_the_only_free_cell():
    sut = make_food_placer()
    only = Cell(3, 4)
    assert sut.place_food([only]) == only


def test_same_seed_gives_same_sequence():
    first = make_food_placer(7)
    second = make_food_placer(7)
    for _ in range(20):
        assert first.place_food(FREE) == second.place_food(FREE)


def test_reaches_every_free_cell():
    sut = make_food_placer()
    placed = {sut.place_food(FREE) for _ in range(200)}
    assert placed == set(FREE)


def test_works_without_given_rng():
    sut = FoodPlacer()
    assert sut.place_food(FREE) in FREE
