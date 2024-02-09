import asyncio
from src.ml.evolution import Evolution

evolution = Evolution()

res = asyncio.run(evolution.run())
res.fittest[0].save()

print(res.serialise())
