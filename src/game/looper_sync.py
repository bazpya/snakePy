class LooperSync:
    _iterations: int
    counter: int
    _func: object
    _should_continue: bool
    _end_callback: object
    _args: tuple

    def __init__(
        self,
        func: object,
        iterations: int = None,
        end_callback: object = lambda: None,
        args: tuple = (),
    ):
        self.counter = 0
        self._func = func
        self._iterations = iterations
        self._args = args
        self._end_callback = end_callback

    def start(self):
        self._should_continue = True
        if self._iterations is None:
            while self._should_continue:
                self._cycle()
        else:
            while self._should_continue and self._iterations > 0:
                self._cycle()
                self._iterations -= 1
        self._end_callback()
        return self.counter

    def stop(self):
        self._should_continue = False
        return self.counter

    def _cycle(self):
        self._func(*self._args)
        self.counter = self.counter + 1
