from source.cell import Cell
from source.global_refs import Direction
from collections import deque


class Worm:
    _cells: deque[Cell]
    _direction: Direction

    def __init__(self, only_cell: Cell) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_worm()
        self._direction = Direction.up

    def get_head(self):
        return self._cells[-1]

    def get_tail(self):
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self):
        head = self.get_head()
        destination = head.get_neighbour(self._direction)
        self._cells.append(destination)
        is_growing = destination.is_food()
        if is_growing:
            pass
        else:
            previous_tail = self._cells.popleft()
            previous_tail.be_blank()
        destination.be_worm()
