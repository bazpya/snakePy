from typing import Protocol
from snake.core import WorldState


class EyeConcept(Protocol):
    # What MLPlayer needs from an eye: a world state as numbers for the brain
    def see(self, state: WorldState) -> list[float]: ...
