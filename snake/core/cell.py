from dataclasses import dataclass
from snake.core.direction import Direction


@dataclass(frozen=True)
class Cell:
    # Immutable and hashable, so it can be compared, used in sets and as dict keys
    row: int
    col: int

    def __add__(self, direction: Direction) -> "Cell":
        row_delta, col_delta = direction.step_delta
        return Cell(self.row + row_delta, self.col + col_delta)
