from typing import Protocol
from snake.core import Cell


class CanvasConcept(Protocol):
    # What Drawer needs from a drawing surface
    def fill(self, cell: Cell, colour: str) -> None: ...

    def show_message(self, text: str) -> None: ...
