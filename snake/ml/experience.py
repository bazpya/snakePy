from dataclasses import dataclass
from snake.core import Turn


@dataclass(frozen=True)
class Experience:
    # One step as the learner sees it: what was seen, what was done, and what came of it
    sight: list[float]
    turn: Turn
    reward: float
    next_sight: list[float]
    is_over: bool
