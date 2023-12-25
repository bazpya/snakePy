from source.cell import Cell


class Game:
    def __init__(self, rows: int, columns: int):
        self.__cells__ = []

        for row_index in range(rows):
            row = []
            for col_index in range(columns):
                cell = Cell()
                row.append(cell)
            self.__cells__.append(row)
        pass

        # todo: Link neighbours
