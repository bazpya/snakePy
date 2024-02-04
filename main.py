import asyncio
import time
from src.ml.generation import Generation
from src.ml.generation_spec import GenerationSpec

spec = GenerationSpec.get()

if spec.selection_count < 1:
    raise ValueError("No player survives the harsh selection ratio")

generation = Generation(1, spec)

time_start = time.time()
res = asyncio.run(generation.run())
time_end = time.time()

time_diff = time_end - time_start
print(res.serialise())
print(f"Time taken: {time_diff} seconds")
