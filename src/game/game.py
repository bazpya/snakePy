from src.game.grid import Grid
from src.game.diff import GameDiff, SnakeDiff
from src.game.Result import GameResult, SnakeResult
from src.game.direction import Direction, Turn
from src.game.event_hub import EventHub
from src.game.cell import Cell
from src.game.snake import Snake


class Game:
    _snake: Snake
    _grid: Grid
    events: EventHub
    _diff: GameDiff
    _steps_to_take: int
    _last_food: Cell = None

    def __init__(
        self,
        row_count: int,
        col_count: int = 0,
        init_food_count: int = 0,  # todo: Swap with steps_to_take
        steps_to_take: int = 0,
    ) -> None:
        self._grid = Grid(row_count, col_count)
        self._steps_to_take = steps_to_take
        self.events = EventHub()
        self._diff = GameDiff()
        self._init_food_count = init_food_count if init_food_count else 1
        self._add_snake()
        self._give_food(self._init_food_count)
        self._bind()

    def _purge_diff(self) -> None:
        self._diff = GameDiff()

    def _give_food(self, count: int = 1) -> Cell:
        cells = self._grid.get_random_blanks(count)
        for initial_food in cells[:-1]:
            initial_food.be_food()
        current_food = cells[-1]
        current_food.be_food()
        self._last_food = current_food
        if count == 1:
            self._diff.set_food(current_food)

    def _add_snake(self) -> None:
        centre = self._grid._get_origin()
        if not centre.is_blank():
            raise ValueError("The centre cell is not blank!")
        self._snake = Snake(centre, self._steps_to_take)

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
