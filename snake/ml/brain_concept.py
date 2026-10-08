from typing import Protocol
from snake.ml.turn_scores import TurnScores


class BrainConcept(Protocol):
    # What MLPlayer needs from a brain: a score for each turn, given what the eye sees
    def score(self, state: list[float]) -> TurnScores: ...
