from snake.core import Cell, WorldState
from snake.ui.canvas_concept import CanvasConcept
from snake.ui.colour import Colour


class Drawer:
    # Shows the game; recolours only the cells that changed, for speed

    def __init__(self, canvas: CanvasConcept) -> None:
        self._canvas = canvas
        self._previous: WorldState | None = None

    # ====================  Commands  ====================

    def on_started(self, state: WorldState) -> None:
        for row in state.grid_cells:
            for cell in row:
                self._canvas.fill(cell, self._get_colour(state, cell))
        self._show_length(state)
        self._previous = state

    def on_stepped(self, state: WorldState) -> None:
        for cell in self._get_diff_cells(state):
            self._canvas.fill(cell, self._get_colour(state, cell))
        self._show_length(state)
        if state.is_over:
            self._canvas.show_message("Game over")
        self._previous = state

    # ====================  Helpers  ====================

    def _show_length(self, state: WorldState) -> None:
        self._canvas.show_status(f"Length: {state.snake_length}")

    def _get_diff_cells(self, state: WorldState) -> set[Cell]:
        # Cells that changed since the previous state
        previous = self._previous
        cells = set(previous.snake_cells ^ state.snake_cells)  # entered or left
        if previous.head != state.head:
            cells.update((previous.head, state.head))  # old head is now body
        if previous.food != state.food:
            cells.update(cell for cell in (previous.food, state.food) if cell is not None)
        return cells

    @staticmethod
    def _get_colour(state: WorldState, cell: Cell) -> Colour:
        if cell == state.head:
            return Colour.head
        if cell in state.snake_cells:
            return Colour.body
        if cell == state.food:
            return Colour.food
        return Colour.empty
