import tkinter as tk
from typing import Callable
from snake.human.key_source_concept import KeySourceConcept


class KeySourceTk(KeySourceConcept):
    # Delivers key presses from a tkinter window

    def __init__(self, window: tk.Tk) -> None:
        self._window = window

    def add_listener(self, listener: Callable[[str], None]) -> None:
        # add="+" keeps earlier listeners bound
        self._window.bind("<Key>", lambda event: listener(event.keysym), add="+")
