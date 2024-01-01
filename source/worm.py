from source.cell import Cell
from source.global_refs import Direction
from collections import deque


class Worm:
    _cells: deque[Cell]
    _direction: Direction

    def __init__(self, only_cell: Cell, death_callback=lambda: None) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_worm()
        self._direction = Direction.up
        self._death_callback = death_callback

    def get_head(self):
        return self._cells[-1]

    def get_tail(self):
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self):
        head = self.get_head()
        destination = head.get_neighbour(self._direction)
        should_grow = destination.is_food()
        should_die = destination.is_wall() or destination.is_worm()
        if should_die:
            self._death_callback()
            return
        if should_grow:
            pass
        else:
            previous_tail = self._cells.popleft()
            previous_tail.be_blank()
        destination.be_worm()
        self._cells.append(destination)
