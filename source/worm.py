from source.cell import Cell
from source.event_hub import EventHub
from source.global_refs import Direction
from collections import deque


class Worm:
    _cells: deque[Cell]
    _direction: Direction
    _events: EventHub

    def __init__(self, only_cell: Cell, events: EventHub = None) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_worm()
        self._direction = Direction.up
        self._events = events

    def get_head(self):
        return self._cells[-1]

    def get_tail(self):
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self):
        head = self.get_head()
        destination = head.get_neighbour(self._direction)
        is_fed = destination.is_food()
        should_die = destination.is_wall() or destination.is_worm()
        if should_die:
            if self._events.died is not None:
                self._events.died.emit()
        else:
            destination.be_worm()
            self._cells.append(destination)
        if is_fed:
            if self._events.ate is not None:
                self._events.ate.emit()
        else:
            previous_tail = self._cells.popleft()
            previous_tail.be_blank()
        if self._events.stepped is not None:
            self._events.stepped.emit()
