from typing import Sequence
from snake.core.world_state import WorldState
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
        self._latest_state: WorldState | None = None

    # ====================  Queries  ====================

    def is_over(self) -> bool:
        return self._latest_state is not None and self._latest_state.is_over

    # ====================  Commands  ====================

    def start(self) -> None:
        if self._latest_state is not None:
            raise RuntimeError("The game has already started")
        self._latest_state = self._world.initial_state
        for observer in self._observers:
            observer.on_started(self._latest_state)

    def tick(self) -> WorldState:
        if self._latest_state is None:
            raise RuntimeError("The game has not started")
        if self.is_over():
            raise RuntimeError("The game is over")
        turn = self._player.pick_turn(self._latest_state)
        self._latest_state = self._world.step(turn)
        for observer in self._observers:
            observer.on_stepped(self._latest_state)
        return self._latest_state
