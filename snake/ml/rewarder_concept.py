from typing import Protocol
from snake.core import WorldState


class RewarderConcept(Protocol):
    # What Recorder needs from a rewarder: a reward for the step that led to this state
    def get_reward(self, state: WorldState) -> float: ...
