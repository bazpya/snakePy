import tkinter as tk
from snake.core import Cell
from snake.ui.canvas_concept import CanvasConcept


class CanvasTk(CanvasConcept):
    # Draws cells as squares on a tkinter canvas inside the given window

    def __init__(self, window: tk.Tk, row_count: int, col_count: int, cell_size: int) -> None:
        self._widget = tk.Canvas(
            window,
            width=col_count * cell_size,
            height=row_count * cell_size,
            highlightthickness=0,
        )
        self._widget.pack()
        # One square per cell, created once and only recoloured afterwards
        self._squares = {
            Cell(row, col): self._widget.create_rectangle(
                col * cell_size,
                row * cell_size,
                (col + 1) * cell_size,
                (row + 1) * cell_size,
                width=0,
            )
            for row in range(row_count)
            for col in range(col_count)
        }

    def fill(self, cell: Cell, colour: str) -> None:
        self._widget.itemconfigure(self._squares[cell], fill=colour)

    def show_message(self, text: str) -> None:
        width = int(self._widget["width"])
        height = int(self._widget["height"])
        self._widget.create_text(width // 2, height // 2, text=text, fill="white")
