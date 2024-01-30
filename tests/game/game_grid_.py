from src.game.cell import Cell
from src.game.direction import Direction
from tests.game.game_ import Game_


class Game_grid_(Game_):
    def test_middle_cells_have_all_neighbours(self):
        def visit(cell: Cell, ri, ci, acc):
            for dir in Direction:
                self.assertIsNotNone(cell.get_neighbour(dir))

        self.sut.iterate_cells(False, visit)

    def test_first_row_lack_up_neighbours(self):
        first_row = self.sut._cells[0]
        for c in range(self.col_count):
            cell = first_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.up))

    def test_first_row_have_down_neighbours(self):
        first_row = self.sut._cells[0]
        for c in range(self.col_count):
            cell = first_row[c]
            self.assertIsNotNone(cell.get_neighbour(Direction.down))

    def test_last_row_have_up_neighbours(self):
        last_row = self.sut._cells[-1]
        for c in range(self.col_count):
            cell = last_row[c]
            self.assertIsNotNone(cell.get_neighbour(Direction.up))

    def test_last_row_lack_down_neighbours(self):
        last_row = self.sut._cells[-1]
        for c in range(self.col_count):
            cell = last_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.down))

    def test_first_col_lack_left_neighbours(self):
        for r in range(self.row_count):
            cell = self.sut._cells[r][0]
            self.assertIsNone(cell.get_neighbour(Direction.left))

    def test_first_col_have_right_neighbours(self):
        for r in range(self.row_count):
            cell = self.sut._cells[r][0]
            self.assertIsNotNone(cell.get_neighbour(Direction.right))

    def test_last_col_have_left_neighbours(self):
        for r in range(self.row_count):
            cell = self.sut._cells[r][-1]
            self.assertIsNotNone(cell.get_neighbour(Direction.left))

    def test_last_col_lack_right_neighbours(self):
        for r in range(self.row_count):
            cell = self.sut._cells[r][-1]
            self.assertIsNone(cell.get_neighbour(Direction.right))
