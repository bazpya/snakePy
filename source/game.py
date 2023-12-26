from source.global_refs import Direction
from source.cell import Cell


class Game:
    def __init__(self, row_count: int, col_count: int):
        self._row_count = row_count
        self._col_count = col_count
        self._cells = []
        self._populate()
        self._link_neighbours()

    def _populate(self):
        for row_index in range(self._row_count):
            row = []
            for col_index in range(self._col_count):
                cell = Cell()
                cell.row = row_index
                cell.col = col_index
                row.append(cell)
            self._cells.append(row)

    def _link_neighbours(self):
        def visit(cell, ri, ci, acc):
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
