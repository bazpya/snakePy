from snake.core import ObserverConcept, StepResult


class Stats(ObserverConcept):
    # Keeps count of how one game is going; starting a game resets it

    def __init__(self) -> None:
        self.taken_step_count = 0
        self.unfed_step_count = 0

    def on_started(self, result: StepResult) -> None:
        self.taken_step_count = 0
        self.unfed_step_count = 0

    def on_stepped(self, result: StepResult) -> None:
        self.taken_step_count += 1
        if result.just_ate:
            self.unfed_step_count = 0
        else:
            self.unfed_step_count += 1
