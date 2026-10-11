from snake.core import PlayerConcept, Turn, WorldState
from snake.ml.brain_concept import BrainConcept
from snake.ml.eye_concept import EyeConcept


class MLPlayer(PlayerConcept):
    # Sees the state, lets the brain estimate each turn, and takes the best one

    def __init__(self, eye: EyeConcept, brain: BrainConcept) -> None:
        self._eye = eye
        self._brain = brain

    def pick_turn(self, state: WorldState) -> Turn:
        sight = self._eye.see(state)
        return self._brain.estimate(sight).best_turn
