class Event:
    _callbacks: list

    def __init__(self) -> None:
        self._callbacks = []

    def subscribe(self, callback) -> None:
        self._callbacks.append(callback)

    def unsubscribe(self, callback) -> None:
        self._callbacks.remove(callback)

    def emit(self, *args, **kwargs) -> None:
        for cb in self._callbacks:
            cb(*args, **kwargs)

    def purge(self) -> None:
        self._callbacks = []
