from source.cell import Cell
from source.event_hub import EventHub
from source.global_refs import Direction
from collections import deque
from source.looper_interval import LooperInterval
from source.looper_sync import LooperSync


class Snake:
    _cells: deque[Cell]
    _direction: Direction
    _events: EventHub
    _steps_taken: int
    _steering: deque[Direction]

    def __init__(self, only_cell: Cell, events: EventHub = None) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_snake()
        self._direction = Direction.left  # todo: randommise this
        self._events = events
        self._looper = None
        self._steps_taken = 0
        self._steering = deque()

    def get_head(self):  # todo: see if you can remove this
        return self._cells[-1]

    def get_tail(self):  # todo: see if you can remove this
        return self._cells[0]

    def get_length(self):  # todo: see if you can remove this
        return len(self._cells)

    def step(self):
        diff = []
        head = self.get_head()
        self._direction = self._steering_deque()
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

    async def run_async(self, interval: float = 0.5, steps_to_take: int = None):
        self._looper = LooperInterval(
            self.step, interval=interval, iterations=steps_to_take
        )
        await self._looper.start()

    def run_sync(self, steps_to_take: int = None):
        self._looper = LooperSync(self.step, iterations=steps_to_take)
        self._looper.start()

    def steering_enque(self, dir: Direction):
        if len(self._steering) > 0:
            previous = self._steering[-1]
            if dir.is_aligned(previous):
                return
        self._steering.append(dir)

    def _steering_deque(self):
        if len(self._steering) > 0:
            return self._steering.popleft()
        else:
            return self._direction
