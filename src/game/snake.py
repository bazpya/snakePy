from collections import deque
from src.game.diff import SnakeDiff
from src.game.global_refs import CauseOfDeath
from src.game.Result import SnakeResult
from src.game.cell import Cell
from src.game.direction import Direction, Turn
from src.game.event_hub import EventHub
from src.game.looper_interval import LooperInterval
from src.game.looper_sync import LooperSync


class Snake:
    _cells: deque[Cell]
    _cells_visited: set[Cell]
    _direction: Direction
    _events: EventHub
    _steps_taken: int
    _steps_to_take: int
    _directions: deque[Direction]
    _diff: SnakeDiff
    _is_dead: bool
    ms = 0.001

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
        self._diff = SnakeDiff()
        self._is_dead = False
        self._cells_visited = set([only_cell])

    def get_head(self) -> Cell:
        return self._cells[-1]

    def get_tail(self) -> Cell:
        return self._cells[0]

    def get_length(self):
        return len(self._cells)

    def step(self) -> None:
        self._steps_taken += 1
        next = self._get_next_cell()
        if next.is_deadly():
            cause = CauseOfDeath.wall if next.is_wall() else CauseOfDeath.snake
            self._die(cause)
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

    def _move_head(self, cell: Cell) -> None:
        self._cells_visited.add(cell)
        cell.be_snake()
        self._cells.append(cell)
        self._diff.set_snake(cell)

    def _drag_tail(self) -> None:
        tail = self._cells.popleft()
        tail.be_blank()
        self._diff.set_blank(tail)

    def _after_step(self) -> None:
        if self._events.stepped is not None:
            self._events.stepped.emit(self._diff)
        self._purge_diff()

    def _die(self, cause: CauseOfDeath = CauseOfDeath.steps_taken) -> None:
        if self._is_dead:
            return
        if self._looper:
            self._is_dead = True
            self._looper.stop()
        if self._events.died is not None:
            result = SnakeResult(
                self._steps_taken,
                self.get_length(),
                cause,
                len(self._cells_visited),
            )
            self._events.died.emit(result)

    def _purge_diff(self) -> None:
        self._diff = SnakeDiff()

    def _get_latest_input(self) -> Direction:
        return self._directions[-1] if self._directions else self._direction

    def _direction_deque(self) -> Direction:
        return self._directions.popleft() if self._directions else self._direction

    def direction_enque(self, dir: Direction) -> None:
        last = self._get_latest_input()
        if dir.is_aligned(last):
            return
        self._directions.append(dir)

    def turn(self, turn: Turn) -> None:
        latest_input = self._get_latest_input()
        next_dir = latest_input.turn(turn)
        self.direction_enque(next_dir)

    async def run_async(self, interval: float = ms) -> None:
        self._looper = LooperInterval(
            func=self.step,
            interval=interval,
            iterations=self._steps_to_take,
            end_callback=self._die,
        )
        await self._looper.start()

    def run_sync(self) -> None:
        self._looper = LooperSync(
            func=self.step,
            iterations=self._steps_to_take,
            end_callback=self._die,
        )
        self._looper.start()
