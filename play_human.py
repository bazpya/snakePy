# Human play: arrow keys steer, a tkinter window shows the game
import tkinter as tk
from snake.config import Config
from snake.core import Factory, Game
from snake.human import HumanPlayer, KeySourceTk
from snake.ui import CanvasTk, Drawer, PacerTk


def main() -> None:
    config = Config()
    grid, display = config.grid, config.display
    world = Factory(grid.row_count, grid.col_count).create()
    window = tk.Tk()
    window.title("Snake")
    window.resizable(False, False)
    canvas = CanvasTk(window, grid.row_count, grid.col_count, display.cell_size)
    drawer = Drawer(canvas)
    key_source = KeySourceTk(window)
    player = HumanPlayer(key_source)
    game = Game(world, player, observers=[drawer])
    pacer = PacerTk(window, display.tick_interval_ms)
    pacer.run(game)


if __name__ == "__main__":
    main()
