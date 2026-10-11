from snake.core import EndCause, WorldState
from snake.ml.rewarder_concept import RewarderConcept


class Rewarder(RewarderConcept):
    # Scores one step for learning; each rule is a separate weight, and they add up
    _food_reward = 1.0
    _crash_penalty = -1.0
    _starvation_penalty = -1.0

    def get_reward(self, state: WorldState) -> float:
        reward = 0.0
        if state.just_ate:
            reward += self._food_reward  # also covers filling the grid: a win
        if state.end_cause == EndCause.crashed:
            reward += self._crash_penalty
        if state.end_cause == EndCause.starved:
            reward += self._starvation_penalty
        return reward
