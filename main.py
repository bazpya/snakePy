import asyncio
import time
from src.config import Config
from src.ml.generation import Generation
from src.ml.generation_spec import GenerationSpec

config = Config.get()
spec = GenerationSpec.get()

if spec.selection_count < 1:
    raise ValueError("No player survives the harsh selection ratio")

gens = config.ml.evolution.generations


async def go():
    res = None
    for i in range(gens):
        gen = Generation(i, spec, res)
        res = await gen.run()
    return res


time_start = time.time()
res = asyncio.run(go())
time_end = time.time()

time_diff = time_end - time_start
print(res.serialise())
print(f"Time taken: {time_diff} seconds")
