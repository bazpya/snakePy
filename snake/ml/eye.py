from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.eye_concept import EyeConcept


class Eye(EyeConcept):
    # Turns a step result into numbers for the brain, as seen from the snake's heading:
    # danger on 5 rays (ahead, left, right, ahead-left, ahead-right), food ahead and right,
    # room after turning left, going ahead and turning right, tail ahead and right,
    # then whether the tail can still be reached after turning left, going ahead and turning right

    @property
    def output_count(self) -> int:
        return 15

    def see(self, result: StepResult) -> list[float]:
        heading = result.heading
        left = heading.turn(Turn.left)
        right = heading.turn(Turn.right)
        rays = ((heading,), (left,), (right,), (heading, left), (heading, right))
        safe_cells = {cell for row in result.grid_cells for cell in row} - result.snake_cells
        dangers = [self._get_danger(result.head, ray, safe_cells) for ray in rays]
        food = self._get_offset(result, result.food, heading, right)
        turn_cells = [result.head + direction for direction in (left, heading, right)]
        rooms = [self._get_room(cell, safe_cells) for cell in turn_cells]
        tail = self._get_offset(result, result.tail, heading, right)
        tail_reaches = [self._get_tail_reach(cell, result.tail, safe_cells) for cell in turn_cells]
        return dangers + food + rooms + tail + tail_reaches

    # ====================  Helpers  ====================

    def _get_danger(self, head: Cell, ray: tuple[Direction, ...], safe_cells: set[Cell]) -> float:
        # 1 / distance to the first unsafe cell (wall or body) along the ray; 1 is the next cell
        cell = self._step(head, ray)
        distance = 1
        while cell in safe_cells:
            cell = self._step(cell, ray)
            distance += 1
        return 1 / distance

    def _get_offset(self, result: StepResult, target: Cell | None, heading: Direction, right: Direction) -> list[float]:
        # Target's offset from the head, along and across the heading, scaled by the grid's larger side
        if target is None:
            return [0.0, 0.0]
        offset = (target.row - result.head.row, target.col - result.head.col)
        scale = max(len(result.grid_cells), len(result.grid_cells[0]))
        return [
            self._project(offset, heading) / scale,
            self._project(offset, right) / scale,
        ]

    def _get_room(self, start: Cell, safe_cells: set[Cell]) -> float:
        # Share of the safe cells reachable from start; 0 when start is unsafe
        return len(self._flood(start, safe_cells)) / len(safe_cells) if start in safe_cells else 0.0

    def _get_tail_reach(self, start: Cell, tail: Cell, safe_cells: set[Cell]) -> float:
        # 1 when the tail can be reached from start: on it, or next to a reachable cell; else 0
        if start == tail:
            return 1.0  # the tail moves away as the head moves in
        if start not in safe_cells:
            return 0.0
        reached = self._flood(start, safe_cells)
        return 1.0 if any(tail + direction in reached for direction in Direction) else 0.0

    @staticmethod
    def _flood(start: Cell, safe_cells: set[Cell]) -> set[Cell]:
        # Every safe cell reachable from start, start included
        reached = {start}
        frontier = [start]
        while frontier:
            cell = frontier.pop()
            for direction in Direction:
                neighbour = cell + direction
                if neighbour in safe_cells and neighbour not in reached:
                    reached.add(neighbour)
                    frontier.append(neighbour)
        return reached

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
