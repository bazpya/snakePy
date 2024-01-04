from threading import Timer


class Looper(Timer):
    counter: int = 0

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(self, *self.args, **self.kwargs)
