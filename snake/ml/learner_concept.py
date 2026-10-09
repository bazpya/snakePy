from typing import Protocol
from snake.core import Turn
from snake.ml.turn_estimates import TurnEstimates


class LearnerConcept(Protocol):
    # What Teacher needs from a brain: its estimates, a way to improve them, and a frozen copy
    def estimate(self, state: list[float]) -> TurnEstimates: ...

    def learn(self, states: list[list[float]], turns: list[Turn], targets: list[float]) -> float: ...

    def copy(self) -> "LearnerConcept": ...
