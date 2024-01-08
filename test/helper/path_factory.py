from source.global_refs import CellType
from source.cell import Cell


class PathFactory:
    @staticmethod
    def _create_func(cell: Cell):
        def func(*args, **kwargs):
            return cell

        return func

    @staticmethod
    def make(pattern: str) -> Cell:
        handle: Cell = None
        previous: Cell = None
        map = {
            "b": CellType.blank,
            "f": CellType.food,
            "s": CellType.snake,
            "w": CellType.wall,
        }
        for i, char in enumerate(pattern):
            type = map[char]
            cell = Cell(None, None, type)
            if i == 0:
                handle = cell
            else:
                previous.get_neighbour = PathFactory._create_func(cell)
            previous = cell

        return handle

    @staticmethod
    def link(cells: list[Cell]) -> Cell:
        pass # todo
