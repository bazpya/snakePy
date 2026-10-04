import tkinter as tk
from snake.core import Game


class PacerTk:
    # Runs a game on the tkinter timer, so the window stays responsive

    def __init__(self, window: tk.Tk, tick_interval_ms: int) -> None:
        self._window = window
        self._tick_interval_ms = tick_interval_ms
        self._game: Game | None = None

    def run(self, game: Game) -> None:
        # Blocks until the window is closed
        self._game = game
        game.start()
        self._schedule_tick()
        self._window.mainloop()

    def _schedule_tick(self) -> None:
        self._window.after(self._tick_interval_ms, self._tick)

    def _tick(self) -> None:
        self._game.tick()
        if not self._game.is_over():
            self._schedule_tick()
