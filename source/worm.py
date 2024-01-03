from source.cell import Cell
from source.event import Event
from source.global_refs import Direction
from collections import deque


class Worm:
    _cells: deque[Cell]
    _direction: Direction
    _step_event: Event
    _ate_event: Event
    _death_event: Event

    def __init__(
        self,
        only_cell: Cell,
        step_event: Event = None,
        ate_event: Event = None,
        death_event: Event = None,
    ) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_worm()
        self._direction = Direction.up
        self._step_event = step_event
        self._ate_event = ate_event
        self._death_event = death_event

    def get_head(self):
        return self._cells[-1]

    def get_tail(self):
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self):
        head = self.get_head()
        destination = head.get_neighbour(self._direction)
        should_stay_same_length = destination.is_food() == False
        should_die = destination.is_wall() or destination.is_worm()
        if should_die:
            if self._death_event is not None:
                self._death_event.emit()
                return
        if should_stay_same_length:
            previous_tail = self._cells.popleft()
            previous_tail.be_blank()
        destination.be_worm()
        self._cells.append(destination)
        if self._step_event is not None:
            self._step_event.emit()
        if self._ate_event is not None:
            self._ate_event.emit()
