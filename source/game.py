from source.global_refs import Direction
from source.cell import Cell


class Game:
    def __init__(self, row_count: int, col_count: int):
        self.row_count = row_count
        self.col_count = col_count
        self.__cells__ = []

        for row_index in range(row_count):
            row = []
            for col_index in range(col_count):
                cell = Cell()
                row.append(cell)
            self.__cells__.append(row)
        self.__link_neighbours()

    def __link_neighbours(self):
        for row_index in range(self.row_count):
            for col_index in range(self.col_count):
                this_cell = self.__cells__[row_index][col_index]

                has_up_neighbour = row_index != 0
                has_left_neighbour = col_index != 0

                if has_up_neighbour:
                    up_neighbour = self.__cells__[row_index - 1][col_index]
                    this_cell.set_neighbour(Direction.up, up_neighbour)
                    up_neighbour.set_neighbour(Direction.down, this_cell)

                if has_left_neighbour:
                    left_neighbour = self.__cells__[row_index][col_index - 1]
                    this_cell.set_neighbour(Direction.left, left_neighbour)
                    left_neighbour.set_neighbour(Direction.right, this_cell)
