import pytest
from snake.core.direction import Direction
from snake.core.cell import Cell
from snake.core._snake import Snake
from snake.core.turn import Turn

START = Cell(5, 5)


@pytest.fixture
def sut() -> Snake:
    return Snake(START, Direction.right)


def make_square_snake() -> Snake:
    # Body (tail -> head): (5,5) (5,6) (6,6) (6,5), heading left
    snake = Snake(START, Direction.right)
    snake.step(grow=True)
    snake.turn(Turn.right)  # down
    snake.step(grow=True)
    snake.turn(Turn.right)  # left
    snake.step(grow=True)
    return snake


def make_long_snake() -> Snake:
    # Body (tail -> head): (5,4) (5,5) (5,6) (6,6) (6,5), heading left
    snake = Snake(Cell(5, 4), Direction.right)
    snake.step(grow=True)
    snake.step(grow=True)
    snake.turn(Turn.right)  # down
    snake.step(grow=True)
    snake.turn(Turn.right)  # left
    snake.step(grow=True)
    return snake


# ====================  Start  ====================


def test_starts_with_one_cell_at_start(sut):
    assert sut.length == 1
    assert sut.head == START
    assert sut.cells == frozenset({START})


def test_starts_with_given_direction(sut):
    assert sut.direction == Direction.right


# ====================  Step  ====================


def test_next_head_follows_direction_without_moving(sut):
    assert sut.next_head == START + Direction.right
    assert sut.head == START


def test_step_without_growing_keeps_length(sut):
    sut.step()
    assert sut.head == START + Direction.right
    assert sut.length == 1
    assert sut.cells == frozenset({START + Direction.right})


def test_step_with_growing_adds_a_cell(sut):
    sut.step(grow=True)
    assert sut.length == 2
    assert sut.cells == frozenset({START, START + Direction.right})


def test_head_may_move_into_cell_the_tail_leaves():
    sut = make_square_snake()
    sut.turn(Turn.right)  # up
    assert sut.next_head == START
    sut.step()
    assert sut.head == START
    assert sut.length == 4
    assert START in sut.cells


# ====================  Turn  ====================


def test_turn_changes_next_head(sut):
    sut.turn(Turn.left)
    assert sut.next_head == START + Direction.up


def test_turn_takes_effect_on_step(sut):
    sut.turn(Turn.left)
    assert sut.direction == Direction.right
    sut.step()
    assert sut.direction == Direction.up


@pytest.mark.parametrize(
    "turn, expected",
    [
        (Turn.left, Direction.up),
        (Turn.ahead, Direction.right),
        (Turn.right, Direction.down),
    ],
)
def test_turn_is_relative_to_current_direction(sut, turn, expected):
    sut.turn(turn)
    sut.step()
    assert sut.direction == expected


def test_latest_turn_wins(sut):
    sut.turn(Turn.left)
    sut.turn(Turn.right)
    sut.step()
    assert sut.direction == Direction.down



# ====================  Self-hit  ====================


def test_is_not_hitting_itself_on_a_free_cell(sut):
    assert not sut.is_hitting_itself()


def test_is_hitting_itself_when_next_head_is_on_its_body():
    sut = make_long_snake()
    sut.turn(Turn.right)  # up, into (5,5)
    assert sut.is_hitting_itself()


def test_is_not_hitting_itself_on_the_cell_the_tail_leaves():
    sut = make_square_snake()
    sut.turn(Turn.right)  # up, into the tail's cell
    assert not sut.is_hitting_itself()
