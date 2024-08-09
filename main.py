import asyncio
from src.ml.ml import ML as anything_to_invoke_stuff_in_the_sourced_file
from src.ml.evolution import Evolution

evolution = Evolution(verbose=True)
res = asyncio.run(evolution.run())
res.fittest[0].save()

line = "==============================="
print(f"\n{line}  Evolution Result  {line} \n")
print(res.serialise())
