from src.game.global_refs import CellType
from src.game.cell import Cell


class CellFactory:
    _map = {
        "b": CellType.blank,
        "f": CellType.food,
        "s": CellType.snake,
        "w": CellType.wall,
    }

    @staticmethod
    def _create_func(cell: Cell):
        def func(*args, **kwargs):
            return cell

        return func

    @staticmethod
    def make_list(pattern: str) -> list[Cell]:
        res: list[Cell] = []
        for i, char in enumerate(pattern):
            type = CellFactory._map[char]
            cell = Cell(None, None, type)
            res.append(cell)
        return res

    @staticmethod
    def link(cells: list[Cell]) -> Cell:
        for i, cell in enumerate(cells[:-1]):
            next = cells[i + 1]
            cell.get_neighbour = CellFactory._create_func(next)
        return cells[0]

    @staticmethod
    def make_chain(pattern: str) -> Cell:
        cells = CellFactory.make_list(pattern)
        CellFactory.link(cells)
        return cells[0]

    @staticmethod
    def make_infinite_chain(*a) -> Cell:
        cell = Cell()
        cell.get_neighbour = CellFactory.make_infinite_chain
        return cell
