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
        # A strip below the grid, so the status never covers any cells
        self._status = tk.Label(window, anchor="w", padx=4)
        self._status.pack(fill="x")
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

    def show_status(self, text: str) -> None:
        self._status.configure(text=text)

    def show_message(self, text: str) -> None:
        width = int(self._widget["width"])
        height = int(self._widget["height"])
        font_size = max(12, width // 10)  # grows with the canvas
        band_half_height = font_size
        # A dark band behind the text keeps it readable over the cells
        self._widget.create_rectangle(
            0, height // 2 - band_half_height,
            width, height // 2 + band_half_height,
            fill="black", width=0,
        )
        self._widget.create_text(
            width // 2, height // 2,
            text=text, fill="white", font=("TkDefaultFont", -font_size, "bold"),  # negative: size in pixels
        )
