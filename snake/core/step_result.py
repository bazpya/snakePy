from dataclasses import dataclass
from snake.core.cell import Cell
from snake.core.direction import Direction
from snake.core.end_cause import EndCause
from snake.core.turn import Turn


@dataclass(frozen=True)
class StepResult:
    end_cause: EndCause | None
    grid_cells: tuple[tuple[Cell, ...], ...]  # rows, top to bottom
    snake_cells: frozenset[Cell]
    head: Cell
    tail: Cell
    heading: Direction
    last_turn: Turn
    just_ate: bool
    food: Cell | None

    @property
    def is_over(self) -> bool:
        return self.end_cause is not None

    @property
    def snake_length(self) -> int:
        return len(self.snake_cells)

    @property
    def grid_cell_count(self) -> int:
        return sum(len(row) for row in self.grid_cells)
