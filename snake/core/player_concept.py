from typing import Protocol
from snake.core.step_result import StepResult
from snake.core.turn import Turn


class PlayerConcept(Protocol):
    # What Game needs from a player: the next turn, given the latest result
    def pick_turn(self, result: StepResult) -> Turn: ...
