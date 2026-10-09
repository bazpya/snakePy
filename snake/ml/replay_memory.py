import random
from collections import deque
from snake.ml.experience import Experience
from snake.ml.experience_source_concept import ExperienceSourceConcept
from snake.ml.replay_memory_concept import ReplayMemoryConcept


class ReplayMemory(ExperienceSourceConcept, ReplayMemoryConcept):
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
