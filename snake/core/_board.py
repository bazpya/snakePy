from dataclasses import dataclass
from snake.core.cell import Cell


@dataclass(frozen=True)
class Board:
    # Playable area only; anything outside it counts as wall
    row_count: int
    col_count: int

    def __post_init__(self) -> None:
        if self.row_count < 1 or self.col_count < 1:
            raise ValueError(f"Board must be at least 1x1, got {self.row_count}x{self.col_count}")
        # Built once; frozen dataclass, so bypass its __setattr__
        cell_rows = tuple(
            tuple(Cell(r, c) for c in range(self.col_count))
            for r in range(self.row_count)
        )
        object.__setattr__(self, "_cell_rows", cell_rows)

    def excludes(self, cell: Cell) -> bool:
        is_inside = 0 <= cell.row < self.row_count and 0 <= cell.col < self.col_count
        return not is_inside

    def get_cells_flat(self) -> list[Cell]:
        return [cell for row in self._cell_rows for cell in row]

    def get_cell_rows(self) -> tuple[tuple[Cell, ...], ...]:
        # Top to bottom; each row left to right
        return self._cell_rows
