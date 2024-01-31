from src.game.direction import Direction
from src.game.global_refs import CellType


class Cell:
    def __init__(
        self,
        row: int = None,
        col: int = None,
        type: CellType = CellType.blank,
    ):
        self._row = row
        self._col = col
        self.type = type
        self.type: CellType
        self._neighbours = {
            Direction.up: None,
            Direction.right: None,
            Direction.down: None,
            Direction.left: None,
        }

    # ====================  Type Setters  ====================

    def be_blank(self) -> None:
        self.type = CellType.blank

    def be_wall(self) -> None:
        self.type = CellType.wall

    def be_snake(self) -> None:
        self.type = CellType.snake

    def be_food(self) -> None:
        self.type = CellType.food

    # ====================  Type Getters  ====================

    def is_blank(self) -> bool:
        return self.type == CellType.blank

    def is_wall(self) -> bool:
        return self.type == CellType.wall

    def is_snake(self) -> bool:
        return self.type == CellType.snake

    def is_food(self) -> bool:
        return self.type == CellType.food

    def is_deadly(self) -> bool:
        return self.is_wall() or self.is_snake()

    # ====================  Neighbours  ====================

    def set_neighbour(self, direction: Direction, neighbour: "Cell") -> None:
        self._neighbours[direction] = neighbour

    def get_neighbour(self, direction: Direction) -> "Cell":
        return self._neighbours[direction]
