import dataclasses
import pytest
from snake.core.direction import Direction
from snake.core.cell import Cell


def test_equality_by_value():
    assert Cell(1, 2) == Cell(1, 2)
    assert Cell(1, 2) != Cell(2, 1)


def test_is_hashable():
    assert len({Cell(1, 2), Cell(1, 2), Cell(3, 4)}) == 2


def test_is_immutable():
    sut = Cell(1, 2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        sut.row = 5


@pytest.mark.parametrize(
    "dir, expected",
    [
        (Direction.up, Cell(4, 5)),
        (Direction.right, Cell(5, 6)),
        (Direction.down, Cell(6, 5)),
        (Direction.left, Cell(5, 4)),
    ],
)
def test_add_direction_gives_neighbour(dir, expected):
    assert Cell(5, 5) + dir == expected


def test_add_does_not_change_original():
    sut = Cell(5, 5)
    etc = sut + Direction.up
    assert sut == Cell(5, 5)
