from src.config import Config
from src.game.direction import Direction
from src.game.cell import Cell
import random


class Grid:
    _cells: list[list[Cell]]
    row_count: int
    col_count: int

    def __init__(self, row_count: int = 0, col_count: int = 0) -> None:
        config = Config.get()
        if row_count:
            self.row_count = row_count
            self.col_count = col_count if col_count else row_count
        else:
            self.row_count = config.game.row_count
            self.col_count = config.game.col_count
        self._cells = []
        self._populate()
        self._link_neighbours()
        self._lay_walls()

    def _populate(self) -> None:
        for row_index in range(self.row_count):
            row = []
            for col_index in range(self.col_count):
                cell = Cell(row_index, col_index)
                row.append(cell)
            self._cells.append(row)

    def _link_neighbours(self) -> None:
        def visit(cell: Cell, ri, ci, acc):
            has_up_neighbour = ri != 0
            has_left_neighbour = ci != 0

            if has_up_neighbour:
                up_neighbour: Cell = self._cells[ri - 1][ci]
                cell.set_neighbour(Direction.up, up_neighbour)
                up_neighbour.set_neighbour(Direction.down, cell)

            if has_left_neighbour:
                left_neighbour: Cell = self._cells[ri][ci - 1]
                cell.set_neighbour(Direction.left, left_neighbour)
                left_neighbour.set_neighbour(Direction.right, cell)

        self.iterate_cells(True, visit)

    def _lay_walls(self) -> None:
        def visit(cell: Cell, ri, ci, acc):
            should_be_wall = ri in [0, self.row_count - 1] or ci in [
                0,
                self.col_count - 1,
            ]
            if should_be_wall:
                cell.be_wall()

        self.iterate_cells(True, visit)

    def iterate_cells(
        self, include_boundaries: bool, visit_func, initial_value=None
    ) -> None:
        row_ind_min = 0 if include_boundaries else 1
        row_ind_max = self.row_count if include_boundaries else self.row_count - 1
        col_ind_min = 0 if include_boundaries else 1
        col_ind_max = self.col_count if include_boundaries else self.col_count - 1
        acc = initial_value

        for ri in range(row_ind_min, row_ind_max):
            for ci in range(col_ind_min, col_ind_max):
                cell = self._cells[ri][ci]
                acc = visit_func(cell, ri, ci, acc)
        return acc

    def get_flat(self) -> list[Cell]:
        return [x for row in self._cells for x in row]

    def _get_blanks(self) -> list[Cell]:
        flat_list_of_cells = self.get_flat()
        return [x for x in flat_list_of_cells if x.is_blank()]

    def get_random_blanks(self, count: int) -> list[Cell]:
        blanks = self._get_blanks()
        return random.sample(blanks, count)

    def _get_centre(self) -> Cell:
        row = self.row_count // 2
        col = self.col_count // 2
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
