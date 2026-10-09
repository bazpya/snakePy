from snake.core import PlayerConcept, StepResult, Turn
from snake.ml.brain_concept import BrainConcept
from snake.ml.eye_concept import EyeConcept


class MLPlayer(PlayerConcept):
    # Sees the result, lets the brain estimate each turn, and takes the best one

    def __init__(self, eye: EyeConcept, brain: BrainConcept) -> None:
        self._eye = eye
        self._brain = brain

    def pick_turn(self, result: StepResult) -> Turn:
        state = self._eye.see(result)
        return self._brain.estimate(state).best_turn
