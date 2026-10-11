import tkinter as tk
from snake.core import Game
from snake.ui.clock import Clock


class PacerTk:
    # Runs a game on the tkinter timer, so the window stays responsive;
    # the clock keeps an even pace, however long each step takes

    def __init__(self, window: tk.Tk, tick_interval_ms: int) -> None:
        self._window = window
        self._clock = Clock(tick_interval_ms)
        self._game: Game | None = None

    def run(self, game: Game) -> None:
        # Blocks until the window is closed
        self._game = game
        game.start()
        self._clock.start()
        self._schedule_tick()
        self._window.mainloop()

    def _schedule_tick(self) -> None:
        self._window.after(self._clock.get_wait_ms(), self._tick)

    def _tick(self) -> None:
        self._clock.advance()
        self._game.tick()
        if not self._game.is_over():
            self._schedule_tick()
