from source.event import Event
from source.event_hub import EventHub
from source.global_refs import Direction
from source.cell import Cell
import random
from source.snake import Snake


class Game:
    _snake: Snake
    _cells: list[list[Cell]]
    _row_count: int
    _col_count: int
    event_hub: EventHub
    _step_diff: list[Cell]

    def __init__(self, row_count: int, col_count: int = None):
        self._row_count = row_count
        self._col_count = row_count if col_count is None else col_count
        self._cells = []
        self._populate()
        self._link_neighbours()
        self._lay_walls()
        self.event_hub = EventHub()
        self._step_diff = []
        self._subscribe_events()

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

    def _subscribe_events(self):
        self.event_hub.stepped.subscribe(self._on_stepped)

    def _on_stepped(self, *args, **kwargs):
        self._add_to_diff(*args)
        self.event_hub.ready_to_draw.emit(self._step_diff)
        self._purge_diff()

    def get_cells(self):
        return [x for row in self._cells for x in row]

    def _get_blank_cells(self) -> list[Cell]:
        flat_list_of_cells = self.get_cells()
        return [x for x in flat_list_of_cells if x.is_blank()]

    def _add_to_diff(self, *args):
        self._step_diff.extend(*args)

    def _purge_diff(self):
        self._step_diff.clear()

    def _drop_food(self) -> Cell:
        blank_cells = self._get_blank_cells()
        food_cell = random.choice(blank_cells)
        food_cell.be_food()
        self._add_to_diff([food_cell])
        return food_cell

    def _get_centre(self) -> Cell:
        row = self._row_count // 2
        col = self._col_count // 2
        return self._cells[row][col]

    def add_snake(self):
        centre = self._get_centre()
        if not centre.is_blank():
            raise ValueError("The centre cell is not blank!")
        self._snake = Snake(centre, self.event_hub)
        return self._snake

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
