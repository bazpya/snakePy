import asyncio
from src.ml.ml import ML as anything_to_invoke_stuff_in_the_sourced_file
from src.ml.evolution import Evolution

print("Wait for AI to play the game ... \n")
evolution = Evolution()
res = asyncio.run(evolution.run())
res.fittest[0].save()

line = "==============================="
print(f"{line}  Evolution Result  {line} \n")
print(res.serialise())
