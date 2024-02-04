import asyncio
import math
import time
from src.ml.generation import Generation, GenerationSpecs
from src.ml.view import View
from src.config import Config

config = Config.get()

# ====================  Game Config  ====================

use_ui = config.game.use_ui
row_count = config.game.row_count
col_count = config.game.col_count
cell_size = config.game.cell_size
food_count = config.game.food_count
interval = config.game.interval

# ====================  ML Config  ====================

fake_player = config.ml.player.fake
max_steps = config.ml.player.max_steps

view = View.get()

# ====================  Generation config  ====================

population = config.ml.generation.population

# ====================  Evolution config  ====================

selection_ratio = config.ml.evolution.selection_ratio
selection_count = math.floor(population * selection_ratio)

if selection_count < 1:
    raise ValueError("No player survives the harsh selection ratio")


generation_specs = GenerationSpecs(
    population,
    selection_count,
    row_count,
    col_count,
    max_steps,
    fake_player,
    view,
    use_ui,
    cell_size,
    interval,
)

generation = Generation(1, generation_specs)


async def func():
    res = await generation.run()
    print(res.serialise())


time_start = time.time()
asyncio.run(func())
time_end = time.time()

time_diff = time_end - time_start

print(f"Time taken: {time_diff} seconds")
