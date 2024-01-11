from source.cell import Cell
from source.global_refs import CellType
from source.graphics import GraphWin, Point, Rectangle


class Drawer:
    _window: GraphWin
    _cell_size: int
    _row_count: int
    _col_count: int
    _colour_map = {
        CellType.wall: "red",
        CellType.blank: "black",
        CellType.snake: "lime",
        CellType.food: "yellow",
    }

    def __init__(self, cell_size: int, row_count: int, col_count: int = None):
        self._cell_size = cell_size
        self._row_count = row_count
        self._col_count = row_count if col_count is None else col_count
        height = self._row_count * self._cell_size
        width = self._col_count * self._cell_size
        self._window = GraphWin("snakePy", width, height)
        pass

    def draw(self, cells: list[Cell]) -> None:
        for cell in cells:
            ri = cell._row
            ci = cell._col

            ver_offset = ri * self._cell_size
            hor_offset = ci * self._cell_size

            left = hor_offset
            right = left + self._cell_size
            top = ver_offset
            bottom = top + self._cell_size

            point1 = Point(left, top)
            point2 = Point(right, bottom)

            square = Rectangle(point1, point2)
            cellType = cell.get_type()
            colour = self._colour_map[cellType]
            square.setFill(colour)
            square.draw(self._window)

    def getMouse(self):
        return self._window.getMouse()
