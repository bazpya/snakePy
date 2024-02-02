import asyncio
import time
from src.ml.generation import Generation, GenerationParam
from src.ml.view import View
from src.config import Config

# ====================  Game Config  ====================

use_ui = Config.get("game.use_ui")
row_count = Config.get("game.row_count")
col_count = Config.get("game.col_count")
cell_size = Config.get("game.cell_size")
food_count = Config.get("game.food_count")
interval = Config.get("game.interval")

# ====================  ML Config  ====================

fake_player = Config.get("ml.player.fake")
max_steps = Config.get("ml.player.max_steps")

view = View(
    reciprocate_distances=Config.get("ml.grid_view.reciprocate_distances"),
    food_squarewise=Config.get("ml.grid_view.food_squarewise"),
    food_diagonal=Config.get("ml.grid_view.food_diagonal"),
    death_squarewise=Config.get("ml.grid_view.death_squarewise"),
    death_diagonal=Config.get("ml.grid_view.death_diagonal"),
)

# ====================  Generation config  ====================

population = Config.get("ml.generation.population")

# ====================  Evolution config  ====================
selection_ratio = Config.get("ml.evolution.selection_ratio")


gen_params = GenerationParam(
    population,
    row_count,
    col_count,
    max_steps,
    fake_player,
    view,
    use_ui,
    cell_size,
    interval,
)

generation = Generation(1, gen_params)


async def func():
    res = await generation.run()
    print(res.serialise())


time_start = time.time()
asyncio.run(func())
time_end = time.time()

time_diff = time_end - time_start

print(f"Time taken: {time_diff} seconds")
