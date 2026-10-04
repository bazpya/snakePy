# Human play: arrow keys steer, a tkinter window shows the game
import tkinter as tk
from snake.core import Factory, Game
from snake.human import HumanPlayer, KeySourceTk
from snake.ui import CanvasTk, Drawer, PacerTk

ROW_COUNT = 20
COL_COUNT = 20
CELL_SIZE = 24  # pixels
TICK_INTERVAL_MS = 120


def main() -> None:
    world = Factory(ROW_COUNT, COL_COUNT).create()
    window = tk.Tk()
    window.title("Snake")
    window.resizable(False, False)
    canvas = CanvasTk(window, ROW_COUNT, COL_COUNT, CELL_SIZE)
    drawer = Drawer(canvas)
    key_source = KeySourceTk(window)
    player = HumanPlayer(key_source)
    game = Game(world, player, observers=[drawer])
    pacer = PacerTk(window, TICK_INTERVAL_MS)
    pacer.run(game)


if __name__ == "__main__":
    main()
