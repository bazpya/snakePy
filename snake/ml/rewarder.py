from snake.core import StepResult


class Rewarder:
    # Scores one step for learning; each rule is a separate weight, and they add up
    _food_reward = 1.0
    _crash_penalty = -1.0
    _starvation_penalty = -1.0

    def get_reward(self, result: StepResult, is_starved: bool) -> float:
        # is_starved: the training loop cut the game short, too long without food
        reward = 0.0
        if result.just_ate:
            reward += self._food_reward  # also covers filling the grid: a win
        elif result.is_over:
            reward += self._crash_penalty
        if is_starved:
            reward += self._starvation_penalty
        return reward
