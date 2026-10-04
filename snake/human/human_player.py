from collections import deque
from snake.core import Direction, StepResult, Turn, PlayerConcept
from snake.human.key_source_concept import KeySourceConcept


class HumanPlayer(PlayerConcept):
    # Queues arrow keys as they come and hands out one turn per step
    _max_queue_length = 10

    def __init__(self, key_source: KeySourceConcept) -> None:
        self._queue: deque[Direction] = deque()
        key_source.add_listener(self._on_key_pressed)

    def pick_turn(self, result: StepResult) -> Turn:
        if not self._queue:
            return Turn.ahead
        turn = result.direction.get_turn_to(self._queue.popleft())
        if turn is None:
            return Turn.ahead  # a reverse is ignored
        return turn

    def _on_key_pressed(self, key: str) -> None:
        # key is a key name, e.g. "Up"
        direction = _key_directions.get(key)
        if direction is None or self._is_full or self._is_repeat(direction):
            return
        self._queue.append(direction)

    @property
    def _is_full(self) -> bool:
        return len(self._queue) >= self._max_queue_length

    def _is_repeat(self, direction: Direction) -> bool:
        return bool(self._queue) and self._queue[-1] == direction


_key_directions = {
    "Up": Direction.up,
    "Right": Direction.right,
    "Down": Direction.down,
    "Left": Direction.left,
}
