import asyncio
import time
from src.ml.evolution import Evolution
from src.config import config
from src.ml.generation_spec import GenerationSpec

spec = GenerationSpec.get()
gens = config.ml.evolution.generations

evolution = Evolution(spec, gens)

time_start = time.time()
res = asyncio.run(evolution.run())
time_end = time.time()

time_diff = time_end - time_start
print(res.serialise())
print(f"Time taken: {time_diff} seconds")
