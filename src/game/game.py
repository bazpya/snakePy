from src.game.grid import Grid
from src.game.diff import GameDiff, SnakeDiff
from src.game.result import GameResult, SnakeResult
from src.game.direction import Direction, Turn
from src.game.event_hub import EventHub
from src.game.cell import Cell
from src.game.snake import Snake


class Game:
    _snake: Snake
    _grid: Grid
    events: EventHub
    _diff: GameDiff
    _last_food: Cell = None

    def __init__(self, grid: Grid = None, snake: Snake = None) -> None:
        self._grid = grid if grid else Grid()
        self.events = EventHub()
        self._diff = GameDiff()
        if snake:
            self._snake = snake
        else:
            origin = self._grid._get_origin()
            self._snake = Snake(origin)

        self._give_food(is_init=True)
        self._bind()

    def _purge_diff(self) -> None:
        self._diff = GameDiff()

    def _give_food(self, is_init: bool = False) -> Cell:
        cell = self._grid.get_random_blanks(1)[0]
        cell.be_food()
        self._last_food = cell
        if not is_init:
            self._diff.set_food(cell)

    def _bind(self, snake: Snake = None) -> None:
        s = snake if snake else self._snake
        self._snake = s
        s._events.stepped.subscribe(self._on_stepped)
        s._events.ate.subscribe(self._on_ate)
        s._events.died.subscribe(self._on_died)

    def _on_stepped(self, snake_diff: SnakeDiff) -> None:
        self._diff.add(snake_diff)
        self.events.stepped.emit(self._diff)
        self._purge_diff()

    def _on_ate(self) -> None:
        self._give_food()
        self.events.ate.emit()

    def _on_died(self, snake_res: SnakeResult) -> None:
        res = GameResult(self._grid.row_count, self._grid.col_count, snake_res)
        self.events.died.emit(res)

    def run_sync(self) -> None:
        self._snake.run_sync()

    async def run_async(self, interval: float = 0.5) -> None:
        await self._snake.run_async(interval)

    def steering_enque(self, dir: Direction) -> None:
        self._snake.direction_enque(dir)

    def turn(self, turn: Turn) -> None:
        self._snake.turn(turn)

    def get_head(self) -> Cell:
        return self._snake.get_head()

    def get_current_food(self) -> Cell:
        return self._last_food
