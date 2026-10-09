from typing import Protocol
from snake.ml.experience import Experience


class ReplayMemoryConcept(Protocol):
    # What Recorder needs from a memory: somewhere to put each experience
    def add(self, experience: Experience) -> None: ...
