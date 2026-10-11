from snake.core import ObserverConcept, WorldState


class Stats(ObserverConcept):
    # Keeps count of how one game is going; starting a game resets it

    def __init__(self) -> None:
        self.taken_step_count = 0

    def on_started(self, state: WorldState) -> None:
        self.taken_step_count = 0

    def on_stepped(self, state: WorldState) -> None:
        self.taken_step_count += 1
