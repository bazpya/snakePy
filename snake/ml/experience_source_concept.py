from typing import Protocol
from snake.ml.experience import Experience


class ExperienceSourceConcept(Protocol):
    # What Teacher needs from a memory: how much it holds, and a random batch
    @property
    def size(self) -> int: ...

    def sample(self, count: int) -> list[Experience]: ...
