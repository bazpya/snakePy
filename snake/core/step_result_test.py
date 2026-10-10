import dataclasses
import pytest
from snake.core.cell import Cell
from snake.core.direction import Direction
from snake.core.end_cause import EndCause
from snake.core.step_result import StepResult
from snake.core.turn import Turn

HEAD = Cell(2, 2)
TAIL = Cell(2, 1)
FOOD = Cell(0, 0)
CELL_ROWS = tuple(tuple(Cell(r, c) for c in range(5)) for r in range(4))


def make_result(snake_cells=frozenset({TAIL, HEAD}), food=FOOD, end_cause=EndCause.crashed) -> StepResult:
    return StepResult(
        end_cause=end_cause,
        grid_cells=CELL_ROWS,
        snake_cells=snake_cells,
        head=HEAD,
        tail=TAIL,
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=False,
        food=food,
    )


def test_keeps_values():
    sut = make_result()
    assert sut.grid_cells == CELL_ROWS
    assert sut.snake_cells == frozenset({TAIL, HEAD})
    assert sut.food == FOOD
    assert sut.head == HEAD
    assert sut.tail == TAIL
    assert sut.heading == Direction.right
    assert sut.last_turn == Turn.ahead
    assert sut.just_ate is False
    assert sut.end_cause == EndCause.crashed


def test_food_may_be_missing():
    # e.g. the grid is filled and there is nowhere left to put food
    assert make_result(food=None).food is None


def test_snake_length_comes_from_snake_cells():
    assert make_result().snake_length == 2


def test_grid_cell_count_comes_from_grid_cells():
    assert make_result().grid_cell_count == 20  # 4x5


def test_immutable():
    sut = make_result()
    with pytest.raises(dataclasses.FrozenInstanceError):
        sut.head = TAIL


def test_is_over_when_there_is_an_end_cause():
    assert make_result(end_cause=EndCause.starved).is_over


def test_is_not_over_without_an_end_cause():
    assert not make_result(end_cause=None).is_over
