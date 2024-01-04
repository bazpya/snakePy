import asyncio


class Looper2:
    _iterations: int
    counter: int
    _interval: float
    _func: object
    _should_continue: bool
    _args: tuple

    def __init__(
        self, func: object, interval: float, iterations: int = None, args: tuple = ()
    ):
        self.counter = 0
        self._interval = interval
        self._func = func
        self._iterations = iterations
        self._args = args

    async def start(self):
        self._should_continue = True
        if self._iterations is None:
            while self._should_continue:
                await self._cycle()
        else:
            while self._should_continue and self._iterations > 0:
                await self._cycle()
                self._iterations -= 1
        return True

    def stop(self):
        self._should_continue = False
        return self.counter

    async def _cycle(self):
        await asyncio.sleep(self._interval)
        self._func(*self._args, self)
        self.counter = self.counter + 1