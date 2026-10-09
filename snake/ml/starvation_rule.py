class StarvationRule:
    # Decides when a snake has gone too long without food; the limit grows with the grid

    def __init__(self, factor: float) -> None:
        self._factor = factor

    def is_starved(self, unfed_step_count: int, grid_cell_count: int) -> bool:
        return unfed_step_count >= self._factor * grid_cell_count
