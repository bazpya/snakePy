import random
from snake.core import PlayerConcept, StepResult, Turn


class ExploringPlayer(PlayerConcept):
    # For training: sometimes tries a random turn instead of asking the inner player;
    # how often (epsilon) shrinks as training goes on

    def __init__(
        self,
        player: PlayerConcept,
        epsilon: float,
        min_epsilon: float,
        decay_factor: float,
        rng: random.Random | None = None,
    ) -> None:
        self._player = player
        self._epsilon = epsilon
        self._min_epsilon = min_epsilon
        self._decay_factor = decay_factor
        self._rng = rng or random.Random()

    @property
    def epsilon(self) -> float:
        return self._epsilon

    def pick_turn(self, result: StepResult) -> Turn:
        if self._rng.random() < self._epsilon:
            return self._rng.choice(list(Turn))
        return self._player.pick_turn(result)

    def decay_epsilon(self) -> None:
        self._epsilon = max(self._min_epsilon, self._epsilon * self._decay_factor)
