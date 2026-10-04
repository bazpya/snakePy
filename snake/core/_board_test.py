import pytest
from snake.core._board import Board
from snake.core.cell import Cell


@pytest.mark.parametrize(
    "rows, cols",
    [
        (0, 3),
        (3, 0),
        (-1, 3),
    ])
def test_rejects_invalid_size(rows, cols):
    with pytest.raises(ValueError):
        Board(rows, cols)


@pytest.mark.parametrize(
    "cell",
    [
        Cell(0, 0),
        Cell(0, 3),
        Cell(2, 0),
        Cell(2, 3),
        Cell(1, 2),
    ]
)
def test_does_not_exclude_inside_and_edges(cell):
    assert not Board(3, 4).excludes(cell)


@pytest.mark.parametrize(
    "cell",
    [
        Cell(-1, 0),
        Cell(3, 0),
        Cell(0, -1),
        Cell(0, 4),
    ]
)
def test_excludes_outside(cell):
    assert Board(3, 4).excludes(cell)


def test_cells_cover_whole_board_once():
    sut = Board(3, 4)
    cells = sut.get_cells_flat()
    assert len(cells) == 12
    assert len(set(cells)) == 12
    assert not any(sut.excludes(cell) for cell in cells)


def test_cell_rows_follow_board_layout():
    sut = Board(3, 4)
    rows = sut.get_cell_rows()
    assert len(rows) == 3
    for r, row in enumerate(rows):
        assert row == tuple(Cell(r, c) for c in range(4))


def test_cell_rows_are_built_once():
    sut = Board(3, 4)
    assert sut.get_cell_rows() is sut.get_cell_rows()
