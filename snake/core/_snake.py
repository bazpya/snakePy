from collections import deque
from snake.core.direction import Direction
from snake.core.cell import Cell
from snake.core.turn import Turn


class Snake:
    # Owns its body and heading only; walls, food and death are the World's business

    def __init__(self, start: Cell, direction: Direction) -> None:
        self._body: deque[Cell] = deque([start])  # tail -> head
        self._occupied: set[Cell] = {start}  # same cells as _body, for fast lookup
        self._direction = direction
        self._next_direction = direction

    # ====================  Queries  ====================

    @property
    def head(self) -> Cell:
        return self._body[-1]

    @property
    def tail(self) -> Cell:
        return self._body[0]

    @property
    def cells(self) -> frozenset[Cell]:
        # Unordered on purpose; use head for the front end
        return frozenset(self._occupied)

    @property
    def length(self) -> int:
        return len(self._body)

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def next_head(self) -> Cell:
        return self.head + self._next_direction

    def is_hitting_itself(self) -> bool:
        # The tail's cell is safe: it moves away in the same step.
        # Growing into the tail can't happen, since food is never on the snake.
        next_head = self.next_head
        return self._occupies(next_head) and next_head != self.tail

    # ====================  Commands  ====================

    def turn(self, turn: Turn) -> None:
        # Relative to the direction of the last step; a turn can never reverse the snake
        self._next_direction = self._direction.turn(turn)

    def step(self, grow: bool = False) -> None:
        new_head = self.next_head
        if not grow:
            # Drop the tail first, so the head may take the cell the tail leaves
            tail = self._body.popleft()
            self._occupied.discard(tail)
        self._body.append(new_head)
        self._occupied.add(new_head)
        self._direction = self._next_direction

    # ====================  Helpers  ====================

    def _occupies(self, cell: Cell) -> bool:
        return cell in self._occupied
