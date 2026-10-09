import pytest
from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.eye import Eye

# Positions in the list that Eye.see returns
AHEAD, LEFT, RIGHT, AHEAD_LEFT, AHEAD_RIGHT, FOOD_AHEAD, FOOD_RIGHT = range(7)


def make_result(
    head: Cell,
    heading: Direction,
    body: tuple[Cell, ...] = (),
    food: Cell | None = None,
    row_count: int = 5,
    col_count: int = 5,
) -> StepResult:
    return StepResult(
        is_over=False,
        grid_cells=tuple(tuple(Cell(r, c) for c in range(col_count)) for r in range(row_count)),
        snake_cells=frozenset({head, *body}),
        head=head,
        heading=heading,
        last_turn=Turn.ahead,
        just_ate=False,
        food=food,
    )


# ====================  Shape  ====================


def test_sees_seven_numbers():
    sut = Eye()
    assert len(sut.see(make_result(Cell(2, 2), Direction.up))) == 7
    assert sut.output_count == 7


# ====================  Danger  ====================


def test_wall_right_ahead_is_full_danger():
    seen = Eye().see(make_result(Cell(0, 2), Direction.up))
    assert seen[AHEAD] == 1.0


def test_wall_four_cells_ahead_is_a_quarter_danger():
    seen = Eye().see(make_result(Cell(3, 2), Direction.up))
    assert seen[AHEAD] == 0.25


def test_body_closer_than_the_wall_counts():
    seen = Eye().see(make_result(Cell(3, 2), Direction.up, body=(Cell(1, 2),)))
    assert seen[AHEAD] == 0.5


def test_left_and_right_follow_the_heading():
    # The same wall on the west side of the grid
    heading_up = Eye().see(make_result(Cell(2, 0), Direction.up))
    heading_down = Eye().see(make_result(Cell(2, 0), Direction.down))
    assert heading_up[LEFT] == 1.0
    assert heading_down[RIGHT] == 1.0
    assert heading_down[LEFT] == 0.2  # east wall is 5 cells away


def test_diagonal_rays():
    # Bottom-left corner heading right: ahead-left goes up-right, ahead-right goes down-right
    seen = Eye().see(make_result(Cell(4, 0), Direction.right))
    assert seen[AHEAD_LEFT] == 0.2
    assert seen[AHEAD_RIGHT] == 1.0


# ====================  Food  ====================


def test_food_straight_ahead():
    seen = Eye().see(make_result(Cell(4, 2), Direction.up, food=Cell(0, 2)))
    assert seen[FOOD_AHEAD] == pytest.approx(0.8)
    assert seen[FOOD_RIGHT] == 0


def test_food_behind():
    seen = Eye().see(make_result(Cell(0, 2), Direction.up, food=Cell(4, 2)))
    assert seen[FOOD_AHEAD] == pytest.approx(-0.8)


def test_food_right_follows_the_heading():
    # The same food cell, east of the head
    heading_up = Eye().see(make_result(Cell(2, 2), Direction.up, food=Cell(2, 4)))
    heading_down = Eye().see(make_result(Cell(2, 2), Direction.down, food=Cell(2, 4)))
    assert heading_up[FOOD_RIGHT] == pytest.approx(0.4)
    assert heading_down[FOOD_RIGHT] == pytest.approx(-0.4)


def test_no_food_is_zero():
    seen = Eye().see(make_result(Cell(2, 2), Direction.up, food=None))
    assert seen[FOOD_AHEAD] == 0
    assert seen[FOOD_RIGHT] == 0


def test_values_stay_in_range():
    # Corner to corner, on a grid that is not square
    seen = Eye().see(
        make_result(Cell(2, 6), Direction.left, food=Cell(0, 0), row_count=3, col_count=7)
    )
    assert all(0 <= value <= 1 for value in seen[:FOOD_AHEAD])
    assert all(-1 <= value <= 1 for value in seen[FOOD_AHEAD:])
