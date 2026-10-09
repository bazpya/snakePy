from typing import Protocol
from snake.core import StepResult


class RewarderConcept(Protocol):
    # What Recorder needs from a rewarder: a reward for the step that gave this result
    def get_reward(self, result: StepResult) -> float: ...
