from dataclasses import dataclass
from snake.core.cell import Cell
from snake.core.direction import Direction


@dataclass(frozen=True)
class StepResult:
    is_over: bool
    cell_rows: tuple[tuple[Cell, ...], ...]  # rows, top to bottom
    snake_cells: frozenset[Cell]
    head: Cell
    direction: Direction  # of the last step
    food: Cell | None

    @property
    def snake_length(self) -> int:
        return len(self.snake_cells)
