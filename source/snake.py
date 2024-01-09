from source.cell import Cell
from source.event_hub import EventHub
from source.global_refs import Direction
from collections import deque
from source.looper import Looper


class Snake:
    _cells: deque[Cell]
    _direction: Direction
    _events: EventHub
    _looper: Looper
    _steps_taken: int

    def __init__(self, only_cell: Cell, events: EventHub = None) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_snake()
        self._direction = Direction.left
        self._events = events
        self._looper = None
        self._steps_taken = 0

    def get_head(self):  # todo: see if you can remove this
        return self._cells[-1]

    def get_tail(self):  # todo: see if you can remove this
        return self._cells[0]

    def get_length(self):  # todo: see if you can remove this
        return len(self._cells)

    def step(self):
        diff = []
        head = self.get_head()
        destination = head.get_neighbour(self._direction)
        is_fed = destination.is_food()
        should_die = destination.is_wall() or destination.is_snake()
        should_live = not should_die
        if should_die:
            if self._looper is not None:
                self._looper.stop()
            if self._events.died is not None:
                self._events.died.emit(self.get_length())
        else:
            destination.be_snake()
            self._cells.append(destination)
            diff.append(destination)
        if is_fed:
            if self._events.ate is not None:  # todo: Replace with init validation
                self._events.ate.emit()
        else:
            if should_live:
                previous_tail = self._cells.popleft()
                previous_tail.be_blank()
                diff.append(previous_tail)
        if self._events.stepped is not None:
            self._events.stepped.emit(diff)

    async def run(self, interval: float = 0.5, steps_to_take: int = None):
        self._looper = Looper(self.step, interval=interval, iterations=steps_to_take)
        await self._looper.start()
