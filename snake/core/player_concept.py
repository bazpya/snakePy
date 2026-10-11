from typing import Protocol
from snake.core.world_state import WorldState
from snake.core.turn import Turn


class PlayerConcept(Protocol):
    # What Game needs from a player: the next turn, given the latest state
    def pick_turn(self, state: WorldState) -> Turn: ...
