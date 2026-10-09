from dataclasses import dataclass
from snake.core import Turn


@dataclass(frozen=True)
class TurnEstimates:
    # How good each turn looks to the brain; higher is better
    left: float
    ahead: float
    right: float

    @property
    def best_turn(self) -> Turn:
        # On a tie, the first highest in left, ahead, right order
        estimated_turns = ((Turn.left, self.left), (Turn.ahead, self.ahead), (Turn.right, self.right))
        turn, _ = max(estimated_turns, key=lambda estimated_turn: estimated_turn[1])
        return turn

    @property
    def best_estimate(self) -> float:
        return max(self.left, self.ahead, self.right)
