from typing import Protocol
from snake.core.step_result import StepResult


class ObserverConcept(Protocol):
    # What Game needs from an observer: to be told how the game began, then each step
    def on_started(self, result: StepResult) -> None: ...

    def on_stepped(self, result: StepResult) -> None: ...
