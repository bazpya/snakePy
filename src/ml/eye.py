from src.ml.ml import ML
from src.game.direction import Direction
from src.ml.view import View, the_view
from src.game.cell import Cell


class Eye:
    def __init__(self, view: View = None) -> None:
        self._view = view or the_view
        self.view_size: int = self._view.size

    def see(self, head: Cell, food: Cell) -> ML.Tensor:
        signals = []
        recip = self._view._reciprocate_distances

        # Food
        (food_ver, food_hor, food_diag) = head.get_distance(recip, food)

        if self._view._food_squarewise:
            signals.extend([food_ver, food_hor])
        if self._view._food_diagonal:
            signals.append(food_diag)

        # Death squarewise
        (*etc, death_up) = head.death_distance(recip, Direction.up)
        (*etc, death_down) = head.death_distance(recip, Direction.down)
        (*etc, death_left) = head.death_distance(recip, Direction.left)
        (*etc, death_right) = head.death_distance(recip, Direction.right)

        if self._view._death_squarewise:
            signals.extend([death_up, death_down, death_left, death_right])

        # Death diagonal
        (*etc, death_up_right) = head.death_distance(
            recip,
            Direction.up,
            Direction.right,
        )
        (*etc, death_up_left) = head.death_distance(
            recip,
            Direction.up,
            Direction.left,
        )
        (*etc, death_down_right) = head.death_distance(
            recip,
            Direction.down,
            Direction.right,
        )
        (*etc, death_down_left) = head.death_distance(
            recip,
            Direction.down,
            Direction.left,
        )

        if self._view._death_diagonal:
            signals.extend(
                [
                    death_up_left,
                    death_up_right,
                    death_down_left,
                    death_down_right,
                ]
            )

        return ML.convert_to_tensor(signals)
