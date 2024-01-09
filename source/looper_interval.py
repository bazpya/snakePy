import asyncio


class LooperInterval:
    _iterations: int
    counter: int
    _interval: float
    _func: object
    _should_continue: bool
    _end_callback: object
    _args: tuple

    def __init__(
        self,
        func: object,
        interval: float,
        iterations: int = None,
        end_callback: object = lambda: None,
        args: tuple = (),
    ):
        self.counter = 0
        self._interval = interval
        self._func = func
        self._iterations = iterations
        self._args = args
        self._end_callback = end_callback

    async def start(self):
        self._should_continue = True
        if self._iterations is None:
            while self._should_continue:
                await self._cycle()
        else:
            while self._should_continue and self._iterations > 0:
                await self._cycle()
                self._iterations -= 1
        self._end_callback()
        return self.counter

    def stop(self):
        self._should_continue = False
        return self.counter

    async def _cycle(self):
        await asyncio.sleep(self._interval)
        self._func(*self._args)
        self.counter = self.counter + 1
