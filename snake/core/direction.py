from enum import Enum
from snake.core.turn import Turn


class Direction(Enum):
    # Clockwise order, so turning is just adding the Turn offset
    up = 0
    right = 1
    down = 2
    left = 3

    @property
    def step_delta(self) -> tuple[int, int]:
        # (row, col) change for one step; rows grow downwards
        return _deltas[self]

    def get_opposite(self) -> "Direction":
        number = self.value + self._half_turn_count
        corrected = self._correct_range(number)
        return Direction(corrected)

    def turn(self, turn: Turn) -> "Direction":
        number = self.value + turn.value
        corrected = self._correct_range(number)
        return Direction(corrected)

    def get_turn_to(self, other: "Direction") -> Turn | None:
        # None for the opposite direction: no single turn reaches it
        for turn in Turn:
            if self.turn(turn) == other:
                return turn
        return None

    @property
    def _full_turn_count(self) -> int:
        return len(Direction)

    @property
    def _half_turn_count(self) -> int:
        return len(Direction) // 2

    def _correct_range(self, input: int) -> int:
        return input % self._full_turn_count


_deltas = {
    Direction.up: (-1, 0),
    Direction.right: (0, 1),
    Direction.down: (1, 0),
    Direction.left: (0, -1),
}
