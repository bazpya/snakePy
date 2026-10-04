import pytest
from snake.core.direction import Direction
from snake.core.turn import Turn


@pytest.mark.parametrize(
    "dir, delta",
    [
        (Direction.up, (-1, 0)),
        (Direction.right, (0, 1)),
        (Direction.down, (1, 0)),
        (Direction.left, (0, -1)),
    ],
)
def test_delta(dir, delta):
    assert dir.step_delta == delta


@pytest.mark.parametrize(
    "dir, opposite",
    [
        (Direction.up, Direction.down),
        (Direction.right, Direction.left),
        (Direction.down, Direction.up),
        (Direction.left, Direction.right),
    ],
)
def test_opposite(dir, opposite):
    assert dir.get_opposite() == opposite


@pytest.mark.parametrize(
    "dir, right_of_it",
    [
        (Direction.up, Direction.right),
        (Direction.right, Direction.down),
        (Direction.down, Direction.left),
        (Direction.left, Direction.up),
    ],
)
def test_turn(dir, right_of_it):
    assert dir.turn(Turn.right) == right_of_it
    assert right_of_it.turn(Turn.left) == dir
    assert dir.turn(Turn.ahead) == dir


@pytest.mark.parametrize(
    "dir, other, turn",
    [
        (Direction.up, Direction.right, Turn.right),
        (Direction.left, Direction.up, Turn.right),
        (Direction.up, Direction.left, Turn.left),
        (Direction.right, Direction.up, Turn.left),
        (Direction.up, Direction.up, Turn.ahead),
        (Direction.up, Direction.down, None),
        (Direction.left, Direction.right, None),
    ],
)
def test_get_turn_to(dir, other, turn):
    assert dir.get_turn_to(other) == turn
