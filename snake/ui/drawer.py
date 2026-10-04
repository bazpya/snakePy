from snake.core import Cell, StepResult
from snake.ui.canvas_concept import CanvasConcept
from snake.ui.colour import Colour


class Drawer:
    # Shows the game; recolours only the cells that changed, for speed

    def __init__(self, canvas: CanvasConcept) -> None:
        self._canvas = canvas
        self._previous: StepResult | None = None

    # ====================  Commands  ====================

    def on_started(self, result: StepResult) -> None:
        for row in result.cell_rows:
            for cell in row:
                self._canvas.fill(cell, self._get_colour(result, cell))
        self._previous = result

    def on_stepped(self, result: StepResult) -> None:
        for cell in self._get_diff_cells(result):
            self._canvas.fill(cell, self._get_colour(result, cell))
        if result.is_over:
            self._canvas.show_message("Game over")
        self._previous = result

    # ====================  Helpers  ====================

    def _get_diff_cells(self, result: StepResult) -> set[Cell]:
        # Cells whose state changed since the previous result
        previous = self._previous
        cells = set(previous.snake_cells ^ result.snake_cells)  # entered or left
        if previous.head != result.head:
            cells.update((previous.head, result.head))  # old head is now body
        if previous.food != result.food:
            cells.update(cell for cell in (previous.food, result.food) if cell is not None)
        return cells

    @staticmethod
    def _get_colour(result: StepResult, cell: Cell) -> Colour:
        if cell == result.head:
            return Colour.head
        if cell in result.snake_cells:
            return Colour.body
        if cell == result.food:
            return Colour.food
        return Colour.empty
