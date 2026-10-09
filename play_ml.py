# ML play: a brain steers, a tkinter window shows the game
import tkinter as tk
from snake.core import Factory, Game
from snake.ml import Brain, Eye, MLPlayer
from snake.ui import CanvasTk, Drawer, PacerTk

ROW_COUNT = 10
COL_COUNT = 10
CELL_SIZE = 24  # pixels
TICK_INTERVAL_MS = 120
STARVATION_FACTOR = 0.5  # starves after half the grid's cell count of steps without food


def main() -> None:
    world = Factory(ROW_COUNT, COL_COUNT, starvation_factor=STARVATION_FACTOR).create()
    window = tk.Tk()
    window.title("Snake (ML)")
    window.resizable(False, False)
    canvas = CanvasTk(window, ROW_COUNT, COL_COUNT, CELL_SIZE)
    drawer = Drawer(canvas)
    eye = Eye()
    brain = Brain(input_count=eye.output_count)  # untrained for now: random weights
    player = MLPlayer(eye, brain)
    game = Game(world, player, observers=[drawer])
    pacer = PacerTk(window, TICK_INTERVAL_MS)
    pacer.run(game)


if __name__ == "__main__":
    main()
