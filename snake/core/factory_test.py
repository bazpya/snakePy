from snake.core.cell import Cell
from snake.core.direction import Direction
from snake.core.factory import Factory
from snake.core.world import World
from snake.core.turn import Turn
from snake.fakes import FixedFoodPlacer


def test_creates_a_world():
    sut = Factory(row_count=4, col_count=6)
    assert isinstance(sut.create(), World)


def test_world_has_the_given_size():
    result = Factory(row_count=4, col_count=6).create().initial_result
    assert len(result.cell_rows) == 4
    assert all(len(row) == 6 for row in result.cell_rows)


def test_snake_starts_at_the_centre_heading_right():
    result = Factory(row_count=4, col_count=6).create().initial_result
    assert result.head == Cell(2, 3)
    assert result.snake_cells == frozenset({Cell(2, 3)})
    assert result.direction == Direction.right


def test_uses_the_given_food_placer():
    sut = Factory(row_count=4, col_count=6, food_placer=FixedFoodPlacer(Cell(0, 0)))
    assert sut.create().initial_result.food == Cell(0, 0)


def test_places_food_off_the_snake_by_default():
    result = Factory(row_count=4, col_count=6).create().initial_result
    assert result.food is not None
    assert result.food not in result.snake_cells


def test_creates_independent_worlds():
    sut = Factory(row_count=4, col_count=6, food_placer=FixedFoodPlacer(Cell(0, 0)))
    first = sut.create()
    second = sut.create()
    first.step(Turn.left)
    assert second.step(Turn.ahead).head == Cell(2, 4)
