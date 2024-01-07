from test.test_game_ import Game_


class Game_areas_(Game_):
    def test_first_row_is_wall(self):
        first_row = self.initial_sut._cells[0]
        for cell in first_row:
            self.assertTrue(cell.is_wall)

    def test_last_row_is_wall(self):
        last_row = self.initial_sut._cells[-1]
        for cell in last_row:
            self.assertTrue(cell.is_wall)

    def test_first_col_is_wall(self):
        for r in range(self.row_count):
            cell = self.initial_sut._cells[r][0]
            self.assertTrue(cell.is_wall)

    def test_last_col_is_wall(self):
        for r in range(self.row_count):
            cell = self.initial_sut._cells[r][-1]
            self.assertTrue(cell.is_wall)

    def test_interior_cells_are_blank(self):
        def visit(cell, ri, ci, acc):
            self.assertTrue(cell.is_blank())

        self.initial_sut.iterate_cells(False, visit)
