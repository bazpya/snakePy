from snake.core._grid import Grid
from snake.core.cell import Cell
from snake.core.end_cause import EndCause
from snake.core.food_placer_concept import FoodPlacerConcept
from snake.core._snake import Snake
from snake.core.step_result import StepResult
from snake.core.turn import Turn


class World:
    # The rules of one round; no looping, timing, input or drawing

    def __init__(
        self,
        grid: Grid,
        snake: Snake,
        food_placer: FoodPlacerConcept,
        unfed_step_limit: int | None = None,  # None: the snake never starves
    ) -> None:
        self._grid = grid
        self._snake = snake
        self._food_placer = food_placer
        self._unfed_step_limit = unfed_step_limit
        self._unfed_step_count = 0
        self._end_cause: EndCause | None = None
        self._heading = snake.direction
        self._last_turn = Turn.ahead
        self._just_ate = False
        self._food: Cell | None = food_placer.place_food(
            self._get_free_cells()
        )
        self._initial_result = self._make_result()

    # ====================  Queries  ====================

    @property
    def initial_result(self) -> StepResult:
        # How the game began, as step 0; fixed, unlike the result of each step
        return self._initial_result

    # ====================  Commands  ====================

    def step(self, turn: Turn) -> StepResult:
        if self._end_cause is not None:
            raise RuntimeError("The game is over")
        self._snake.turn(turn)
        self._heading = self._snake.direction.turn(turn)  # set here, so a crash reports it too
        self._last_turn = turn
        self._just_ate = False

        next_head = self._snake.next_head
        if self._grid.excludes(next_head) or self._snake.is_hitting_itself():
            self._end_cause = EndCause.crashed
            return self._make_result()

        self._just_ate = next_head == self._food
        self._snake.step(grow=self._just_ate)

        if self._just_ate:
            self._unfed_step_count = 0
            free = self._get_free_cells()
            if free:
                self._food = self._food_placer.place_food(free)
            else:
                self._food = None
                self._end_cause = EndCause.won
        else:
            self._unfed_step_count += 1
            if self._is_starved():
                self._end_cause = EndCause.starved

        return self._make_result()

    # ====================  Helpers  ====================

    def _is_starved(self) -> bool:
        return self._unfed_step_limit is not None and self._unfed_step_count >= self._unfed_step_limit

    def _get_free_cells(self) -> list[Cell]:
        snake_cells = self._snake.cells
        return [
            cell for cell in self._grid.get_cells_flat()
            if cell not in snake_cells
        ]

    def _make_result(self) -> StepResult:
        return StepResult(
            end_cause=self._end_cause,
            grid_cells=self._grid.get_cell_rows(),
            snake_cells=self._snake.cells,
            head=self._snake.head,
            tail=self._snake.tail,
            heading=self._heading,
            last_turn=self._last_turn,
            just_ate=self._just_ate,
            food=self._food,
        )
