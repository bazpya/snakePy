import pytest
from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.eye import Eye

# Positions in the list that Eye.see returns
(
    AHEAD, LEFT, RIGHT, AHEAD_LEFT, AHEAD_RIGHT,
    FOOD_AHEAD, FOOD_RIGHT,
    ROOM_LEFT, ROOM_AHEAD, ROOM_RIGHT,
    TAIL_AHEAD, TAIL_RIGHT,
    TAIL_REACH_LEFT, TAIL_REACH_AHEAD, TAIL_REACH_RIGHT,
) = range(15)


def make_result(
    head: Cell,
    heading: Direction,
    body: tuple[Cell, ...] = (),
    tail: Cell | None = None,  # None: the head is the tail
    food: Cell | None = None,
    row_count: int = 5,
    col_count: int = 5,
) -> StepResult:
    return StepResult(
        end_cause=None,
        grid_cells=tuple(tuple(Cell(r, c) for c in range(col_count)) for r in range(row_count)),
        snake_cells=frozenset({head, *body, tail or head}),
        head=head,
        tail=tail or head,
        heading=heading,
        last_turn=Turn.ahead,
        just_ate=False,
        food=food,
    )


# ====================  Shape  ====================


def test_sees_fifteen_numbers():
    sut = Eye()
    assert len(sut.see(make_result(Cell(2, 2), Direction.up))) == 15
    assert sut.output_count == 15


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
    assert all(-1 <= value <= 1 for value in seen[FOOD_AHEAD:ROOM_LEFT])
    assert all(0 <= value <= 1 for value in seen[ROOM_LEFT:TAIL_AHEAD])
    assert all(-1 <= value <= 1 for value in seen[TAIL_AHEAD:TAIL_REACH_LEFT])
    assert all(value in (0.0, 1.0) for value in seen[TAIL_REACH_LEFT:])


# ====================  Room  ====================


def test_open_space_has_full_room_every_way():
    seen = Eye().see(make_result(Cell(2, 2), Direction.up))
    assert seen[ROOM_LEFT] == seen[ROOM_AHEAD] == seen[ROOM_RIGHT] == 1.0


def test_turn_into_a_pocket_has_little_room():
    # The body walls off column 0 and (2,1): 6 of the 20 free cells lie that way
    body = (Cell(0, 1), Cell(1, 1), Cell(3, 1), Cell(4, 1))
    seen = Eye().see(make_result(Cell(2, 2), Direction.up, body=body))
    assert seen[ROOM_LEFT] == pytest.approx(6 / 20)
    assert seen[ROOM_AHEAD] == pytest.approx(14 / 20)
    assert seen[ROOM_RIGHT] == pytest.approx(14 / 20)


def test_blocked_turn_has_no_room():
    # Wall ahead, body to the right
    seen = Eye().see(make_result(Cell(0, 2), Direction.up, body=(Cell(0, 3),)))
    assert seen[ROOM_AHEAD] == 0.0
    assert seen[ROOM_RIGHT] == 0.0
    assert seen[ROOM_LEFT] > 0.0


def test_room_follows_the_heading():
    # The same pocket on the west side, seen heading down: it is now to the right
    body = (Cell(0, 1), Cell(1, 1), Cell(3, 1), Cell(4, 1))
    seen = Eye().see(make_result(Cell(2, 2), Direction.down, body=body))
    assert seen[ROOM_RIGHT] == pytest.approx(6 / 20)


# ====================  Tail  ====================


def test_tail_behind():
    seen = Eye().see(make_result(Cell(2, 2), Direction.up, body=(Cell(3, 2),), tail=Cell(4, 2)))
    assert seen[TAIL_AHEAD] == pytest.approx(-0.4)
    assert seen[TAIL_RIGHT] == 0


def test_tail_right_follows_the_heading():
    # The same tail cell, east of the head
    heading_up = Eye().see(make_result(Cell(2, 2), Direction.up, body=(Cell(2, 3),), tail=Cell(2, 4)))
    heading_down = Eye().see(make_result(Cell(2, 2), Direction.down, body=(Cell(2, 3),), tail=Cell(2, 4)))
    assert heading_up[TAIL_RIGHT] == pytest.approx(0.4)
    assert heading_down[TAIL_RIGHT] == pytest.approx(-0.4)


def test_open_space_reaches_the_tail_every_way():
    seen = Eye().see(make_result(Cell(2, 2), Direction.up, tail=Cell(3, 2)))
    assert seen[TAIL_REACH_LEFT] == seen[TAIL_REACH_AHEAD] == seen[TAIL_REACH_RIGHT] == 1.0


def test_turn_cut_off_from_the_tail_cannot_reach_it():
    # The body walls off column 0 and (2,1); the tail lies on the other side
    body = (Cell(0, 1), Cell(1, 1), Cell(3, 1), Cell(4, 1), Cell(4, 2))
    seen = Eye().see(make_result(Cell(2, 2), Direction.up, body=body, tail=Cell(4, 3)))
    assert seen[TAIL_REACH_LEFT] == 0.0
    assert seen[TAIL_REACH_AHEAD] == 1.0
    assert seen[TAIL_REACH_RIGHT] == 1.0


def test_blocked_turn_cannot_reach_the_tail():
    seen = Eye().see(make_result(Cell(0, 2), Direction.up, tail=Cell(1, 2)))
    assert seen[TAIL_REACH_AHEAD] == 0.0


def test_moving_onto_the_tail_reaches_it():
    # Tail (2,1) -> (3,1) -> (3,2) -> head (2,2), heading up: turning left enters the tail's cell
    seen = Eye().see(make_result(Cell(2, 2), Direction.up, body=(Cell(3, 1), Cell(3, 2)), tail=Cell(2, 1)))
    assert seen[TAIL_REACH_LEFT] == 1.0
