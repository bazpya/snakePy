from source.cell import Cell
from source.global_refs import Direction
from collections import deque


class Worm:
    _cells: deque[Cell]

    def __init__(self, only_cell: Cell) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_worm()

    def get_head(self):
        return self._cells[-1]

    def get_tail(self):
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self, dir: Direction):
        head = self.get_head()
        next_cell = head.get_neighbour(dir)
        next_cell.be_worm()
        self._cells.append(next_cell)
        self._cells.popleft()
