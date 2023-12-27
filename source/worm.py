from source.cell import Cell
from source.global_refs import Direction


class Worm:
    _cells: list[Cell]
    _head: Cell
    _tail: Cell

    def __init__(self, only_cell: Cell) -> None:
        self._cells = []
        self._cells.append(only_cell)
        self._head = only_cell
        self._tail = only_cell
        only_cell.be_worm()

    def get_length(self):
        return len(self._cells)

    def step(self, dir: Direction):
        next_head = self._head.get_neighbour(dir)
        self._head = next_head
