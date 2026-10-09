from typing import Protocol
from snake.ml.turn_estimates import TurnEstimates


class BrainConcept(Protocol):
    # What MLPlayer needs from a brain: an estimate for each turn, given what the eye sees
    def estimate(self, state: list[float]) -> TurnEstimates: ...
