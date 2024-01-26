from src.game.Result import GameResult, SnakeResult
from src.game.direction import Direction, Turn
from src.game.event_hub import EventHub
from src.game.cell import Cell
import random
from src.game.snake import Snake


class Game:
    _snake: Snake
    _cells: list[list[Cell]]
    _row_count: int
    _col_count: int
    _events: EventHub
    _step_diff: list[Cell]

    def __init__(
        self, row_count: int, col_count: int = None, init_food_count: int = None
    ):
        self._row_count = row_count
        self._col_count = row_count if col_count is None else col_count
        self._cells = []
        self._populate()
        self._link_neighbours()
        self._lay_walls()
        self._events = EventHub()
        self._step_diff = []
        self._add_snake()
        self._ini_food_count = init_food_count if init_food_count else 1
        self._add_food(self._ini_food_count)
        self._bind()

    def _populate(self):
        for row_index in range(self._row_count):
            row = []
            for col_index in range(self._col_count):
                cell = Cell(row_index, col_index)
                row.append(cell)
            self._cells.append(row)

    def _link_neighbours(self):
        def visit(cell: Cell, ri, ci, acc):
            has_up_neighbour = ri != 0
            has_left_neighbour = ci != 0

            if has_up_neighbour:
                up_neighbour = self._cells[ri - 1][ci]
                cell.set_neighbour(Direction.up, up_neighbour)
                up_neighbour.set_neighbour(Direction.down, cell)

            if has_left_neighbour:
                left_neighbour = self._cells[ri][ci - 1]
                cell.set_neighbour(Direction.left, left_neighbour)
                left_neighbour.set_neighbour(Direction.right, cell)

        self.iterate_cells(True, visit)

    def _lay_walls(self):
        def visit(cell, ri, ci, acc):
            should_be_wall = ri in [0, self._row_count - 1] or ci in [
                0,
                self._col_count - 1,
            ]
            if should_be_wall:
                cell.be_wall()

        self.iterate_cells(True, visit)

    def iterate_cells(self, include_boundaries: bool, visit_func, initial_value=None):
        row_index_lower_bound = 0 if include_boundaries else 1
        row_index_upper_bound = (
            self._row_count if include_boundaries else (self._row_count - 1)
        )
        col_index_lower_bound = 0 if include_boundaries else 1
        col_index_upper_bound = (
            self._col_count if include_boundaries else (self._col_count - 1)
        )

        accumulator = initial_value

        for row_index in range(row_index_lower_bound, row_index_upper_bound):
            for col_index in range(col_index_lower_bound, col_index_upper_bound):
                this_cell = self._cells[row_index][col_index]
                accumulator = visit_func(this_cell, row_index, col_index, accumulator)

        return accumulator

    def get_cells(self):
        return [x for row in self._cells for x in row]

    def _get_blank_cells(self) -> list[Cell]:
        flat_list_of_cells = self.get_cells()
        return [x for x in flat_list_of_cells if x.is_blank()]

    def _add_to_diff(self, *args):
        self._step_diff.extend(*args)

    def _purge_diff(self):
        self._step_diff.clear()

    def _add_food(self, count: int = 1) -> Cell:
        blank_cells = self._get_blank_cells()
        cells = random.sample(blank_cells, count)
        for cell in cells:
            cell.be_food()
        self._add_to_diff(cells)
        return cells

    def _get_centre(self) -> Cell:
        row = self._row_count // 2
        col = self._col_count // 2
        return self._cells[row][col]

    def _get_origin(self, hor_dir: Direction = None, ver_dir: Direction = None) -> Cell:
        runner = self._get_centre()
        if hor_dir is not None:
            while runner.get_neighbour(hor_dir).is_blank():
                runner = runner.get_neighbour(hor_dir)
        if ver_dir is not None:
            while runner.get_neighbour(ver_dir).is_blank():
                runner = runner.get_neighbour(ver_dir)
        return runner

    def _add_snake(self) -> None:
        centre = self._get_origin()
        if not centre.is_blank():
            raise ValueError("The centre cell is not blank!")
        self._snake = Snake(centre)

    def _bind(self, snake: Snake = None) -> None:
        s = snake if snake else self._snake
        self._snake = s
        s._events.stepped.subscribe(self._on_stepped)
        s._events.ate.subscribe(self._on_ate)
        s._events.died.subscribe(self._on_died)

    def _on_stepped(self, *args, **kwargs):
        self._add_to_diff(*args)
        self._events.ready_to_draw.emit(self._step_diff)
        self._purge_diff()
        self._events.stepped.emit(*args, **kwargs)

    def _on_ate(self, *args, **kwargs):
        self._events.ate.emit(*args, **kwargs)

    def _on_died(self, snake_res: SnakeResult):
        res = GameResult(self._row_count, self._col_count, [], [], snake_res)
        self._events.died.emit(res)

    def run_sync(self, steps_to_take: int = None):
        self._snake.run_sync(steps_to_take)

    async def run_async(self, interval: float = 0.5, steps_to_take: int = None):
        await self._snake.run_async(interval, steps_to_take)

    def steering_enque(self, dir: Direction):
        self._snake.direction_enque(dir)

    def turn(self, turn: Turn):
        self._snake.turn(turn)
