from src.game.global_refs import CellType
from src.game.cell import Cell


class PathFactory:
    @staticmethod
    def _create_func(cell: Cell):
        def func(*args, **kwargs):
            return cell

        return func

    @staticmethod
    def make_list(pattern: str) -> list[Cell]:
        map = {
            "b": CellType.blank,
            "f": CellType.food,
            "s": CellType.snake,
            "w": CellType.wall,
        }
        res: list[Cell] = []
        for i, char in enumerate(pattern):
            type = map[char]
            cell = Cell(None, None, type)
            res.append(cell)
        return res

    @staticmethod
    def link(cells: list[Cell]) -> Cell:
        for i, cell in enumerate(cells[:-1]):
            next = cells[i + 1]
            cell.get_neighbour = PathFactory._create_func(next)
        return cells[0]

    @staticmethod
    def make_chain(pattern: str) -> Cell:
        cells = PathFactory.make_list(pattern)
        PathFactory.link(cells)
        return cells[0]

    @staticmethod
    def neighbour_maker(*args):
        neighbour = Cell()
        neighbour.get_neighbour = PathFactory.neighbour_maker
        return neighbour

    @staticmethod
    def make_infinite_chain() -> Cell:
        origin = Cell()
        origin.get_neighbour = PathFactory.neighbour_maker
        return origin
