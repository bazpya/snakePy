class Event:
    _callbacks: [object]

    def __init__(self):
        self._callbacks = []

    def subscribe(self, callback):
        self._callbacks.append(callback)

    def unsubscribe(self, callback):
        self._callbacks.remove(callback)

    def emit(self, *args, **kwargs):
        for cb in self._callbacks:
            cb(*args, **kwargs)

    def purge(self):
        self._callbacks = []
