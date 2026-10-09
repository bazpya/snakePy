from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.eye_concept import EyeConcept


class Eye(EyeConcept):
    # Turns a step result into numbers for the brain, as seen from the snake's heading:
    # danger on 5 rays (ahead, left, right, ahead-left, ahead-right), then food ahead and right

    @property
    def output_count(self) -> int:
        return 7

    def see(self, result: StepResult) -> list[float]:
        heading = result.heading
        left = heading.turn(Turn.left)
        right = heading.turn(Turn.right)
        rays = ((heading,), (left,), (right,), (heading, left), (heading, right))
        safe_cells = {cell for row in result.grid_cells for cell in row} - result.snake_cells
        dangers = [self._get_danger(result.head, ray, safe_cells) for ray in rays]
        return dangers + self._get_food(result, heading, right)

    # ====================  Helpers  ====================

    def _get_danger(self, head: Cell, ray: tuple[Direction, ...], safe_cells: set[Cell]) -> float:
        # 1 / distance to the first unsafe cell (wall or body) along the ray; 1 is the next cell
        cell = self._step(head, ray)
        distance = 1
        while cell in safe_cells:
            cell = self._step(cell, ray)
            distance += 1
        return 1 / distance

    def _get_food(self, result: StepResult, heading: Direction, right: Direction) -> list[float]:
        # Food offset along and across the heading, scaled by the grid's larger side
        if result.food is None:
            return [0.0, 0.0]
        offset = (result.food.row - result.head.row, result.food.col - result.head.col)
        scale = max(len(result.grid_cells), len(result.grid_cells[0]))
        return [
            self._project(offset, heading) / scale,
            self._project(offset, right) / scale,
        ]

    @staticmethod
    def _project(offset: tuple[int, int], direction: Direction) -> int:
        # How far the offset goes in the given direction
        row_delta, col_delta = direction.step_delta
        return offset[0] * row_delta + offset[1] * col_delta

    @staticmethod
    def _step(cell: Cell, ray: tuple[Direction, ...]) -> Cell:
        # One step along the ray; a diagonal ray moves in both directions
        for direction in ray:
            cell = cell + direction
        return cell
