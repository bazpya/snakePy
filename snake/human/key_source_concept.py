from typing import Callable, Protocol


class KeySourceConcept(Protocol):
    # What HumanPlayer needs: key names (e.g. "Up") delivered to it, by any means
    def add_listener(self, listener: Callable[[str], None]) -> None: ...
