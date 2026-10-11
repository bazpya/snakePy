from typing import Protocol
from snake.core.world_state import WorldState


class ObserverConcept(Protocol):
    # What Game needs from an observer: to be told how the game began, then each step
    def on_started(self, state: WorldState) -> None: ...

    def on_stepped(self, state: WorldState) -> None: ...
