from src.game.game import Game
from src.game.Diff import GameDiff
from src.game.cell import Cell
from src.game.global_refs import CellType
from src.game.graphics import GraphWin, Point, Rectangle


class Drawer:
    _window: GraphWin
    _cell_size: int
    _game: Game
    _colour_map = {
        CellType.wall: "red",
        CellType.blank: "black",
        CellType.snake: "lime",
        CellType.food: "yellow",
    }

    def __init__(self, cell_size: int):
        self._cell_size = cell_size

    def bind(self, game: Game):
        height = game._row_count * self._cell_size
        width = game._col_count * self._cell_size
        game.events.ready_to_draw.subscribe(self.draw_diff)
        self._window = GraphWin("snakePy", width, height)
        self._draw(game.get_cells())
        self._game = game

    def _draw(self, cells: list[Cell]) -> None:
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

    def draw_diff(self, diff: GameDiff):
        self._draw(diff.flatten())

    def getMouse(self):
        return self._window.getMouse()
