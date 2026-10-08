from typing import Protocol
from snake.core import StepResult


class EyeConcept(Protocol):
    # What MLPlayer needs from an eye: a step result as numbers for the brain
    def see(self, result: StepResult) -> list[float]: ...
