import dataclasses
import pytest
from snake.core.cell import Cell
from snake.core.direction import Direction
from snake.core.step_result import StepResult

HEAD = Cell(2, 2)
TAIL = Cell(2, 1)
FOOD = Cell(0, 0)
CELL_ROWS = tuple(tuple(Cell(r, c) for c in range(5)) for r in range(4))


def make_result(snake_cells=frozenset({TAIL, HEAD}), food=FOOD) -> StepResult:
    return StepResult(
        is_over=True,
        cell_rows=CELL_ROWS,
        snake_cells=snake_cells,
        head=HEAD,
        direction=Direction.right,
        food=food,
    )


def test_keeps_values():
    sut = make_result()
    assert sut.cell_rows == CELL_ROWS
    assert sut.snake_cells == frozenset({TAIL, HEAD})
    assert sut.food == FOOD
    assert sut.head == HEAD
    assert sut.direction == Direction.right
    assert sut.is_over


def test_food_may_be_missing():
    # e.g. the board is filled and there is nowhere left to put food
    assert make_result(food=None).food is None


def test_snake_length_comes_from_snake_cells():
    assert make_result().snake_length == 2


def test_immutable():
    sut = make_result()
    with pytest.raises(dataclasses.FrozenInstanceError):
        sut.head = TAIL
