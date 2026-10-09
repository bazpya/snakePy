import random
from collections import deque
from snake.ml.experience import Experience


class ReplayMemory:
    # Keeps the latest experiences and hands out random batches; the oldest drop out when full

    def __init__(self, capacity: int, rng: random.Random | None = None) -> None:
        self._experiences: deque[Experience] = deque(maxlen=capacity)
        self._rng = rng or random.Random()

    @property
    def size(self) -> int:
        return len(self._experiences)

    def add(self, experience: Experience) -> None:
        self._experiences.append(experience)

    def sample(self, count: int) -> list[Experience]:
        # Raises ValueError when asked for more than it holds
        return self._rng.sample(list(self._experiences), count)
