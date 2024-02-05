from src.ml.generation import Generation
from src.ml.generation_spec import GenerationSpec


class Evolution:

    def __init__(self, specs: GenerationSpec, generations: int = 1) -> None:
        self._specs = specs
        self._genererations = generations

    async def run(self) -> None:
        res = None
        for i in range(self._genererations):
            gen = Generation(i, self._specs, res)
            res = await gen.run()
        return res
