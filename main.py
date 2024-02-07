import asyncio
from src.ml.evolution import Evolution

evolution = Evolution()

res = asyncio.run(evolution.run())

print(res.serialise())
