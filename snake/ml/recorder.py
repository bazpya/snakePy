from snake.core import ObserverConcept, WorldState
from snake.ml.experience import Experience
from snake.ml.eye_concept import EyeConcept
from snake.ml.replay_memory_concept import ReplayMemoryConcept
from snake.ml.rewarder_concept import RewarderConcept


class Recorder(ObserverConcept):
    # Turns each step into an experience and puts it in the memory

    def __init__(self, eye: EyeConcept, rewarder: RewarderConcept, memory: ReplayMemoryConcept) -> None:
        self._eye = eye
        self._rewarder = rewarder
        self._memory = memory
        self._sight: list[float] = []

    def on_started(self, state: WorldState) -> None:
        self._sight = self._eye.see(state)

    def on_stepped(self, state: WorldState) -> None:
        next_sight = self._eye.see(state)
        self._memory.add(Experience(
            sight=self._sight,
            turn=state.last_turn,
            reward=self._rewarder.get_reward(state),
            next_sight=next_sight,
            is_over=state.is_over,
        ))
        self._sight = next_sight
