from collections import deque
from src.game.Result import SnakeResult
from src.game.cell import Cell
from src.game.direction import Direction, Turn
from src.game.event_hub import EventHub
from src.game.looper_interval import LooperInterval
from src.game.looper_sync import LooperSync


class Snake:
    _cells: deque[Cell]
    _direction: Direction
    _events: EventHub
    _steps_taken: int
    _steps_to_take: int
    _directions: deque[Direction]
    _diff: list[Cell]

    def __init__(self, only_cell: Cell, steps_to_take: int = 0) -> None:
        self._cells = deque()
        self._cells.append(only_cell)
        only_cell.be_snake()
        self._direction = Direction.left
        self._events = EventHub()
        self._looper = None
        self._steps_taken = 0
        self._steps_to_take = steps_to_take
        self._directions = deque()
        self._diff = []

    def get_head(self):
        return self._cells[-1]

    def get_tail(self):
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self):
        self._steps_taken += 1
        next = self._get_next_cell()
        should_die = next.is_deadly() or self._steps_taken == self._steps_to_take
        if should_die:
            self._die()
        else:
            if next.is_food():
                if self._events.ate is not None:
                    self._events.ate.emit()
            else:
                self._drag_tail()
            self._move_head(next)
        self._after_step()

    def _get_next_cell(self) -> Cell:
        head = self.get_head()
        self._direction = self._direction_deque()
        return head.get_neighbour(self._direction)

    def _move_head(self, cell: Cell):
        cell.be_snake()
        self._cells.append(cell)
        self._diff.append(cell)

    def _drag_tail(self):
        tail = self._cells.popleft()
        tail.be_blank()
        self._diff.append(tail)

    def _after_step(self):
        if self._events.stepped is not None:
            self._events.stepped.emit(self._diff)
        self._diff = []

    def _die(self):
        if self._looper:
            self._looper.stop()
        if self._events.died is not None:
            result = SnakeResult(self._steps_taken, self.get_length())
            self._events.died.emit(result)

    def _get_latest_input(self):
        return self._directions[-1] if self._directions else self._direction

    def direction_enque(self, dir: Direction):
        last = self._get_latest_input()
        if dir.is_aligned(last):
            return
        self._directions.append(dir)

    def _direction_deque(self):
        return self._directions.popleft() if self._directions else self._direction

    def turn(self, turn: Turn):
        latest_input = self._get_latest_input()
        next_dir = latest_input.turn(turn)
        self.direction_enque(next_dir)

    async def run_async(self, interval: float = 0.5, steps_to_take: int = None):
        self._looper = LooperInterval(
            self.step, interval=interval, iterations=steps_to_take
        )
        await self._looper.start()

    def run_sync(self, steps_to_take: int = None):
        self._looper = LooperSync(self.step, iterations=steps_to_take)
        self._looper.start()
