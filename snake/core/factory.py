from snake.core._grid import Grid
from snake.core.cell import Cell
from snake.core.direction import Direction
from snake.core.food_placer import FoodPlacer
from snake.core.food_placer_concept import FoodPlacerConcept
from snake.core.world import World
from snake.core._snake import Snake


class Factory:
    # Keeps the settings and creates new, independent worlds from them

    def __init__(
        self,
        row_count: int,
        col_count: int,
        food_placer: FoodPlacerConcept | None = None,
        starvation_factor: float | None = None,  # None: the snake never starves
    ) -> None:
        self._grid = Grid(row_count, col_count)  # immutable, so shared
        self._food_placer = food_placer or FoodPlacer()
        self._unfed_step_limit = (
            None if starvation_factor is None
            else int(starvation_factor * row_count * col_count)  # grows with the grid
        )

    def create(self) -> World:
        snake = Snake(self._get_start(), Direction.right)
        return World(self._grid, snake, self._food_placer, self._unfed_step_limit)

    # ====================  Helpers  ====================

    def _get_start(self) -> Cell:
        # Grid centre
        return Cell(self._grid.row_count // 2, self._grid.col_count // 2)
