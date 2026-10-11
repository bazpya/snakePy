import math
import time
from collections.abc import Callable


def _get_now_ms() -> float:
    return time.monotonic() * 1000


class Clock:
    # Keeps a fixed beat: ticks are due every interval from the start,
    # however long each step takes; if far behind, it skips to the next beat

    def __init__(self, interval_ms: int, time_source: Callable[[], float] = _get_now_ms) -> None:
        self._interval_ms = interval_ms
        self._time_source = time_source  # returns the current time in milliseconds
        self._due_ms = 0.0

    def start(self) -> None:
        self._due_ms = self._time_source() + self._interval_ms

    def get_wait_ms(self) -> int:
        # Whole milliseconds until the next tick is due; 0 when already due
        return max(0, math.ceil(self._due_ms - self._time_source()))

    def advance(self) -> None:
        # Call once per tick; moves to the next beat still ahead
        self._due_ms += self._interval_ms
        now_ms = self._time_source()
        while self._due_ms <= now_ms:
            self._due_ms += self._interval_ms
