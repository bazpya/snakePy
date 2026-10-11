# ML play: a brain steers, a tkinter window shows the game
import tkinter as tk
from snake.config import Config
from snake.core import Factory, Game
from snake.ml import Brain, Eye, MLPlayer
from snake.ui import CanvasTk, Drawer, PacerTk


def main() -> None:
    config = Config()
    grid, display, brain_path = config.grid, config.display, config.paths.brain_path
    world = Factory(grid.row_count, grid.col_count, starvation_factor=grid.starvation_factor).create()
    window = tk.Tk()
    window.title("Snake (ML)")
    window.resizable(False, False)
    canvas = CanvasTk(window, grid.row_count, grid.col_count, display.cell_size)
    drawer = Drawer(canvas)
    eye = Eye()
    brain = Brain(input_count=eye.output_count)
    if brain_path.exists():
        brain.load(brain_path)
    else:
        print(f"{brain_path} not found: playing untrained, with random weights")
    player = MLPlayer(eye, brain)
    game = Game(world, player, observers=[drawer])
    pacer = PacerTk(window, display.tick_interval_ms)
    pacer.run(game)


if __name__ == "__main__":
    main()
