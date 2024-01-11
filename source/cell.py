from source.direction import Direction
from source.global_refs import CellType


class CellConcept:
    pass


class Cell(CellConcept):
    def __init__(
        self, row: int = None, col: int = None, type: CellType = CellType.blank
    ):
        self._row = row
        self._col = col
        self._type = type
        self._type: CellType
        self._neighbours = {
            Direction.up: None,
            Direction.right: None,
            Direction.down: None,
            Direction.left: None,
        }

    # ====================  Type Setters  ====================

    def set_type(self, type: CellType):
        self._type = type

    def be_blank(self) -> None:
        self._type = CellType.blank

    def be_wall(self) -> None:
        self._type = CellType.wall

    def be_snake(self) -> None:
        self._type = CellType.snake

    def be_food(self) -> None:
        self._type = CellType.food

    # ====================  Type Getters  ====================

    def get_type(self) -> CellType:
        return self._type

    def is_blank(self) -> bool:
        return self._type == CellType.blank

    def is_wall(self) -> bool:
        return self._type == CellType.wall

    def is_snake(self) -> bool:
        return self._type == CellType.snake

    def is_food(self) -> bool:
        return self._type == CellType.food

    # ====================  Neighbours  ====================

    def set_neighbour(self, direction: Direction, neighbour: "Cell") -> None:
        self._neighbours[direction] = neighbour

    def get_neighbour(self, direction: Direction) -> "Cell":
        return self._neighbours[direction]
