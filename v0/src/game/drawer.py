from src.config import config
from src.game.game import Game
from src.game.diff import GameDiff
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

    def __init__(self, game: Game, cell_size: int = 0) -> None:
        self._cell_size = cell_size or config.game.cell_size
        self._shapes = dict()
        if game:
            self._bind(game)

    def _bind(self, game: Game) -> None:
        height = game._grid.row_count * self._cell_size
        width = game._grid.col_count * self._cell_size
        game.events.stepped.subscribe(self.draw_diff)
        self._window = GraphWin("snakePy", width, height)
        self._draw_init(game._grid.get_flat())
        self._game = game

    def _draw_init(self, cells: list[Cell]) -> None:
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
            self._shapes[(ri, ci)] = square
            colour = self._colour_map[cell.type]
            square.setFill(colour)
            square.draw(self._window)

    def _update(self, cells: list[Cell]) -> None:
        for cell in cells:
            square = self._shapes[(cell._row, cell._col)]
            colour = self._colour_map[cell.type]
            square.setFill(colour)

    def draw_diff(self, diff: GameDiff) -> None:
        self._update(diff.flatten())

    def getMouse(self) -> None:
        return self._window.getMouse()
