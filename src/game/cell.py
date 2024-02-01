import math
from typing import Tuple
from src.game.direction import Direction
from src.game.global_refs import CellType


class Cell:
    def __init__(
        self,
        row: int = None,
        col: int = None,
        type: CellType = CellType.blank,
    ) -> None:
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

    # ====================  Distances  ====================

    def get_distance(
        self, reciprocal: bool, target: "Cell"
    ) -> Tuple[float, float, float]:
        diff_row = target._row - self._row
        diff_col = target._col - self._col
        dist = math.sqrt(diff_row**2 + diff_col**2)
        if reciprocal:
            diff_row_recip = 1 / diff_row if diff_row else 0
            diff_col_recip = 1 / diff_col if diff_col else 0
            dist_recip = 1 / dist if dist else 0
            return diff_row_recip, diff_col_recip, dist_recip
        else:
            return diff_row, diff_col, dist

    def death_distance(self, reciprocal: bool, *dirs) -> Tuple[float, float, float]:
        if not dirs:
            raise ValueError(self.death_distance.__name__ + " needs some directions")
        runner = self
        while not runner.is_deadly():
            for dir in dirs:
                runner = runner.get_neighbour(dir)
        return self.get_distance(reciprocal, runner)
