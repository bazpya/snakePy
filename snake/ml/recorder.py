from snake.core import ObserverConcept, StepResult
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
        self._state: list[float] = []

    def on_started(self, result: StepResult) -> None:
        self._state = self._eye.see(result)

    def on_stepped(self, result: StepResult) -> None:
        next_state = self._eye.see(result)
        self._memory.add(Experience(
            state=self._state,
            turn=result.last_turn,
            reward=self._rewarder.get_reward(result),
            next_state=next_state,
            is_over=result.is_over,
        ))
        self._state = next_state
