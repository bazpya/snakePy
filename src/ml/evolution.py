from src.ml.generation import Generation


class Evolution:

    def __init__(self, generations: int = 1) -> None:
        self._genererations = generations

    async def run(self) -> None:
        res = None
        for i in range(self._genererations):
            gen = Generation(i, res)
            res = await gen.run()
        return res
