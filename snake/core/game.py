from typing import Sequence
from snake.core.step_result import StepResult
from snake.core.world import World
from snake.core.player_concept import PlayerConcept
from snake.core.observer_concept import ObserverConcept


class Game:
    # Drives one world as a game: asks the player, steps the world, tells the observers.
    # No timing: callers decide when to tick (a UI timer, or a plain loop)

    def __init__(
        self,
        world: World,
        player: PlayerConcept,
        observers: Sequence[ObserverConcept] = (),
    ) -> None:
        self._world = world
        self._player = player
        self._observers = tuple(observers)
        self._latest_result: StepResult | None = None

    # ====================  Queries  ====================

    def is_over(self) -> bool:
        return self._latest_result is not None and self._latest_result.is_over

    # ====================  Commands  ====================

    def start(self) -> None:
        if self._latest_result is not None:
            raise RuntimeError("The game has already started")
        self._latest_result = self._world.initial_result
        for observer in self._observers:
            observer.on_started(self._latest_result)

    def tick(self) -> StepResult:
        if self._latest_result is None:
            raise RuntimeError("The game has not started")
        if self.is_over():
            raise RuntimeError("The game is over")
        turn = self._player.pick_turn(self._latest_result)
        self._latest_result = self._world.step(turn)
        for observer in self._observers:
            observer.on_stepped(self._latest_result)
        return self._latest_result
