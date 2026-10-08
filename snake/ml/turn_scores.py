from dataclasses import dataclass
from snake.core import Turn


@dataclass(frozen=True)
class TurnScores:
    # How good each turn looks to the brain; higher is better
    left: float
    ahead: float
    right: float

    @property
    def best_turn(self) -> Turn:
        # On a tie, the first highest in left, ahead, right order
        scored_turns = ((Turn.left, self.left), (Turn.ahead, self.ahead), (Turn.right, self.right))
        turn, _ = max(scored_turns, key=lambda scored_turn: scored_turn[1])
        return turn
