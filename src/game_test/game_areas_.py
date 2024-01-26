from src.game.cell import Cell
from src.game_test.game_ import Game_


class Game_areas_(Game_):
    def test_first_row_is_wall(self):
        sut = self.make_sut()
        first_row = sut._cells[0]
        for cell in first_row:
            self.assertTrue(cell.is_wall)

    def test_last_row_is_wall(self):
        sut = self.make_sut()
        last_row = sut._cells[-1]
        for cell in last_row:
            self.assertTrue(cell.is_wall)

    def test_first_col_is_wall(self):
        sut = self.make_sut()
        for r in range(self.row_count):
            cell = sut._cells[r][0]
            self.assertTrue(cell.is_wall)

    def test_last_col_is_wall(self):
        sut = self.make_sut()
        for r in range(self.row_count):
            cell = sut._cells[r][-1]
            self.assertTrue(cell.is_wall)

    def test_interior_cells_are_blank(self):
        def visit(cell: Cell, ri, ci, acc):
            self.assertTrue(cell.is_blank() or cell == origin)

        sut = self.make_sut()
        origin = sut._snake.get_head()
        sut.iterate_cells(False, visit)
